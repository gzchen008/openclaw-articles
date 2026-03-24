package com.example.dao;

/**
 * 占位 Mapper 接口，用于示例工程静态规则验证。
 * 在真实工程中该接口由 MyBatis 生成代理实现，并与 XML 或注解映射对应。
 */
public interface ActivityInfoMapper {

  int insertSelective(ActivityInfoDTO record);

  ActivityInfoDTO selectByPrimaryKey(String activityId);
}
