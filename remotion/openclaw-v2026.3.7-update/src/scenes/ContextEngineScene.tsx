import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const ContextEngineScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const contentOpacity = interpolate(frame, [30, 60], [0, 1]);
  const highlightOpacity = interpolate(frame, [70, 100], [0, 1]);

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
          🧠 1. Context Engine 插件
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
          <p style={{ marginBottom: 24 }}>✅ 无损记忆，永不丢失信息</p>
          <p style={{ marginBottom: 24 }}>✅ 自定义上下文管理策略</p>
          <p style={{ marginBottom: 24 }}>✅ 第三方插件支持</p>
        </div>

        {/* 底部高亮 */}
        <div
          style={{
            marginTop: 40,
            padding: 32,
            background: 'linear-gradient(135deg, #0366d6 0%, #0056b3 100%)',
            borderRadius: 16,
            opacity: highlightOpacity,
            width: '100%',
            maxWidth: 800,
          }}
        >
          <p style={{ fontSize: 28, color: '#fff', margin: 0, textAlign: 'center' }}>
            💡 插件示例：lossless-claw
          </p>
        </div>
      </div>
    </AbsoluteFill>
  );
};
