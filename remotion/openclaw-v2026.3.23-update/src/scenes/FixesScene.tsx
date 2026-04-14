import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const FixesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const contentOpacity = interpolate(frame, [30, 50], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0a',
        padding: 80,
        opacity: interpolate(frame, [0, 15], [0, 1]),
      }}
    >
      <div style={{ opacity: titleOpacity, marginBottom: 60 }}>
        <div style={{ fontSize: 64, fontWeight: 'bold', color: '#e53935' }}>
          📦 50+ 项修复
        </div>
      </div>
      <div style={{ opacity: contentOpacity }}>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • Auth / Plugins / CLI 稳定性
        </div>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • Telegram / Discord / LINE 修复
        </div>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • Browser / Gateway 优化
        </div>
      </div>
    </AbsoluteFill>
  );
};
