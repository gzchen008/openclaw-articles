import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const globalOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  const quickStartOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateRight: 'clamp' });
  const githubOpacity = interpolate(frame, [80, 110], [0, 1], { extrapolateRight: 'clamp' });
  const finalOpacity = interpolate(frame, [130, 160], [0, 1], { extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [220, 270], [1, 0], { extrapolateLeft: 'clamp' });

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
          opacity: globalOpacity * fadeOut,
        }}
      >
        {/* 快速开始 */}
        <div
          style={{
            backgroundColor: '#1a1a1a',
            padding: 24,
            borderRadius: 12,
            marginBottom: 48,
            opacity: quickStartOpacity,
            width: '100%',
          }}
        >
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 12 }}>快速开始</div>
          <div
            style={{
              fontSize: 20,
              color: '#fff',
              fontFamily: 'monospace',
              textAlign: 'center',
              wordBreak: 'break-all',
            }}
          >
            npx paperclipai onboard --yes
          </div>
        </div>

        {/* GitHub */}
        <div
          style={{
            opacity: githubOpacity,
            marginBottom: 48,
          }}
        >
          <div style={{ fontSize: 48, marginBottom: 16 }}>🔗</div>
          <div style={{ fontSize: 24, color: '#0366d6', textAlign: 'center' }}>
            github.com/paperclipai/paperclip
          </div>
        </div>

        {/* 底部文字 */}
        <div
          style={{
            opacity: finalOpacity,
            textAlign: 'center',
            fontSize: 22,
            color: '#ccc',
          }}
        >
          <div style={{ marginBottom: 16 }}>如果觉得有用</div>
          <div style={{ fontSize: 28, color: '#fff' }}>点个"在看"吧 👇</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
