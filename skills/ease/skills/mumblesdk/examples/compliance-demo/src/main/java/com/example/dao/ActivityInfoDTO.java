package com.example.dao;

import java.time.Instant;

/**
 * 占位 DTO，用于示例工程静态规则验证。
 * 在真实工程中应放置到业务包，并配合校验注解与映射。
 */
public class ActivityInfoDTO {
  private String activityId;
  private String activityName;
  private String status;
  private Integer deleted;
  private Instant createdTime;
  private Instant updatedTime;

  public String getActivityId() { return activityId; }
  public void setActivityId(String activityId) { this.activityId = activityId; }

  public String getActivityName() { return activityName; }
  public void setActivityName(String activityName) { this.activityName = activityName; }

  public String getStatus() { return status; }
  public void setStatus(String status) { this.status = status; }

  public Integer getDeleted() { return deleted; }
  public void setDeleted(Integer deleted) { this.deleted = deleted; }

  public Instant getCreatedTime() { return createdTime; }
  public void setCreatedTime(Instant createdTime) { this.createdTime = createdTime; }

  public Instant getUpdatedTime() { return updatedTime; }
  public void setUpdatedTime(Instant updatedTime) { this.updatedTime = updatedTime; }
}
