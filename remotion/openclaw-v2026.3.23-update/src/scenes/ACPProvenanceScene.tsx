import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const ACPProvenanceScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const codeOpacity = interpolate(frame, [30, 60], [0, 1]);
  const featuresOpacity = interpolate(frame, [60, 100], [0, 1]);

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
          📋 ACP 来源追踪
        </div>

        {/* 命令行 */}
        <div
          style={{
            backgroundColor: '#1a1a2e',
            padding: '30px 50px',
            borderRadius: 16,
            opacity: codeOpacity,
            marginBottom: 50,
          }}
        >
          <div style={{ fontSize: 28, color: '#8b949e', fontFamily: 'monospace' }}>
            openclaw acp --provenance
          </div>
          <div style={{ fontSize: 24, color: '#00d9ff', fontFamily: 'monospace', marginTop: 10 }}>
            off | meta | meta+receipt
          </div>
        </div>

        {/* 功能点 */}
        <div
          style={{
            display: 'flex',
            gap: 50,
            opacity: featuresOpacity,
          }}
        >
          <FeatureCard
            icon="🔗"
            title="来源元数据"
            desc="保留 ACP 来源上下文"
          />
          <FeatureCard
            icon="🧾"
            title="可见收据"
            desc="注入会话追踪 ID"
          />
          <FeatureCard
            icon="🔍"
            title="可追溯"
            desc="完整操作审计链"
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

const FeatureCard: React.FC<{ icon: string; title: string; desc: string }> = ({
  icon,
  title,
  desc,
}) => (
  <div
    style={{
      backgroundColor: '#161b22',
      padding: '30px 40px',
      borderRadius: 16,
      textAlign: 'center',
      width: 240,
    }}
  >
    <div style={{ fontSize: 48, marginBottom: 16 }}>{icon}</div>
    <div style={{ fontSize: 26, color: '#fff', fontWeight: 'bold', marginBottom: 10 }}>
      {title}
    </div>
    <div style={{ fontSize: 20, color: '#8b949e' }}>{desc}</div>
  </div>
);
