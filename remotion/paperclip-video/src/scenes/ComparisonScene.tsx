import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const ComparisonScene: React.FC = () => {
  const frame = useCurrentFrame();
  const globalOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  const comparisons = [
    {
      without: '20个终端混乱',
      with: '任务工单化',
      delay: 20,
    },
    {
      without: '手动收集上下文',
      with: '上下文自动流转',
      delay: 40,
    },
    {
      without: 'Agent 疯狂烧钱',
      with: '预算限制 + 成本追踪',
      delay: 60,
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
            color: '#fff',
            textAlign: 'center',
            marginBottom: 48,
            opacity: globalOpacity,
          }}
        >
          没有 vs 有了
        </div>

        {/* 对比列表 */}
        {comparisons.map((comp, index) => {
          const itemOpacity = interpolate(
            frame,
            [comp.delay, comp.delay + 20],
            [0, 1],
            { extrapolateRight: 'clamp' }
          );

          return (
            <div
              key={index}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                width: '100%',
                marginBottom: 28,
                opacity: globalOpacity * itemOpacity,
                fontSize: 22,
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  fontSize: 26,
                  color: '#ff6b6b',
                  flex: 1,
                }}
              >
                ❌ {comp.without}
              </div>
              <div style={{ fontSize: 40, margin: '0 16px' }}>➡️</div>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  fontSize: 26,
                  color: '#4CAF50',
                  flex: 1,
                  textAlign: 'right',
                }}
              >
                {comp.with} ✅
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
