import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const EndingScene: React.FC = () => {
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
          fontSize: 60,
          fontWeight: 'bold',
          color: '#e53935',
          marginBottom: 30,
        }}>
          立即升级
        </div>
        <div style={{
          fontSize: 40,
          color: '#ffffff',
          marginBottom: 20,
        }}>
          npm install -g openclaw@latest
        </div>
        <div style={{
          fontSize: 32,
          color: '#9e9e9e',
        }}>
          github.com/openclaw/openclaw
        </div>
      </div>
    </AbsoluteFill>
  );
};
