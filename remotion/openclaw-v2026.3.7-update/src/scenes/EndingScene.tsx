import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const EndingScene: React.FC = () => {
  const frame = useCurrentFrame();

  // 所有元素只使用 opacity 动画，不改变位置
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const codeOpacity = interpolate(frame, [40, 70], [0, 1]);
  const link1Opacity = interpolate(frame, [80, 100], [0, 1]);
  const link2Opacity = interpolate(frame, [100, 120], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%)',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'system-ui, sans-serif',
      }}
    >
      {/* 内容容器 */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '90%',
          maxWidth: 960,
        }}
      >
        {/* 主标题 - 固定位置，只淡入 */}
        <div
          style={{
            fontSize: 64,
            fontWeight: 'bold',
            background: 'linear-gradient(135deg, #0366d6 0%, #00d9ff 50%, #0366d6 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            textAlign: 'center',
            opacity: titleOpacity,
            marginBottom: 32,
          }}
        >
          🚀 立即升级
        </div>

        {/* 命令框 - 固定位置，只淡入 */}
        <div
          style={{
            padding: '24px 48px',
            background: '#161b22',
            borderRadius: 16,
            border: '3px solid #0366d6',
            opacity: codeOpacity,
            boxShadow: '0 0 40px rgba(3, 102, 214, 0.3)',
          }}
        >
          <p
            style={{
              fontSize: 26,
              color: '#58a6ff',
              margin: 0,
              fontFamily: 'monospace',
              fontWeight: 'bold',
              textAlign: 'center',
            }}
          >
            npm install -g openclaw@latest
          </p>
        </div>

        {/* 链接 - 固定位置，只淡入 */}
        <div
          style={{
            marginTop: 40,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 12,
          }}
        >
          <div
            style={{
              fontSize: 22,
              color: '#8b949e',
              textAlign: 'center',
              opacity: link1Opacity,
            }}
          >
            📖 docs.openclaw.ai
          </div>
          <div
            style={{
              fontSize: 22,
              color: '#8b949e',
              textAlign: 'center',
              opacity: link2Opacity,
            }}
          >
            💬 discord.com/invite/clawd
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
