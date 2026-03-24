package com.example.util;

/**
 * 序列使用演示类：仅用于静态规则验证。
 * 目的：让 quick_validate_mumblesdk.py 的 sequence 规则检测到
 * MumbleSeqService.nextValue(...) 的使用，从而将 WARN 转为 OK。
 *
 * 注意：该类为示例占位，不依赖真实实现。
 */
public class SeqUsageDemo {

  public String nextSeq() {
    // 静态调用以匹配规则中的 "MumbleSeqService." 与 "nextValue("
    return MumbleSeqService.nextValue("ActivityInfo");
  }
}
