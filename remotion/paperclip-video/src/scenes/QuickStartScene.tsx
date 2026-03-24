import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const QuickStartScene: React.FC = () => {
  const frame = useCurrentFrame();
  const globalOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  const steps = [
    {
      num: '1️⃣',
      title: '定义目标',
      desc: '打造 #1 AI 笔记应用',
      delay: 20,
    },
    {
      num: '2️⃣',
      title: '雇佣团队',
      desc: 'CEO、CTO、工程师...',
      delay: 45,
    },
    {
      num: '3️⃣',
      title: '审批并运行',
      desc: '设置预算 → 点击开始',
      delay: 70,
    },
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
          三步启动 AI 公司
        </div>

        {/* 步骤列表 */}
        {steps.map((step, index) => {
          const itemOpacity = interpolate(
            frame,
            [step.delay, step.delay + 20],
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
                marginBottom: 36,
                opacity: globalOpacity * itemOpacity,
                fontSize: 22,
                color: '#ccc',
              }}
            >
              <span style={{ fontSize: 56, marginBottom: 12 }}>{step.num}</span>
              <div style={{ fontSize: 32, fontWeight: 'bold', color: '#fff', marginBottom: 8 }}>
                {step.title}
              </div>
              <div style={{ fontSize: 22 }}>{step.desc}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
