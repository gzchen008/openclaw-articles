import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const CSPScene: React.FC = () => {
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
          🔒 CSP 安全加固
        </div>
      </div>
      <div style={{ opacity: contentOpacity }}>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • 自动计算 SHA-256 哈希值
        </div>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • 仅允许经过验证的脚本
        </div>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • 完全符合现代安全标准
        </div>
      </div>
    </AbsoluteFill>
  );
};
