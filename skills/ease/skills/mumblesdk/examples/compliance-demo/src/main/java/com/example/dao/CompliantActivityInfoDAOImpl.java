package com.example.dao;

import java.sql.SQLException;
import org.springframework.stereotype.Repository;

/**
 * 合规示例 DAO 实现：
 * - 继承 AbstractSimpleDAO
 * - 所有数据访问方法 throws SQLException
 * - 使用 try-with-resources 管理 MumbleSqlSession
 * - 写操作显式 session.commit()；读操作不 commit
 *
 * 说明：该文件用于静态规则验证示例，非完整可运行实现。
 */
@Repository
public class CompliantActivityInfoDAOImpl extends AbstractSimpleDAO implements ActivityInfoDAO {

  public int insertSelective(ActivityInfoDTO record) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      int rows = mapper.insertSelective(record);
      session.commit();
      return rows;
    }
  }

  public ActivityInfoDTO selectByPrimaryKey(String activityId) throws SQLException {
    try (MumbleSqlSession session = openSession()) {
      ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
      return mapper.selectByPrimaryKey(activityId);
    }
  }
}
