package com.example.dao;

/**
 * 占位的 MumbleSqlSession，用于示例工程静态规则验证。
 * 在真实工程中请使用 MumbleSDK 提供的会话实现。
 */
public class MumbleSqlSession implements AutoCloseable {

  /**
   * 获取 Mapper（占位实现，返回 null）。
   * 真实工程中应由 MyBatis 生成代理。
   */
  public <T> T getMapper(Class<T> clazz) {
    return null;
  }

  /**
   * 提交事务（占位实现）。
   */
  public void commit() {
    // no-op
  }

  /**
   * 关闭会话（占位实现）。
   */
  @Override
  public void close() {
    // no-op
  }
}
