package com.example.dao;

import java.sql.SQLException;

/**
 * 占位 DAO 接口，用于示例工程静态规则验证。
 * 在真实工程中请使用对应的业务接口。
 */
public interface ActivityInfoDAO {

  int insertSelective(ActivityInfoDTO record) throws SQLException;

  ActivityInfoDTO selectByPrimaryKey(String activityId) throws SQLException;
}
