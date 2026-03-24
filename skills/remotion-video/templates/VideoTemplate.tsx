import React from 'react';
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame, Img, staticFile } from 'remotion';

// ============ 场景组件 ============

// 封面场景
export const CoverScene: React.FC<{ title: string; subtitle?: string }> = ({ title, subtitle }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [60, 90], [1, 0], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', backgroundColor: '#0a0a0a' }}>
      <div style={{ opacity: opacity * fadeOut, textAlign: 'center', padding: 48 }}>
        {staticFile('cover.jpg') ? (
          <Img src={staticFile('cover.jpg')} style={{ width: 1080, height: 1920, objectFit: 'cover' }} />
        ) : (
          <>
            <div style={{ fontSize: 56, fontWeight: 'bold', color: '#4CAF50', marginBottom: 24 }}>{title}</div>
            {subtitle && <div style={{ fontSize: 32, color: '#fff' }}>{subtitle}</div>}
          </>
        )}
      </div>
    </AbsoluteFill>
  );
};

// 文本场景（通用）
export const TextScene: React.FC<{
  title: string;
  lines: string[];
  titleColor?: string;
  bgColor?: string;
}> = ({ title, lines, titleColor = '#4CAF50', bgColor = '#0a0a0a' }) => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  
  return (
    <AbsoluteFill style={{ backgroundColor: bgColor, justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: titleColor, opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          {title}
        </div>
        {lines.map((line, index) => {
          const lineOpacity = interpolate(frame, [20 + index * 20, 40 + index * 20], [0, 1], { extrapolateRight: 'clamp' });
          return (
            <div key={index} style={{ fontSize: 28, color: '#fff', opacity: lineOpacity, marginBottom: 24, textAlign: 'center', lineHeight: 1.6 }}>
              {line}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// 卡片场景
export const CardScene: React.FC<{
  title: string;
  cards: Array<{ title: string; content: string; color?: string }>;
}> = ({ title, cards }) => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 40, textAlign: 'center' }}>
          {title}
        </div>
        {cards.map((card, index) => {
          const cardOpacity = interpolate(frame, [20 + index * 20, 40 + index * 20], [0, 1], { extrapolateRight: 'clamp' });
          return (
            <div key={index} style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 20, width: '100%', opacity: cardOpacity, borderLeft: `4px solid ${card.color || '#4CAF50'}` }}>
              <div style={{ fontSize: 24, color: card.color || '#4CAF50', marginBottom: 8 }}>{card.title}</div>
              <div style={{ fontSize: 20, color: '#ccc' }}>{card.content}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// 对比场景
export const ComparisonScene: React.FC<{
  title: string;
  comparisons: Array<{ left: string; right: string }>;
}> = ({ title, comparisons }) => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 40, textAlign: 'center' }}>
          {title}
        </div>
        {comparisons.map((comp, index) => {
          const rowOpacity = interpolate(frame, [20 + index * 20, 40 + index * 20], [0, 1], { extrapolateRight: 'clamp' });
          return (
            <div key={index} style={{ display: 'flex', width: '100%', marginBottom: 16, opacity: rowOpacity }}>
              <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, marginRight: 12 }}>
                <div style={{ fontSize: 20, color: '#ff6b6b', marginBottom: 8 }}>❌ {comp.left}</div>
              </div>
              <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, borderLeft: '3px solid #4CAF50' }}>
                <div style={{ fontSize: 20, color: '#4CAF50', marginBottom: 8 }}>✅ {comp.right}</div>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// CTA 场景
export const CTAScene: React.FC<{
  title: string;
  steps: string[];
}> = ({ title, steps }) => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          {title}
        </div>
        {steps.map((step, index) => {
          const stepOpacity = interpolate(frame, [20 + index * 20, 40 + index * 20], [0, 1], { extrapolateRight: 'clamp' });
          return (
            <div key={index} style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 20, width: '100%', opacity: stepOpacity }}>
              <div style={{ fontSize: 24, color: '#4CAF50' }}>{index + 1}️⃣ {step}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ============ 主视频组件 ============

export interface VideoConfig {
  title: string;
  subtitle?: string;
  scenes: Array<{
    type: 'cover' | 'text' | 'card' | 'comparison' | 'cta';
    title: string;
    data: any;
    duration: number;
  }>;
}

export const generateVideo = (config: VideoConfig) => {
  const totalFrames = config.scenes.reduce((sum, s) => sum + s.duration * 30, 0);
  
  return () => {
    let currentFrame = 0;
    
    return (
      <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
        {config.scenes.map((scene, index) => {
          const from = currentFrame;
          currentFrame += scene.duration * 30;
          
          return (
            <Sequence key={index} from={from} durationInFrames={scene.duration * 30}>
              {scene.type === 'cover' && <CoverScene title={scene.title} subtitle={scene.data.subtitle} />}
              {scene.type === 'text' && <TextScene title={scene.title} lines={scene.data.lines} />}
              {scene.type === 'card' && <CardScene title={scene.title} cards={scene.data.cards} />}
              {scene.type === 'comparison' && <ComparisonScene title={scene.title} comparisons={scene.data.comparisons} />}
              {scene.type === 'cta' && <CTAScene title={scene.title} steps={scene.data.steps} />}
            </Sequence>
          );
        })}
      </AbsoluteFill>
    );
  };
};
