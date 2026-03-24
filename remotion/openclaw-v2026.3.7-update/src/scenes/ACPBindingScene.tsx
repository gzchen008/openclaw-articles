import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const ACPBindingScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const contentOpacity = interpolate(frame, [30, 60], [0, 1]);
  const codeOpacity = interpolate(frame, [70, 100], [0, 1]);

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
            marginBottom: 40,
            textAlign: 'center',
          }}
        >
          🔗 2. ACP 持久化绑定
        </div>

        {/* 主要内容 */}
        <div
          style={{
            fontSize: 28,
            color: '#e6edf3',
            opacity: contentOpacity,
            lineHeight: 2,
            textAlign: 'center',
          }}
        >
          <p style={{ marginBottom: 24 }}>✅ Discord 频道绑定重启后保留</p>
          <p style={{ marginBottom: 24 }}>✅ Telegram 话题绑定重启后保留</p>
          <p style={{ marginBottom: 24 }}>✅ 多账号管理一致性</p>
        </div>

        {/* 代码示例 */}
        <div
          style={{
            marginTop: 40,
            padding: 32,
            background: '#161b22',
            borderRadius: 16,
            border: '2px solid #30363d',
            opacity: codeOpacity,
            width: '100%',
            maxWidth: 800,
          }}
        >
          <p style={{ fontSize: 28, color: '#8b949e', margin: 0, fontFamily: 'monospace', textAlign: 'center' }}>
            /acp spawn --thread here
          </p>
        </div>
      </div>
    </AbsoluteFill>
  );
};
