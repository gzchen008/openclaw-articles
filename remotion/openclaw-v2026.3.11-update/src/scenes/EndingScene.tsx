import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const EndingScene: React.FC = () => {
  const frame = useCurrentFrame();

  const logoOpacity = interpolate(frame, [0, 20], [0, 1]);
  const versionOpacity = interpolate(frame, [20, 40], [0, 1]);
  const ctaOpacity = interpolate(frame, [40, 60], [0, 1]);
  const linkOpacity = interpolate(frame, [60, 80], [0, 1]);

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
          position: 'absolute',
          width: '100%',
          height: '100%',
          background: 'radial-gradient(circle at 50% 50%, #1a1a2e 0%, #0a0a0a 70%)',
        }}
      />

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1,
        }}
      >
        {/* Logo */}
        <div
          style={{
            fontSize: 72,
            fontWeight: 'bold',
            color: '#fff',
            opacity: logoOpacity,
            marginBottom: 20,
          }}
        >
          OpenClaw
        </div>

        {/* 版本 */}
        <div
          style={{
            fontSize: 40,
            background: 'linear-gradient(135deg, #0366d6 0%, #00d9ff 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            opacity: versionOpacity,
            marginBottom: 30,
          }}
        >
          v2026.3.8
        </div>

        {/* 更新命令 */}
        <div
          style={{
            backgroundColor: '#238636',
            padding: '20px 50px',
            borderRadius: 12,
            opacity: ctaOpacity,
            marginBottom: 30,
          }}
        >
          <span style={{ fontSize: 28, color: '#fff', fontFamily: 'monospace' }}>
            npm update -g openclaw
          </span>
        </div>

        {/* 链接 */}
        <div
          style={{
            fontSize: 24,
            color: '#8b949e',
            opacity: linkOpacity,
          }}
        >
          github.com/openclaw/openclaw
        </div>

        {/* 装饰 */}
        <div
          style={{
            position: 'absolute',
            width: 400,
            height: 400,
            borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(3, 102, 214, 0.15) 0%, transparent 70%)',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            zIndex: 0,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
