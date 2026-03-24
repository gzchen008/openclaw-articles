import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const TelegramTopicScene: React.FC = () => {
  const frame = useCurrentFrame();

  // 所有元素只使用 opacity 动画，不改变位置
  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const card1Opacity = interpolate(frame, [30, 50], [0, 1]);
  const card2Opacity = interpolate(frame, [50, 70], [0, 1]);
  const card3Opacity = interpolate(frame, [70, 90], [0, 1]);
  const footerOpacity = interpolate(frame, [100, 120], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0a',
        justifyContent: 'center',
        alignItems: 'center',
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
        {/* 标题 - 固定位置 */}
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
          📱 3. Telegram 话题路由
        </div>

        {/* 卡片容器 - 纵向排列 */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 20,
            width: '100%',
            maxWidth: 800,
          }}
        >
          {/* 卡片1 - 固定位置 */}
          <div
            style={{
              padding: 32,
              background: 'linear-gradient(135deg, #238636 0%, #1a7f37 100%)',
              borderRadius: 16,
              opacity: card1Opacity,
            }}
          >
            <div style={{ fontSize: 28, color: '#fff', marginBottom: 8, fontWeight: 'bold', textAlign: 'center' }}>
              #技术问答
            </div>
            <div style={{ fontSize: 20, color: '#c9d1d9', textAlign: 'center' }}>
              coding-expert • 专注代码
            </div>
          </div>

          {/* 卡片2 - 固定位置 */}
          <div
            style={{
              padding: 32,
              background: 'linear-gradient(135deg, #0366d6 0%, #0056b3 100%)',
              borderRadius: 16,
              opacity: card2Opacity,
            }}
          >
            <div style={{ fontSize: 28, color: '#fff', marginBottom: 8, fontWeight: 'bold', textAlign: 'center' }}>
              #闲聊
            </div>
            <div style={{ fontSize: 20, color: '#c9d1d9', textAlign: 'center' }}>
              friendly-assistant • 轻松对话
            </div>
          </div>

          {/* 卡片3 - 固定位置 */}
          <div
            style={{
              padding: 32,
              background: 'linear-gradient(135deg, #8957e5 0%, #6e40c9 100%)',
              borderRadius: 16,
              opacity: card3Opacity,
            }}
          >
            <div style={{ fontSize: 28, color: '#fff', marginBottom: 8, fontWeight: 'bold', textAlign: 'center' }}>
              #工作
            </div>
            <div style={{ fontSize: 20, color: '#c9d1d9', textAlign: 'center' }}>
              task-manager • 任务管理
            </div>
          </div>
        </div>

        {/* 底部说明 - 固定位置 */}
        <div
          style={{
            marginTop: 32,
            fontSize: 28,
            color: '#8b949e',
            opacity: footerOpacity,
            textAlign: 'center',
          }}
        >
          💡 每个话题专属 Agent
        </div>
      </div>
    </AbsoluteFill>
  );
};
