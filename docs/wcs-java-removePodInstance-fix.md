# removePodInstance 修复方案

## 问题描述

当前 `RmUatServiceImpl.removePodInstance()` 只调 STS 副本数为 0，**不删除 VIPC/PVC**，导致资源泄露。

## 修复方案

### 核心原则

**清理 K8s 资源必须在 DB 元数据回收后执行**，避免 DB 删除失败但 K8s 资源已被删除的不一致状态。

### 修改文件

`wcs-rm/src/main/java/cn/webank/wcs/rm/service/uat/RmUatServiceImpl.java`

### 修复代码

```java
public ResultDto<Void> removePodInstance(RemoveInstanceRequest request, String traceId) {
    logger.info("removePodInstance request={}, traceId={}", request, traceId);
    String podName = request.getName().toLowerCase();

    // query from RM
    ResultDto getPodRsp = uatRmService.getPodInfoByPodName(request.getName());
    if (!getPodRsp.isSuccess() && !getPodRsp.getMessage().equals(ResponseMsg.POD_NOT_FOUND)) {
        return getPodRsp;
    }

    PodInfo podInfo = (PodInfo) getPodRsp.getData();
    if (podInfo != null && !StringUtils.isEmpty(request.getIp()) && !podInfo.getPodIp().equals(request.getIp())) {
        return ResultDto.newDefaultFailedResult(traceId, "request ip not match name");
    }
    ResultDto<Void> resultDto = ResultDto.newSuccessResult("remove success", traceId, null);
    if (podInfo == null) {
        if (!StringUtils.hasLength(request.getClusterId())) {
            return ResultDto.newDefaultFailedResult(traceId, "pod not found in RM, clusterId can not null");
        }
        podInfo = new PodInfo();
        podInfo.setClusterId(request.getClusterId());
        podInfo.setPodName(podName);
    } else {
        // Step 1: 从 RM (DB) 删除元数据
        resultDto = uatRmService.removePodInstance(request);
        if (!resultDto.isSuccess()) {
            String msg = String.format("removePodInstance code !=0, code=%s, response body=%s", 
                resultDto.getCode(), GsonUtil.toJsonFilterNullField(resultDto));
            logger.warn(msg);
            return resultDto.newDefaultFailedResult(traceId, msg);
        } else {
            String msg = String.format("removePodInstance success, response message=%s, data=%s, traceId=%s", 
                resultDto.getMessage(), GsonUtil.toJsonFilterNullField(resultDto.getData()), traceId);
            logger.info(msg);
            resultDto = resultDto.newSuccessResult(msg, traceId, resultDto.getData());
        }
    }

    // Step 2: 清理 K8s 资源（DB 删除成功后执行）
    try {
        cleanupK8sResources(podName, podInfo.getClusterId(), traceId);
    } catch (Exception e) {
        // K8s 清理失败不影响返回结果，记录告警即可
        logger.error("cleanupK8sResources failed, podName={}, clusterId={}, traceId={}, error={}", 
            podName, podInfo.getClusterId(), traceId, e.getMessage(), e);
    }

    return resultDto;
}

/**
 * 清理 K8s 资源：STS、VIPC、PVC
 * 在 DB 元数据删除成功后调用
 */
private void cleanupK8sResources(String podName, String clusterId, String traceId) {
    logger.info("cleanupK8sResources start, podName={}, clusterId={}, traceId={}", podName, clusterId, traceId);

    // 2.1 删除 VIPC（所有 ordinal）
    deleteAllVipcs(podName, clusterId, traceId);

    // 2.2 删除 STS
    deleteStatefulSet(podName, clusterId, traceId);

    // 2.3 删除 PVC（如果有）
    deletePvc(podName, clusterId, traceId);

    logger.info("cleanupK8sResources completed, podName={}, clusterId={}, traceId={}", podName, clusterId, traceId);
}

/**
 * 删除所有 ordinal 的 VIPC
 * StatefulSet 可能有多个副本，需要删除所有 VIPC
 */
private void deleteAllVipcs(String podName, String clusterId, String traceId) {
    // 删除 ordinal=0 的 VIPC
    deleteVipcWithRetry(clusterId, podName + "-0", traceId);

    // 尝试删除 ordinal=1~9 的 VIPC（如果存在）
    for (int i = 1; i <= 9; i++) {
        String vipcName = podName + "-" + i;
        try {
            deleteVipcWithRetry(clusterId, vipcName, traceId);
        } catch (Exception e) {
            // ordinal>=1 的 VIPC 可能不存在，忽略错误
            logger.debug("delete vipc {} failed (may not exist), error={}", vipcName, e.getMessage());
            break; // 如果 ordinal=N 不存在，后面的也不会存在
        }
    }
}

/**
 * 删除 VIPC（带重试）
 */
private void deleteVipcWithRetry(String clusterId, String vipcName, String traceId) {
    int maxRetries = 3;
    for (int i = 0; i < maxRetries; i++) {
        try {
            deleteVipc(clusterId, vipcName);
            logger.info("deleteVipc success, clusterId={}, vipcName={}, traceId={}", clusterId, vipcName, traceId);
            return;
        } catch (Exception e) {
            String errorMsg = e.getMessage();
            // VIPC 不存在，视为成功
            if (errorMsg != null && errorMsg.contains("not exist")) {
                logger.info("vipc not exist, clusterId={}, vipcName={}, traceId={}", clusterId, vipcName, traceId);
                return;
            }
            if (i < maxRetries - 1) {
                logger.warn("deleteVipc failed, retry {}/{}, clusterId={}, vipcName={}, error={}", 
                    i + 1, maxRetries, clusterId, vipcName, errorMsg);
                try {
                    Thread.sleep(500);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                }
            } else {
                logger.error("deleteVipc failed after {} retries, clusterId={}, vipcName={}, traceId={}", 
                    maxRetries, clusterId, vipcName, traceId);
                throw new RuntimeException("delete vipc failed: " + errorMsg);
            }
        }
    }
}

/**
 * 删除 StatefulSet
 */
private void deleteStatefulSet(String podName, String clusterId, String traceId) {
    try {
        DeleteStsResponse deleteRsp = deleteStatefulSet(podName, clusterId);
        String deleteMsg = deleteRsp.getMsg();
        boolean stsNotExistOrSuccess = deleteMsg != null && 
            (deleteMsg.contains("not exist") || deleteMsg.contains(ResponseMsg.STS_NOT_EXIST));
        
        if (!deleteRsp.isSuccess() && !stsNotExistOrSuccess) {
            logger.error("deleteStatefulSet failed, podName={}, clusterId={}, traceId={}, error={}", 
                podName, clusterId, traceId, deleteMsg);
        } else {
            logger.info("deleteStatefulSet success, podName={}, clusterId={}, traceId={}", podName, clusterId, traceId);
        }
    } catch (Exception e) {
        logger.error("deleteStatefulSet exception, podName={}, clusterId={}, traceId={}", 
            podName, clusterId, traceId, e);
    }
}

/**
 * 删除 PVC
 */
private void deletePvc(String podName, String clusterId, String traceId) {
    try {
        // 检查 pod 是否使用了 CFS
        // 如果使用了 CFS，需要删除 PVC 和 PV
        DeletePvcResponse deletePvcRsp = deletePvc(podName, clusterId);
        String deleteMsg = deletePvcRsp.getMsg();
        boolean pvcNotExistOrSuccess = deleteMsg != null && 
            (deleteMsg.contains("not exist") || deleteMsg.contains("not found"));
        
        if (!deletePvcRsp.isSuccess() && !pvcNotExistOrSuccess) {
            logger.warn("deletePvc failed (pod may not use cfs), podName={}, clusterId={}, traceId={}, error={}", 
                podName, clusterId, traceId, deleteMsg);
        } else {
            logger.info("deletePvc success, podName={}, clusterId={}, traceId={}", podName, clusterId, traceId);
            
            // 删除关联的 PV
            if (pvcNotExistOrSuccess == false) {
                try {
                    deletePv(podName, clusterId);
                    logger.info("deletePv success, podName={}, clusterId={}, traceId={}", podName, clusterId, traceId);
                } catch (Exception e) {
                    logger.warn("deletePv failed, podName={}, clusterId={}, traceId={}, error={}", 
                        podName, clusterId, traceId, e.getMessage());
                }
            }
        }
    } catch (Exception e) {
        // PVC 删除失败不阻塞流程（可能 pod 没有使用 CFS）
        logger.debug("deletePvc exception (pod may not use cfs), podName={}, clusterId={}, traceId={}", 
            podName, clusterId, traceId, e);
    }
}
```

