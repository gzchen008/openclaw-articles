import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const TalkSilenceScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const configOpacity = interpolate(frame, [30, 60], [0, 1]);
  const visualOpacity = interpolate(frame, [60, 100], [0, 1]);

  // 模拟声波动画（仅使用 opacity）
  const wave1Opacity = interpolate(frame, [80, 100, 120, 140], [0, 1, 0.3, 1]);
  const wave2Opacity = interpolate(frame, [90, 110, 130, 150], [0, 1, 0.3, 1]);
  const wave3Opacity = interpolate(frame, [100, 120, 140, 160], [0, 1, 0.3, 1]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0a',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'system-ui, sans-serif',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '90%',
          maxWidth: 1400,
        }}
      >
        {/* 标题 */}
        <div
          style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: '#fff',
            opacity: titleOpacity,
            marginBottom: 40,
          }}
        >
          🎙️ Talk 静默检测
        </div>

        {/* 配置代码 */}
        <div
          style={{
            backgroundColor: '#1a1a2e',
            padding: '30px 50px',
            borderRadius: 16,
            opacity: configOpacity,
            marginBottom: 50,
          }}
        >
          <div style={{ fontSize: 24, color: '#8b949e', fontFamily: 'monospace' }}>
            talk:
          </div>
          <div style={{ fontSize: 24, color: '#00ff88', fontFamily: 'monospace', marginLeft: 20 }}>
            silenceTimeoutMs: 2000
          </div>
          <div style={{ fontSize: 20, color: '#6e7681', fontFamily: 'monospace', marginTop: 10 }}>
            # 静默 2 秒后自动发送
          </div>
        </div>

        {/* 可视化：声波效果 */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 20,
            opacity: visualOpacity,
          }}
        >
          {/* 声波条 */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div
              style={{
                width: 8,
                height: 40,
                backgroundColor: '#00d9ff',
                borderRadius: 4,
                opacity: wave1Opacity,
              }}
            />
            <div
              style={{
                width: 8,
                height: 60,
                backgroundColor: '#00d9ff',
                borderRadius: 4,
                opacity: wave2Opacity,
              }}
            />
            <div
              style={{
                width: 8,
                height: 80,
                backgroundColor: '#00d9ff',
                borderRadius: 4,
                opacity: wave3Opacity,
              }}
            />
            <div
              style={{
                width: 8,
                height: 60,
                backgroundColor: '#00d9ff',
                borderRadius: 4,
                opacity: wave2Opacity,
              }}
            />
            <div
              style={{
                width: 8,
                height: 40,
                backgroundColor: '#00d9ff',
                borderRadius: 4,
                opacity: wave1Opacity,
              }}
            />
          </div>

          {/* 箭头 */}
          <div style={{ fontSize: 40, color: '#8b949e' }}>→</div>

          {/* 发送图标 */}
          <div
            style={{
              backgroundColor: '#238636',
              padding: '15px 30px',
              borderRadius: 12,
              display: 'flex',
              alignItems: 'center',
              gap: 12,
            }}
          >
            <span style={{ fontSize: 28 }}>📤</span>
            <span style={{ fontSize: 24, color: '#fff' }}>自动发送</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
