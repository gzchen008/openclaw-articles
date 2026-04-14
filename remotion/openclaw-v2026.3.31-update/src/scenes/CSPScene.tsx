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
          🚀 新功能特性
        </div>
      </div>
      <div style={{ opacity: contentOpacity }}>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • QQ Bot 频道支持
        </div>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • Matrix 历史记录支持
        </div>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • MCP 远程服务器支持
        </div>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • WhatsApp 表情反应支持
        </div>
        <div style={{ fontSize: 36, color: '#ffffff', marginBottom: 30 }}>
          • LINE 媒体外发增强
        </div>
      </div>
    </AbsoluteFill>
  );
};
