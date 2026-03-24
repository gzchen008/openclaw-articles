import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();

  // 所有元素只使用 opacity 动画，不改变位置
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const versionOpacity = interpolate(frame, [30, 60], [0, 1]);
  const subtitleOpacity = interpolate(frame, [60, 90], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0a',
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: 'system-ui, sans-serif',
      }}
    >
      {/* 背景渐变 */}
      <div
        style={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          background: 'radial-gradient(circle at 50% 50%, #1a1a2e 0%, #0a0a0a 70%)',
        }}
      />

      {/* 内容容器 - 完全居中 */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '90%',
          maxWidth: 960,
          zIndex: 1,
        }}
      >
        {/* 主标题 - 固定位置 */}
        <div
          style={{
            fontSize: 72,
            fontWeight: 'bold',
            color: '#fff',
            opacity: titleOpacity,
            textAlign: 'center',
            marginBottom: 16,
          }}
        >
          OpenClaw
        </div>

        {/* 版本号 - 固定位置 */}
        <div
          style={{
            fontSize: 44,
            fontWeight: 'bold',
            background: 'linear-gradient(135deg, #0366d6 0%, #00d9ff 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            opacity: versionOpacity,
            textAlign: 'center',
            marginBottom: 24,
          }}
        >
          v2026.3.7 更新
        </div>

        {/* 副标题 - 固定位置 */}
        <div
          style={{
            fontSize: 32,
            color: '#8b949e',
            opacity: subtitleOpacity,
            textAlign: 'center',
          }}
        >
          5 个重磅新功能 🚀
        </div>
      </div>

      {/* 装饰性圆圈 - 居中 */}
      <div
        style={{
          position: 'absolute',
          width: 240,
          height: 240,
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(3, 102, 214, 0.2) 0%, transparent 70%)',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 0,
        }}
      />
    </AbsoluteFill>
  );
};
