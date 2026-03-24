import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

export const TechScene: React.FC = () => {
  const frame = useCurrentFrame();
  const globalOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });

  const techs = [
    { icon: '⚡', title: '原子执行', desc: '不会重复工作，不会超支', delay: 20 },
    { icon: '💾', title: '持久化状态', desc: '跨心跳恢复任务上下文', delay: 40 },
    { icon: '🔒', title: '治理与回滚', desc: '配置变更版本化', delay: 60 },
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
            color: '#0366d6',
            textAlign: 'center',
            marginBottom: 48,
            opacity: globalOpacity,
          }}
        >
          技术亮点
        </div>

        {/* 技术列表 */}
        {techs.map((tech, index) => {
          const itemOpacity = interpolate(
            frame,
            [tech.delay, tech.delay + 20],
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
              <span style={{ fontSize: 48, marginBottom: 8 }}>{tech.icon}</span>
              <div style={{ fontSize: 28, fontWeight: 'bold', color: '#fff', marginBottom: 4 }}>
                {tech.title}
              </div>
              <div style={{ fontSize: 20 }}>{tech.desc}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
