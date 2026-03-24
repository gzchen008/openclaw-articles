import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const WebUIScene: React.FC = () => {
  const frame = useCurrentFrame();

  // 所有元素只使用 opacity 动画，不改变位置
  const titleOpacity = interpolate(frame, [0, 20], [0, 1]);
  const flag1Opacity = interpolate(frame, [30, 50], [0, 1]);
  const flag2Opacity = interpolate(frame, [50, 70], [0, 1]);
  const flag3Opacity = interpolate(frame, [70, 90], [0, 1]);
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
            marginBottom: 40,
            textAlign: 'center',
          }}
        >
          🌍 4. Web UI 国际化
        </div>

        {/* 语言列表 - 固定位置 */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 28,
          }}
        >
          {/* 英语 - 固定位置 */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 20,
              opacity: flag1Opacity,
            }}
          >
            <div style={{ fontSize: 72 }}>🇺🇸</div>
            <div style={{ fontSize: 28, color: '#8b949e' }}>English</div>
          </div>

          {/* 中文 - 固定位置 */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 20,
              opacity: flag2Opacity,
            }}
          >
            <div style={{ fontSize: 72 }}>🇨🇳</div>
            <div style={{ fontSize: 28, color: '#8b949e' }}>中文</div>
          </div>

          {/* 西班牙语 - 固定位置 */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 20,
              opacity: flag3Opacity,
            }}
          >
            <div style={{ fontSize: 72 }}>🇪🇸</div>
            <div style={{ fontSize: 28, color: '#8b949e' }}>Español</div>
          </div>
        </div>

        {/* 底部说明 - 固定位置 */}
        <div
          style={{
            marginTop: 40,
            fontSize: 24,
            color: '#8b949e',
            opacity: footerOpacity,
            textAlign: 'center',
          }}
        >
          ✅ 自动语言检测 + 懒加载
        </div>
      </div>
    </AbsoluteFill>
  );
};
