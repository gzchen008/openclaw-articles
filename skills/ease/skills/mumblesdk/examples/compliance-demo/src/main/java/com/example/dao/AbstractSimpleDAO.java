package com.example.dao;

/**
 * 占位抽象 DAO 基类，用于示例工程静态规则验证。
 * 在真实工程中请使用 MumbleSDK 提供的 AbstractSimpleDAO。
 */
public abstract class AbstractSimpleDAO {

  /**
   * 打开数据访问会话（占位实现）。
   * 真实工程中请从会话工厂创建。
   */
  protected MumbleSqlSession openSession() {
    return new MumbleSqlSession();
  }
}
