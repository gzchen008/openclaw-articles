import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const WebSearchScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const providersOpacity = interpolate(frame, [30, 60], [0, 1]);
  const featuresOpacity = interpolate(frame, [80, 110], [0, 1]);

  const providers = [
    { name: 'Brave Search', color: '#ff5722', emoji: '🦁' },
    { name: 'Perplexity', color: '#20b2aa', emoji: '🔮' },
    { name: 'Tavily', color: '#9c27b0', emoji: '⚡' },
    { name: 'SerpAPI', color: '#2196f3', emoji: '🔍' },
  ];

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0a',
        justifyContent: 'center',      // 垂直居中
        alignItems: 'center',           // 水平居中
        fontFamily: 'system-ui, sans-serif',
      }}
    >
      {/* 内容容器 */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '90%',
          maxWidth: 960,
        }}
      >
        {/* 标题 */}
        <div
          style={{
            fontSize: 48,
            fontWeight: 'bold',
            color: '#fff',
            opacity: titleOpacity,
            marginBottom: 32,
            textAlign: 'center',
          }}
        >
          🔍 5. Web Search 增强
        </div>

        {/* 提供商列表 */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 16,
            width: '100%',
            maxWidth: 800,
            opacity: providersOpacity,
          }}
        >
          {providers.map((provider, index) => (
            <div
              key={index}
              style={{
                padding: 20,
                background: `linear-gradient(135deg, ${provider.color}22 0%, ${provider.color}11 100%)`,
                border: `2px solid ${provider.color}`,
                borderRadius: 12,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 16,
              }}
            >
              <div style={{ fontSize: 40 }}>{provider.emoji}</div>
              <span style={{ fontSize: 28, color: '#fff', fontWeight: 'bold' }}>
                {provider.name}
              </span>
            </div>
          ))}
        </div>

        {/* 功能列表 */}
        <div
          style={{
            marginTop: 32,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 12,
            opacity: featuresOpacity,
          }}
        >
          <div style={{ fontSize: 22, color: '#8b949e' }}>✅ 语言过滤</div>
          <div style={{ fontSize: 22, color: '#8b949e' }}>✅ 地区过滤</div>
          <div style={{ fontSize: 22, color: '#8b949e' }}>✅ 时间过滤</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