## 执行流程

```
1. 从 DB 查询 pod 信息
   ↓
2. 从 RM (DB) 删除 pod 元数据
   ↓ (成功)
3. 清理 K8s 资源（cleanupK8sResources）:
   3.1 删除所有 VIPC (ordinal=0~N)
   3.2 删除 STS
   3.3 删除 PVC + PV (如果有)
   ↓
4. 返回结果
```

## 关键改动

| 项目 | 修改前 | 修改后 |
|------|--------|--------|
| VIPC | ❌ 不删除 | ✅ 删除所有 ordinal |
| STS | 调副本数 → 0 | ✅ 完全删除 |
| PVC | ❌ 不删除 | ✅ 删除 (如果有) |
| 执行顺序 | K8s 清理在 DB 前 | ✅ DB 删除成功后再清理 K8s |

## 异常处理

1. **DB 删除失败** → 直接返回失败，不清理 K8s
2. **K8s 清理失败** → 记录告警日志，不影响返回结果（DB 已删除成功）
3. **VIPC 不存在** → 视为成功，继续清理其他资源
4. **PVC 删除失败** → 不阻塞流程（可能 pod 没有使用 CFS）

## 测试建议

1. **单副本 pod**：验证 VIPC-0、STS、PVC 正常删除
2. **多副本 pod**：验证所有 ordinal 的 VIPC 都被删除
3. **使用 CFS 的 pod**：验证 PVC + PV 被删除
4. **DB 删除失败**：验证 K8s 资源不被清理
5. **VIPC 已被手动删除**：验证代码正常处理

## 注意事项

⚠️ **此修复会改变 UAT 回收行为**：从"软删除"（调副本数）变为"硬删除"（完全清理）。需要确认：
1. 是否有依赖 STS 保留的场景？
2. 是否需要保留 PVC 数据？
3. 回滚策略：如果清理失败，是否需要重建 STS？
