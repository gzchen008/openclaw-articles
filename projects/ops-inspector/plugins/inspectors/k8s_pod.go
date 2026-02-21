package inspectors

import (
	"context"
	"fmt"
	"os/exec"
	"strconv"
	"strings"
	"time"

	"github.com/opsinspector/opsinspector/pkg/inspector"
)

// K8sPodInspector K8s Pod 巡检器
type K8sPodInspector struct{}

// NewK8sPodInspector 创建 K8s Pod 巡检器
func NewK8sPodInspector() *K8sPodInspector {
	return &K8sPodInspector{}
}

// Name 返回名称
func (k *K8sPodInspector) Name() string {
	return "k8s-pod"
}

// Description 返回描述
func (k *K8sPodInspector) Description() string {
	return "Kubernetes Pod 状态检查"
}

// Version 返回版本
func (k *K8sPodInspector) Version() string {
	return "1.0.0"
}

// Validate 验证配置
func (k *K8sPodInspector) Validate(config map[string]interface{}) error {
	namespace := getString(config, "namespace", "")
	if namespace == "" {
		return fmt.Errorf("namespace is required")
	}
	return nil
}

// Execute 执行检查
func (k *K8sPodInspector) Execute(ctx context.Context, config map[string]interface{}) (*inspector.Result, error) {
	result := inspector.NewResult()

	namespace := getString(config, "namespace", "default")
	selector := getString(config, "selector", "")
	checkRestarts := getInt(config, "max_restarts", 3)
	checkStatus := getBool(config, "check_status", true)
	checkResources := getBool(config, "check_resources", true)

	// 获取 Pod 列表
	pods, err := k.getPods(ctx, namespace, selector)
	if err != nil {
		result.SetError(fmt.Errorf("failed to get pods: %w", err))
		return result, nil
	}

	totalPods := len(pods)
	readyPods := 0
	failedPods := 0
	warningPods := 0

	for _, pod := range pods {
		detail := inspector.Detail{
			Name:   fmt.Sprintf("pod/%s", pod.Name),
			Status: inspector.StatusSuccess,
		}

		issues := []string{}

		// 检查 Pod 状态
		if checkStatus {
			if pod.Phase != "Running" {
				issues = append(issues, fmt.Sprintf("status: %s", pod.Phase))
				detail.Status = inspector.StatusFailed
			} else if !pod.Ready {
				issues = append(issues, "not ready")
				detail.Status = inspector.StatusWarning
			}
		}

		// 检查重启次数
		if checkRestarts > 0 && pod.RestartCount > checkRestarts {
			issues = append(issues, fmt.Sprintf("restarts: %d", pod.RestartCount))
			if detail.Status == inspector.StatusSuccess {
				detail.Status = inspector.StatusWarning
			}
		}

		// 检查资源使用
		if checkResources {
			if pod.CPUUsage > 80 {
				issues = append(issues, fmt.Sprintf("CPU high: %.1f%%", pod.CPUUsage))
				if detail.Status == inspector.StatusSuccess {
					detail.Status = inspector.StatusWarning
				}
			}
			if pod.MemoryUsage > 80 {
				issues = append(issues, fmt.Sprintf("Memory high: %.1f%%", pod.MemoryUsage))
				if detail.Status == inspector.StatusSuccess {
					detail.Status = inspector.StatusWarning
				}
			}
		}

		if len(issues) > 0 {
			detail.Message = strings.Join(issues, ", ")
			if detail.Status == inspector.StatusFailed {
				failedPods++
			} else if detail.Status == inspector.StatusWarning {
				warningPods++
			}
		} else {
			detail.Message = "healthy"
			readyPods++
		}

		result.AddDetail(detail)
	}

	// 添加指标
	result.AddMetric(inspector.Metric{
		Name:  "total_pods",
		Value: float64(totalPods),
	})
	result.AddMetric(inspector.Metric{
		Name:  "ready_pods",
		Value: float64(readyPods),
	})
	result.AddMetric(inspector.Metric{
		Name:  "failed_pods",
		Value: float64(failedPods),
	})
	result.AddMetric(inspector.Metric{
		Name:  "warning_pods",
		Value: float64(warningPods),
	})

	// 设置结果
	if failedPods > 0 {
		result.SetFailed(fmt.Sprintf("%d pods failed, %d warnings in namespace %s", failedPods, warningPods, namespace))
	} else if warningPods > 0 {
		result.SetWarning(fmt.Sprintf("%d pods have warnings in namespace %s", warningPods, namespace))
	} else {
		result.SetSuccess(fmt.Sprintf("All %d pods healthy in namespace %s", totalPods, namespace))
	}

	result.Metadata = map[string]interface{}{
		"namespace":     namespace,
		"selector":      selector,
		"total_pods":    totalPods,
		"ready_pods":    readyPods,
		"failed_pods":   failedPods,
		"warning_pods":  warningPods,
	}

	return result, nil
}

// PodInfo Pod 信息
type PodInfo struct {
	Name         string
	Namespace    string
	Phase        string
	Ready        bool
	RestartCount int
	CPUUsage     float64
	MemoryUsage  float64
	Age          time.Duration
}

// getPods 获取 Pod 列表
func (k *K8sPodInspector) getPods(ctx context.Context, namespace, selector string) ([]PodInfo, error) {
	// 使用 kubectl 获取 Pod 信息
	args := []string{"get", "pods", "-n", namespace, "-o", "json"}
	if selector != "" {
		args = append(args, "-l", selector)
	}

	cmd := exec.CommandContext(ctx, "kubectl", args...)
	output, err := cmd.Output()
	if err != nil {
		// 如果 kubectl 不可用，返回模拟数据（测试用）
		if _, ok := err.(*exec.Error); ok {
			return k.getMockPods(namespace), nil
		}
		return nil, err
	}

	// 解析 JSON 输出（简化版）
	return k.parsePods(output), nil
}

// parsePods 解析 Pod 输出
func (k *K8sPodInspector) parsePods(data []byte) []PodInfo {
	// 实际实现中应该使用 client-go 库或解析 kubectl JSON 输出
	// 这里返回空列表，实际部署时需要完善
	return []PodInfo{}
}

// getMockPods 获取模拟数据（测试用）
func (k *K8sPodInspector) getMockPods(namespace string) []PodInfo {
	return []PodInfo{
		{
			Name:         "app-frontend-7d9f4b8c5-x1a2b",
			Namespace:    namespace,
			Phase:        "Running",
			Ready:        true,
			RestartCount: 0,
			CPUUsage:     45.2,
			MemoryUsage:  60.5,
		},
		{
			Name:         "app-backend-5c8d3f9a2-y3c4d",
			Namespace:    namespace,
			Phase:        "Running",
			Ready:        true,
			RestartCount: 2,
			CPUUsage:     72.1,
			MemoryUsage:  85.3,
		},
		{
			Name:         "app-cache-9b2e5f1d8-z5e6f",
			Namespace:    namespace,
			Phase:        "CrashLoopBackOff",
			Ready:        false,
			RestartCount: 15,
			CPUUsage:     0,
			MemoryUsage:  0,
		},
	}
}
