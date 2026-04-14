import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const BackupScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const codeOpacity = interpolate(frame, [30, 60], [0, 1]);
  const featuresOpacity = interpolate(frame, [60, 90], [0, 1]);
  const descOpacity = interpolate(frame, [90, 120], [0, 1]);

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
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '90%',
          maxWidth: 1400,
        }}
      >
        {/* 标题 */}
        <div
          style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: '#fff',
            opacity: titleOpacity,
            marginBottom: 40,
          }}
        >
          📦 CLI 备份系统
        </div>

        {/* 代码示例 */}
        <div
          style={{
            backgroundColor: '#1a1a2e',
            padding: '30px 50px',
            borderRadius: 16,
            opacity: codeOpacity,
            marginBottom: 40,
          }}
        >
          <div style={{ fontSize: 28, color: '#00d9ff', fontFamily: 'monospace' }}>
            openclaw backup create
          </div>
          <div style={{ fontSize: 28, color: '#8b949e', fontFamily: 'monospace', marginTop: 10 }}>
            openclaw backup verify
          </div>
        </div>

        {/* 功能点 */}
        <div
          style={{
            display: 'flex',
            gap: 40,
            opacity: featuresOpacity,
          }}
        >
          <FeatureBox emoji="📁" text="本地归档" />
          <FeatureBox emoji="⚙️" text="配置备份" />
          <FeatureBox emoji="✅" text="完整性验证" />
        </div>

        {/* 描述 */}
        <div
          style={{
            fontSize: 28,
            color: '#8b949e',
            opacity: descOpacity,
            marginTop: 40,
            textAlign: 'center',
          }}
        >
          全新的备份命令让你的 OpenClaw 配置更安全
        </div>
      </div>
    </AbsoluteFill>
  );
};

const FeatureBox: React.FC<{ emoji: string; text: string }> = ({ emoji, text }) => (
  <div
    style={{
      backgroundColor: '#161b22',
      padding: '20px 30px',
      borderRadius: 12,
      display: 'flex',
      alignItems: 'center',
      gap: 12,
    }}
  >
    <span style={{ fontSize: 32 }}>{emoji}</span>
    <span style={{ fontSize: 24, color: '#fff' }}>{text}</span>
  </div>
);
