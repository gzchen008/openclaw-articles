import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const PainPointScene: React.FC = () => {
  const frame = useCurrentFrame();
  const globalOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  const painPoints = [
    { icon: '🤯', text: '20个 Claude Code 终端混乱', delay: 20 },
    { icon: '📝', text: '手动收集上下文太烦', delay: 35 },
    { icon: '💸', text: 'Agent 疯狂烧钱', delay: 50 },
    { icon: '⏰', text: '定时任务需要手动触发', delay: 65 },
  ];

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
        }}
      >
        {/* 标题 */}
        <div
          style={{
            fontSize: 48,
            fontWeight: 'bold',
            color: '#ff6b6b',
            textAlign: 'center',
            marginBottom: 48,
            opacity: globalOpacity,
          }}
        >
          痛点：AI Agent 太多了
        </div>

        {/* 痛点列表 */}
        {painPoints.map((point, index) => {
          const itemOpacity = interpolate(
            frame,
            [point.delay, point.delay + 20],
            [0, 1],
            { extrapolateRight: 'clamp' }
          );

          return (
            <div
              key={index}
              style={{
                display: 'flex',
                alignItems: 'center',
                marginBottom: 28,
                opacity: globalOpacity * itemOpacity,
                fontSize: 26,
                color: '#ccc',
              }}
            >
              <span style={{ fontSize: 40, marginRight: 16 }}>{point.icon}</span>
              <span>{point.text}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
