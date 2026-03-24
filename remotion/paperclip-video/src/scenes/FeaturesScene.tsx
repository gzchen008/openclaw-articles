import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const FeaturesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const globalOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  const features = [
    { icon: '🏢', title: '组织架构', desc: 'CEO、CTO、工程师分工明确', delay: 20 },
    { icon: '💰', title: '预算控制', desc: '超限自动停止，不烧钱', delay: 35 },
    { icon: '🎯', title: '目标对齐', desc: '所有任务追溯到公司使命', delay: 50 },
    { icon: '⏰', title: '心跳机制', desc: '定时唤醒，自动执行任务', delay: 65 },
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
            color: '#4CAF50',
            textAlign: 'center',
            marginBottom: 48,
            opacity: globalOpacity,
          }}
        >
          核心特性
        </div>

        {/* 特性列表 */}
        {features.map((feature, index) => {
          const itemOpacity = interpolate(
            frame,
            [feature.delay, feature.delay + 20],
            [0, 1],
            { extrapolateRight: 'clamp' }
          );

          return (
            <div
              key={index}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                marginBottom: 32,
                opacity: globalOpacity * itemOpacity,
                fontSize: 22,
                color: '#ccc',
              }}
            >
              <span style={{ fontSize: 48, marginBottom: 8 }}>{feature.icon}</span>
              <div style={{ fontSize: 28, fontWeight: 'bold', color: '#fff', marginBottom: 4 }}>
                {feature.title}
              </div>
              <div style={{ fontSize: 20 }}>{feature.desc}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
