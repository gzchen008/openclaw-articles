import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const BraveSearchScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const configOpacity = interpolate(frame, [30, 60], [0, 1]);
  const featuresOpacity = interpolate(frame, [60, 90], [0, 1]);

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
          🔍 Brave 智能搜索增强
        </div>

        {/* 配置代码 */}
        <div
          style={{
            backgroundColor: '#1a1a2e',
            padding: '30px 50px',
            borderRadius: 16,
            opacity: configOpacity,
            marginBottom: 40,
          }}
        >
          <div style={{ fontSize: 24, color: '#8b949e', fontFamily: 'monospace' }}>
            tools:
          </div>
          <div style={{ fontSize: 24, color: '#8b949e', fontFamily: 'monospace', marginLeft: 20 }}>
            web:
          </div>
          <div style={{ fontSize: 24, color: '#8b949e', fontFamily: 'monospace', marginLeft: 40 }}>
            search:
          </div>
          <div style={{ fontSize: 24, color: '#8b949e', fontFamily: 'monospace', marginLeft: 60 }}>
            brave:
          </div>
          <div style={{ fontSize: 24, color: '#00ff88', fontFamily: 'monospace', marginLeft: 80 }}>
            mode: "llm-context"
          </div>
        </div>

        {/* 功能说明 */}
        <div
          style={{
            display: 'flex',
            gap: 60,
            opacity: featuresOpacity,
          }}
        >
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 48, marginBottom: 10 }}>🧠</div>
            <div style={{ fontSize: 24, color: '#fff' }}>LLM Context</div>
            <div style={{ fontSize: 20, color: '#8b949e', marginTop: 8 }}>智能摘要提取</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 48, marginBottom: 10 }}>📊</div>
            <div style={{ fontSize: 24, color: '#fff' }}>来源元数据</div>
            <div style={{ fontSize: 20, color: '#8b949e', marginTop: 8 }}>精确溯源</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 48, marginBottom: 10 }}>⚡</div>
            <div style={{ fontSize: 24, color: '#fff' }}>更精准</div>
            <div style={{ fontSize: 20, color: '#8b949e', marginTop: 8 }}>AI 友好格式</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
