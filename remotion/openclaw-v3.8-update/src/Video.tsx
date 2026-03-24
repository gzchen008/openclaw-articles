import React from 'react';
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame } from 'remotion';

// 封面场景
const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [60, 90], [1, 0], { extrapolateRight: 'clamp' });
  const subtitleOpacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', backgroundColor: '#0a0a0a' }}>
      <div style={{ opacity: opacity * fadeOut, textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ fontSize: 72, fontWeight: 'bold', color: '#4CAF50', marginBottom: 40, textAlign: 'center', lineHeight: 1.3 }}>
          OpenClaw<br/>v2026.3.8
        </div>
        <div style={{ fontSize: 36, color: '#fff', opacity: subtitleOpacity, textAlign: 'center', lineHeight: 1.6 }}>
          5 大新功能 + 多项 Bug 修复
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 痛点场景
const PainPointScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const text1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const text2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const text3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 48, fontWeight: 'bold', color: '#2196F3', opacity: titleOpacity, marginBottom: 60, textAlign: 'center' }}>
          🆕 本次更新亮点
        </div>
        <div style={{ fontSize: 28, color: '#fff', opacity: text1Opacity, marginBottom: 32, textAlign: 'center', lineHeight: 1.6 }}>
          ✅ CLI 备份命令（全新）
        </div>
        <div style={{ fontSize: 28, color: '#fff', opacity: text2Opacity, marginBottom: 32, textAlign: 'center', lineHeight: 1.6 }}>
          ✅ Talk 静音超时配置
        </div>
        <div style={{ fontSize: 28, color: '#fff', opacity: text3Opacity, textAlign: 'center', lineHeight: 1.6 }}>
          ✅ Brave 搜索 LLM 增强模式
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 概念场景
const ConceptScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const box1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const box2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const box3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 60, textAlign: 'center' }}>
          💾 CLI 备份命令
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', opacity: box1Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 12 }}>创建备份</div>
          <div style={{ fontFamily: 'monospace', fontSize: 20, color: '#ccc' }}>openclaw backup create</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', opacity: box2Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 12 }}>仅备份配置</div>
          <div style={{ fontFamily: 'monospace', fontSize: 20, color: '#ccc' }}>openclaw backup create --only-config</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, width: '100%', opacity: box3Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 12 }}>验证备份</div>
          <div style={{ fontFamily: 'monospace', fontSize: 20, color: '#ccc' }}>openclaw backup verify</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 方案对比场景
const SolutionsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const box1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const box2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const box3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          🎤 Talk 静音超时
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', borderLeft: '4px solid #4CAF50', opacity: box1Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 8 }}>配置方式</div>
          <div style={{ fontFamily: 'monospace', fontSize: 18, color: '#ccc' }}>{"{\"talk\": {\"silenceTimeoutMs\": 2000}}"}</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', borderLeft: '4px solid #2196F3', opacity: box2Opacity }}>
          <div style={{ fontSize: 24, color: '#2196F3', marginBottom: 8 }}>默认值</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>各平台不同，现在可自定义</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, width: '100%', borderLeft: '4px solid #9C27B0', opacity: box3Opacity }}>
          <div style={{ fontSize: 24, color: '#9C27B0', marginBottom: 8 }}>效果</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>静音 2 秒后自动发送语音转文字</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 性能对比场景
const ComparisonScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const row1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const row2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const row3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          🔍 Brave 搜索 LLM 模式
        </div>
        <div style={{ display: 'flex', width: '100%', marginBottom: 24, opacity: row1Opacity }}>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, marginRight: 12 }}>
            <div style={{ fontSize: 20, color: '#ff6b6b', marginBottom: 8 }}>❌ 普通搜索</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>仅返回链接列表</div>
          </div>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, borderLeft: '3px solid #4CAF50' }}>
            <div style={{ fontSize: 20, color: '#4CAF50', marginBottom: 8 }}>✅ LLM 模式</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>结构化摘要 + 来源</div>
          </div>
        </div>
        <div style={{ display: 'flex', width: '100%', marginBottom: 24, opacity: row2Opacity }}>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, marginRight: 12 }}>
            <div style={{ fontSize: 20, color: '#ff6b6b', marginBottom: 8 }}>❌ 普通搜索</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>需要手动提取信息</div>
          </div>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, borderLeft: '3px solid #4CAF50' }}>
            <div style={{ fontSize: 20, color: '#4CAF50', marginBottom: 8 }}>✅ LLM 模式</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>AI 直接消费</div>
          </div>
        </div>
        <div style={{ display: 'flex', width: '100%', opacity: row3Opacity }}>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, marginRight: 12 }}>
            <div style={{ fontSize: 20, color: '#ff6b6b', marginBottom: 8 }}>❌ 普通搜索</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>无元数据</div>
          </div>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, borderLeft: '3px solid #4CAF50' }}>
            <div style={{ fontSize: 20, color: '#4CAF50', marginBottom: 8 }}>✅ LLM 模式</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>完整来源追溯</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 代码示例场景
const CodeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const code1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const code2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          🛠️ 其他新功能
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 28, borderRadius: 16, width: '100%', opacity: code1Opacity, marginBottom: 24 }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 12 }}>ACP 来源追踪</div>
          <div style={{ fontFamily: 'monospace', fontSize: 18, color: '#9CDCFE', lineHeight: 1.8 }}>
            openclaw acp --provenance meta+receipt
          </div>
          <div style={{ fontSize: 16, color: '#999', marginTop: 8 }}>保留会话追踪 ID</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 28, borderRadius: 16, width: '100%', opacity: code2Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 12 }}>macOS 远程网关</div>
          <div style={{ fontSize: 18, color: '#ccc', lineHeight: 1.8 }}>
            • 新增远程网关 Token 字段<br/>
            • 改善远程模式配置体验
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 行动号召场景
const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const step1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const step2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const step3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          🎯 如何升级？
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', opacity: step1Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 8 }}>1️⃣ npm 升级</div>
          <div style={{ fontFamily: 'monospace', fontSize: 20, color: '#ccc' }}>npm update -g openclaw</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', opacity: step2Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 8 }}>2️⃣ Homebrew 升级</div>
          <div style={{ fontFamily: 'monospace', fontSize: 20, color: '#ccc' }}>brew upgrade openclaw</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, width: '100%', opacity: step3Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 8 }}>3️⃣ 检查版本</div>
          <div style={{ fontFamily: 'monospace', fontSize: 20, color: '#ccc' }}>openclaw --version</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 主视频组件
export const OpenClawUpdate: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {/* 封面场景：0-90帧（3秒） */}
      <Sequence from={0} durationInFrames={90}>
        <CoverScene />
      </Sequence>

      {/* 痛点场景：90-240帧（5秒） */}
      <Sequence from={90} durationInFrames={150}>
        <PainPointScene />
      </Sequence>

      {/* 概念场景：240-390帧（5秒） */}
      <Sequence from={240} durationInFrames={150}>
        <ConceptScene />
      </Sequence>

      {/* 方案对比场景：390-540帧（5秒） */}
      <Sequence from={390} durationInFrames={150}>
        <SolutionsScene />
      </Sequence>

      {/* 性能对比场景：540-690帧（5秒） */}
      <Sequence from={540} durationInFrames={150}>
        <ComparisonScene />
      </Sequence>

      {/* 代码示例场景：690-840帧（5秒） */}
      <Sequence from={690} durationInFrames={150}>
        <CodeScene />
      </Sequence>

      {/* 行动号召场景：840-990帧（5秒） */}
      <Sequence from={840} durationInFrames={150}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
