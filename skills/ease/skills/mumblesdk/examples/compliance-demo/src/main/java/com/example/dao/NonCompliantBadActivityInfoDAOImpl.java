package com.example.dao;

import org.springframework.stereotype.Repository;

/**
 * 非合规示例 DAO 实现：
 * - 未继承 AbstractSimpleDAO（违反强制）
 * - 方法未声明 throws SQLException（违反强制）
 * - 未使用 try-with-resources 管理 MumbleSqlSession（违反强制）
 *
 * 说明：该类用于触发 quick_validate_mumblesdk.py 的 DAO 规则 ERROR，以验证 CI 门禁阻断路径。
 */
@Repository
public class NonCompliantBadActivityInfoDAOImpl implements ActivityInfoDAO {

  public int insertSelective(ActivityInfoDTO record) {
    MumbleSqlSession session = new MumbleSqlSession(); // 非 try-with-resources
    ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
    int rows = mapper.insertSelective(record);
    // 未显式 commit 或关闭（示例中刻意不合规）
    return rows;
  }

  public ActivityInfoDTO selectByPrimaryKey(String activityId) {
    MumbleSqlSession session = new MumbleSqlSession(); // 非 try-with-resources
    ActivityInfoMapper mapper = session.getMapper(ActivityInfoMapper.class);
    return mapper.selectByPrimaryKey(activityId);
  }
}
