import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [60, 90], [1, 0], { extrapolateLeft: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0a',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 48,
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
          maxWidth: 960,
          opacity: opacity * fadeOut,
        }}
      >
        {/* emoji */}
        <div
          style={{
            fontSize: 96,
            marginBottom: 32,
            opacity: interpolate(frame, [20, 50], [0, 1], { extrapolateRight: 'clamp' }),
          }}
        >
          🏢
        </div>

        {/* 主标题 */}
        <div
          style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: '#fff',
            textAlign: 'center',
            marginBottom: 24,
            lineHeight: 1.2,
            opacity: interpolate(frame, [30, 60], [0, 1], { extrapolateRight: 'clamp' }),
          }}
        >
          如果 OpenClaw 是员工
        </div>

        <div
          style={{
            fontSize: 56,
            fontWeight: 'bold',
            color: '#4CAF50',
            textAlign: 'center',
            marginBottom: 32,
            lineHeight: 1.2,
            opacity: interpolate(frame, [35, 65], [0, 1], { extrapolateRight: 'clamp' }),
          }}
        >
          Paperclip 就是公司
        </div>

        {/* 副标题 */}
        <div
          style={{
            fontSize: 28,
            color: '#ccc',
            textAlign: 'center',
            opacity: interpolate(frame, [40, 70], [0, 1], { extrapolateRight: 'clamp' }),
          }}
        >
          24.8K Stars • AI Agent 编排平台
        </div>
      </div>
    </AbsoluteFill>
  );
};
