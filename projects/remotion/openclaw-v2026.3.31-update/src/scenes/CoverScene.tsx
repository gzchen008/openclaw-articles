import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0a',
        justifyContent: 'center',
        alignItems: 'center',
        opacity,
      }}
    >
      <div style={{ textAlign: 'center' }}>
        <div style={{
          fontSize: 80,
          fontWeight: 'bold',
          color: '#e53935',
          marginBottom: 20,
        }}>
          OpenClaw
        </div>
        <div style={{
          fontSize: 60,
          color: '#ffffff',
          marginBottom: 30,
        }}>
          2026.3.31
        </div>
        <div style={{
          fontSize: 40,
          color: '#9e9e9e',
        }}>
          重大更新发布
        </div>
      </div>
    </AbsoluteFill>
  );
};
