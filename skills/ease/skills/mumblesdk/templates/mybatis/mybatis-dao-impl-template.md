# MyBatis DAO 实现模板（详版）

目的：提供符合 MumbleSDK 规范的 DAO 实现范式，确保：
- DAO 实现类继承 `AbstractSimpleDAO`
- 数据访问使用 `try-with-resources` 包裹 `MumbleSqlSession`
- 接口与实现方法统一声明 `throws SQLException`
- 事务边界在服务层（`@Transactional`），DAO 仅承担数据访问

参考：接口方法签名示例见 `mumble-sdk/templates/mybatis/mybatis-mapper-interface.md`。

---

## 1) DAO 接口示例（简版）

```java
package com.yourcompany.yourapp.dao;

import java.sql.SQLException;
import java.time.LocalDateTime;
import java.util.List;
import com.yourcompany.yourapp.pojo.dto.ActivityInfoDTO;
import com.yourcompany.yourapp.pojo.condition.ActivityInfoCondition;

public interface ActivityInfoDAO {
  int deleteByPrimaryKey(String activityId) throws SQLException;
  int insertSelective(ActivityInfoDTO record) throws SQLException;
  int insertBatch(List<ActivityInfoDTO> records) throws SQLException;
  ActivityInfoDTO selectByPrimaryKey(String activityId) throws SQLException;
  List<ActivityInfoDTO> selectByCondition(ActivityInfoCondition condition) throws SQLException;
  int countByCondition(ActivityInfoCondition condition) throws SQLException;
  int updateByPrimaryKeySelective(ActivityInfoDTO record) throws SQLException;
  int updateByPrimaryKey(ActivityInfoDTO record) throws SQLException;
  int softDeleteByPrimaryKey(String activityId) throws SQLException;
  List<ActivityInfoDTO> selectRecentByStatus(String status, LocalDateTime startTime, LocalDateTime endTime, int limit) throws SQLException;
}
```

关键点：
- 所有方法必须显式 `throws SQLException`（脚本将作为 ERROR 项校验）
- 条件与分页参数建议封装为 `Condition`/`Query` DTO

---

## 2) DAO 实现示例（符合 MumbleSDK 规范）

```java
package com.yourcompany.yourapp.dao.impl;

import java.sql.SQLException;
import java.time.LocalDateTime;
import java.util.List;

import org.springframework.stereotype.Repository;

// MumbleSDK 基础类与会话类型（按企业坐标导入）
import cn.webank.mumble.persistence.AbstractSimpleDAO;
import cn.webank.mumble.persistence.MumbleSqlSession;

import com.yourcompany.yourapp.dao.ActivityInfoDAO;
import com.yourcompany.yourapp.mapper.ActivityInfoMapper;
import com.yourcompany.yourapp.pojo.dto.ActivityInfoDTO;
import com.yourcompany.yourapp.pojo.condition.ActivityInfoCondition;

/**
 * 说明：
 * - 继承 AbstractSimpleDAO，使用其提供的 openSession()/getDataSource() 等基础能力
 * - 所有写操作在成功时显式 commit()
 * - 通过 try-with-resources 自动关闭 MumbleSqlSession
 * - 事务边界在 Service 层（@Transactional），DAO 不直接控制事务
 */
@Repository
public class ActivityInfoDAOImpl extends AbstractSimpleDAO implements ActivityInfoDAO {

  @Override
  public int deleteByPrimaryKey(String activityId) throws SQLException {
    try (MumbleSqlSession session = openSession()) { // try-with-resources 包裹会话
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      int rows = mapper.deleteByPrimaryKey(activityId);
      session.commit();
      return rows;
    }
  }

  @Override
  public int insertSelective(ActivityInfoDTO record) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      int rows = mapper.insertSelective(record);
      session.commit();
      return rows;
    }
  }

  @Override
  public int insertBatch(List<ActivityInfoDTO> records) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      int total = mapper.insertBatch(records);
      session.commit();
      return total;
    }
  }

  @Override
  public ActivityInfoDTO selectByPrimaryKey(String activityId) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      return mapper.selectByPrimaryKey(activityId);
    }
  }

  @Override
  public List<ActivityInfoDTO> selectByCondition(ActivityInfoCondition condition) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      return mapper.selectByCondition(condition);
    }
  }

  @Override
  public int countByCondition(ActivityInfoCondition condition) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      return mapper.countByCondition(condition);
    }
  }

  @Override
  public int updateByPrimaryKeySelective(ActivityInfoDTO record) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      int rows = mapper.updateByPrimaryKeySelective(record);
      session.commit();
      return rows;
    }
  }

  @Override
  public int updateByPrimaryKey(ActivityInfoDTO record) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      int rows = mapper.updateByPrimaryKey(record);
      session.commit();
      return rows;
    }
  }

  @Override
  public int softDeleteByPrimaryKey(String activityId) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      int rows = mapper.softDeleteByPrimaryKey(activityId);
      session.commit();
      return rows;
    }
  }

  @Override
  public List<ActivityInfoDTO> selectRecentByStatus(String status, LocalDateTime startTime, LocalDateTime endTime, int limit) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      return mapper.selectRecentByStatus(status, startTime, endTime, limit);
    }
  }
}
```

要点：
- `extends AbstractSimpleDAO` 与 `try (MumbleSqlSession session = openSession()) { ... }` 是强制项（脚本 ERROR）
- 写操作需要 `session.commit()`；读操作不需要 commit
- DAO 不应抛出业务异常，业务异常由 Service 层统一转换与处理
- Mapper 方法的入参/出参类型与 XML 映射需严格对齐（BaseResultMap/Base_Column_List）

---

## 3) 设计注意事项与建议

- 接口与实现统一 throws SQLException：便于在 Service 层 `@Transactional` 边界统一处理异常与回滚策略。
- 严禁在 XML 中使用 `select *`；所有参数使用 `#{..., jdbcType=...}` 并通过 `where`/`<where>` 明确条件。
- 更新语句优先使用选择性更新（`<set>` 动态列）；删除优先软删除（保留审计字段）。
- 批量插入时使用 `<foreach>` 并控制批次大小，避免超大 SQL。
- 与 MumbleSDK 规范的集成要点：日志 MDC 包含 `bizSeqNo`/`txnSeqNo`；服务层在 `finally` 清理 `MumbleContextUtil`；控制器严禁使用 `@Transactional`。

---

## 4) 相关模板与链接

- Mapper 接口详版示例：`mumble-sdk/templates/mybatis/mybatis-mapper-interface.md`
- Mapper XML 模板：`mumble-sdk/templates/mybatis/mybatis-mapper-xml-template.xml`
- 质量门与校验脚本：`mumble-sdk/assets/quality-gates.yml`、`mumble-sdk/scripts/quick_validate_mumblesdk.py`

复制后请根据项目包名与依赖坐标调整 import 与类型声明。确保与实体 DTO/Condition/XML 映射严格一致，以通过静态规则与 CI 质量门的校验。
