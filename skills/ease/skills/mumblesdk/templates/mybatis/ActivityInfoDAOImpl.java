/*
MumbleSDK 模板占位：MyBatis DAO 实现（强制规范版）

说明：
- 为避免 IDE/语言服务将模板示例当作真实 Java 源解析导致报错，本 .java 文件仅保留占位与指引。
- 完整可复制的模板示例代码如下方代码块所示；复制到实际工程后，按包名/类名/字段进行调整。

强制规范要点（DAO/Mapper/XML 三件套）：
1) Mapper 接口的所有方法必须声明 throws SQLException；
2) DAO 实现类必须继承 AbstractSimpleDAO，并通过 try-with-resources 管理 MumbleSqlSession；
3) DAO 实现调用 session.getMapper(YourMapper.class) 委托执行；
4) XML 必须包含 BaseResultMap 与 Base_Column_List；禁止 select *；参数必须 #{..., jdbcType=...}；
5) 更新/删除必须具备明确 where 条件；insertSelective/批量插入/选择性更新/软删除建议提供。

参考文档：
- ease_docs/mybatis-best-practices.md
- mumble-sdk/references/integration-checklist.md
- mumble-sdk/templates/mybatis/mybatis-mapper-interface.md
- mumble-sdk/templates/mybatis/mybatis-mapper-xml-template.xml（建议名称，需在实际工程创建）

------------------------------------------------------------
DAO 实现示例（复制到真实 Java 文件后使用）
------------------------------------------------------------
```java
package com.yourcompany.yourapp.dao.impl;

import com.yourcompany.yourapp.dao.mapper.ActivityInfoMapper;
import com.yourcompany.yourapp.pojo.dto.ActivityInfoDTO;
import com.yourcompany.yourapp.pojo.dto.ActivityInfoCondition;
import cn.webank.mumble.sdk.mybatis.AbstractSimpleDAO;
import cn.webank.mumble.sdk.mybatis.MumbleSqlSession;
import org.springframework.stereotype.Repository;

import java.sql.SQLException;
import java.util.List;

/**
 * DAO 实现：必须继承 AbstractSimpleDAO；使用 try-with-resources 管理 MumbleSqlSession；
 * 所有方法声明 throws SQLException，并委托给 Mapper。
 */
@Repository
public class ActivityInfoDAOImpl extends AbstractSimpleDAO implements ActivityInfoMapper {

  @Override
  public int deleteByPrimaryKey(String activityId) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class).deleteByPrimaryKey(activityId);
    }
  }

  @Override
  public int insertSelective(ActivityInfoDTO record) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class).insertSelective(record);
    }
  }

  @Override
  public int insertBatch(List<ActivityInfoDTO> records) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class).insertBatch(records);
    }
  }

  @Override
  public ActivityInfoDTO selectByPrimaryKey(String activityId) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class).selectByPrimaryKey(activityId);
    }
  }

  @Override
  public List<ActivityInfoDTO> selectByCondition(ActivityInfoCondition condition) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class).selectByCondition(condition);
    }
  }

  @Override
  public int countByCondition(ActivityInfoCondition condition) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class).countByCondition(condition);
    }
  }

  @Override
  public int updateByPrimaryKeySelective(ActivityInfoDTO record) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class).updateByPrimaryKeySelective(record);
    }
  }

  @Override
  public int updateByPrimaryKey(ActivityInfoDTO record) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class).updateByPrimaryKey(record);
    }
  }

  @Override
  public int softDeleteByPrimaryKey(String activityId) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class).softDeleteByPrimaryKey(activityId);
    }
  }

  @Override
  public List<ActivityInfoDTO> selectRecentByStatus(
      String status,
      java.time.LocalDateTime startTime,
      java.time.LocalDateTime endTime,
      int limit
  ) throws SQLException {
    try (MumbleSqlSession session = getSession()) {
      return session.getMapper(ActivityInfoMapper.class)
          .selectRecentByStatus(status, startTime, endTime, limit);
    }
  }
}
```

使用提示：
- 事务边界建议在 Service 层（@Transactional）管理；DAO 层仅负责数据访问委托与 Session 生命周期；避免在 Controller 层使用 @Transactional（见 MumbleSDK 规范）。
- XML 中确保 BaseResultMap 与 Base_Column_List 一致；所有 #{...} 参数声明 jdbcType；避免 select *；更新/删除具备 where 条件。
- 配合 scripts/quick_validate_mumblesdk.py：DAO 必须继承 AbstractSimpleDAO、方法 throws SQLException、try-with-resources 使用 MumbleSqlSession，这些为 ERROR 级检查项。
*/
