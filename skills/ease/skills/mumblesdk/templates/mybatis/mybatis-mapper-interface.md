# MyBatis Mapper 接口模板（强制规范版）

说明
- 本模板提供 MyBatis Mapper 接口与 XML 的规范示例，复制到实际工程后按包名/类名/字段进行调整。
- 强制规范要点：
  1) 接口命名与 XML namespace 必须完全一致；
  2) Mapper 接口的所有方法必须声明 throws SQLException；
  3) XML 必须包含 BaseResultMap 与 Base_Column_List；
  4) 禁止使用 select *；所有参数使用 #{param, jdbcType=...}；
  5) 更新/删除必须具备明确 where 条件；
  6) 时间统一使用 LocalDateTime；DTO/Condition 字段与 JDBC 类型一致。

参考文档
- ease_docs/mybatis-best-practices.md
- mumble-sdk/references/integration-checklist.md

---

## 1) Mapper 接口示例（复制到真实 Java 文件后使用）

```java
package com.yourcompany.yourapp.dao.mapper;

import com.yourcompany.yourapp.pojo.dto.ActivityInfoDTO;
import com.yourcompany.yourapp.pojo.dto.ActivityInfoCondition;
import java.sql.SQLException;
import java.util.List;

/**
 * Mapper 接口：示例表 activity_info
 * 所有方法必须声明 throws SQLException
 */
public interface ActivityInfoMapper {

  // 删除主键（软删除建议通过 update 维护 deleted 字段）
  int deleteByPrimaryKey(String activityId) throws SQLException;

  // 选择性插入（仅非空字段）
  int insertSelective(ActivityInfoDTO record) throws SQLException;

  // 批量插入（注意 JDBC 批量优化与事务边界）
  int insertBatch(List<ActivityInfoDTO> records) throws SQLException;

  // 主键查询（ResultMap 必须使用 BaseResultMap）
  ActivityInfoDTO selectByPrimaryKey(String activityId) throws SQLException;

  // 条件查询（Condition 中仅包含查询字段）
  List<ActivityInfoDTO> selectByCondition(ActivityInfoCondition condition) throws SQLException;

  // 条件计数（用于分页）
  int countByCondition(ActivityInfoCondition condition) throws SQLException;

  // 选择性更新（仅非空字段）
  int updateByPrimaryKeySelective(ActivityInfoDTO record) throws SQLException;

  // 全量更新（慎用；必须具备 where 主键条件）
  int updateByPrimaryKey(ActivityInfoDTO record) throws SQLException;

  // 软删除（示例：更新 deleted=1 并记录删除时间/操作者）
  int softDeleteByPrimaryKey(String activityId) throws SQLException;

  // 自定义查询示例：按状态与创建时间范围查询最近 N 条
  List<ActivityInfoDTO> selectRecentByStatus(
      String status,
      java.time.LocalDateTime startTime,
      java.time.LocalDateTime endTime,
      int limit
  ) throws SQLException;
}
```

---

## 2) DTO 与条件对象示例（占位）

```java
public class ActivityInfoDTO {
  private String activityId;
  private String activityName;
  private String status;
  private java.time.LocalDateTime createdTime;
  private java.time.LocalDateTime updatedTime;
  // ... getters/setters
}

public class ActivityInfoCondition {
  private String status;
  private java.time.LocalDateTime startTime;
  private java.time.LocalDateTime endTime;
  // 分页参数（如使用统一分页组件则替换）
  private Integer offset;
  private Integer pageSize;
  // ... getters/setters
}
```

---

