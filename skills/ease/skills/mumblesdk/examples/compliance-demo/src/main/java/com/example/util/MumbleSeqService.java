package com.example.util;

/**
 * 占位的序列服务，用于示例工程静态规则验证与 IDE 侧类型消除。
 * 在真实工程中请替换为 MumbleSDK 提供的序列服务实现。
 */
public final class MumbleSeqService {
  private MumbleSeqService() {}

  /**
   * 返回下一个序列值（占位实现）。
   * @param biz 业务标识
   * @return 占位序列值
   */
  public static String nextValue(String biz) {
    return "SEQ-" + (biz == null ? "UNKNOWN" : biz) + "-000001";
  }
}