## 3) Mapper XML 片段示例（resources/mapper/ActivityInfoMapper.xml）

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.yourcompany.yourapp.dao.mapper.ActivityInfoMapper">

  <resultMap id="BaseResultMap" type="com.yourcompany.yourapp.pojo.dto.ActivityInfoDTO">
    <id     column="activity_id"   jdbcType="VARCHAR"   property="activityId"/>
    <result column="activity_name" jdbcType="VARCHAR"   property="activityName"/>
    <result column="status"        jdbcType="VARCHAR"   property="status"/>
    <result column="created_time"  jdbcType="TIMESTAMP" property="createdTime"/>
    <result column="updated_time"  jdbcType="TIMESTAMP" property="updatedTime"/>
  </resultMap>

  <sql id="Base_Column_List">
    activity_id, activity_name, status, created_time, updated_time
  </sql>

  <select id="selectByPrimaryKey" resultMap="BaseResultMap">
    SELECT <include refid="Base_Column_List"/>
    FROM activity_info
    WHERE activity_id = #{activityId, jdbcType=VARCHAR}
  </select>

  <select id="selectByCondition" resultMap="BaseResultMap">
    SELECT <include refid="Base_Column_List"/>
    FROM activity_info
    <where>
      <if test="status != null and status != ''">
        status = #{status, jdbcType=VARCHAR}
      </if>
      <if test="startTime != null">
        AND created_time >= #{startTime, jdbcType=TIMESTAMP}
      </if>
      <if test="endTime != null">
        AND created_time <= #{endTime, jdbcType=TIMESTAMP}
      </if>
    </where>
    <if test="offset != null and pageSize != null">
      LIMIT #{pageSize, jdbcType=INTEGER} OFFSET #{offset, jdbcType=INTEGER}
    </if>
  </select>

  <insert id="insertSelective">
    INSERT INTO activity_info
    <trim prefix="(" suffix=")" suffixOverrides=",">
      <if test="activityId != null">activity_id,</if>
      <if test="activityName != null">activity_name,</if>
      <if test="status != null">status,</if>
      <if test="createdTime != null">created_time,</if>
      <if test="updatedTime != null">updated_time,</if>
    </trim>
    VALUES
    <trim prefix="(" suffix=")" suffixOverrides=",">
      <if test="activityId != null">#{activityId, jdbcType=VARCHAR},</if>
      <if test="activityName != null">#{activityName, jdbcType=VARCHAR},</if>
      <if test="status != null">#{status, jdbcType=VARCHAR},</if>
      <if test="createdTime != null">#{createdTime, jdbcType=TIMESTAMP},</if>
      <if test="updatedTime != null">#{updatedTime, jdbcType=TIMESTAMP},</if>
    </trim>
  </insert>

  <update id="updateByPrimaryKeySelective">
    UPDATE activity_info
    <set>
      <if test="activityName != null">activity_name = #{activityName, jdbcType=VARCHAR},</if>
      <if test="status != null">status = #{status, jdbcType=VARCHAR},</if>
      <if test="updatedTime != null">updated_time = #{updatedTime, jdbcType=TIMESTAMP},</if>
    </set>
    WHERE activity_id = #{activityId, jdbcType=VARCHAR}
  </update>

  <update id="softDeleteByPrimaryKey">
    UPDATE activity_info
    SET deleted = 1, updated_time = NOW()
    WHERE activity_id = #{activityId, jdbcType=VARCHAR}
  </update>

</mapper>
```

---

## 4) 质量门提示与脚本联动

- scripts/quick_validate_mumblesdk.py 将检查：
  - 禁止 select *
  - 参数必须声明 jdbcType
  - 必须存在 BaseResultMap 与 Base_Column_List
  - XML 具备 where 条件
- DAO 接口/实现必须遵循：
  - 方法声明 throws SQLException
  - DAO 类继承 AbstractSimpleDAO
  - 使用 MumbleSqlSession 的 try-with-resources

---

## 5) 复制指引

- 在实际工程中创建 Java 源文件（如 src/main/java/.../ActivityInfoMapper.java），将上方示例代码粘贴并根据业务字段调整；
- 在 resources/mapper 下创建 ActivityInfoMapper.xml 并使用上方 XML 片段；
- 配置 MyBatis 扫描路径与 SqlSessionFactory，并遵循企业统一配置与连接池最佳实践。
