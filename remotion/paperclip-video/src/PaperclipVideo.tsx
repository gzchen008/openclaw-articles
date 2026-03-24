import React from 'react';
import { AbsoluteFill, Sequence, interpolate } from 'remotion';
import { CoverScene } from './scenes/CoverScene';
import { PainPointScene } from './scenes/PainPointScene';
import { FeaturesScene } from './scenes/FeaturesScene';
import { ComparisonScene } from './scenes/ComparisonScene';
import { QuickStartScene } from './scenes/QuickStartScene';
import { TechScene } from './scenes/TechScene';
import { CtaScene } from './scenes/CtaScene';

export const PaperclipVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {/* 场景1: 封面 (0-3秒) */}
      <Sequence from={0} durationInFrames={90}>
        <CoverScene />
      </Sequence>

      {/* 场景2: 痛点 (3-8秒) */}
      <Sequence from={90} durationInFrames={150}>
        <PainPointScene />
      </Sequence>

      {/* 场景3: 核心特性 (8-13秒) */}
      <Sequence from={240} durationInFrames={150}>
        <FeaturesScene />
      </Sequence>

      {/* 场景4: 对比 (13-18秒) */}
      <Sequence from={390} durationInFrames={150}>
        <ComparisonScene />
      </Sequence>

      {/* 场景5: 三步启动 (18-23秒) */}
      <Sequence from={540} durationInFrames={150}>
        <QuickStartScene />
      </Sequence>

      {/* 场景6: 技术亮点 (23-28秒) */}
      <Sequence from={690} durationInFrames={150}>
        <TechScene />
      </Sequence>

      {/* 场景7: 结尾 (28-37秒) */}
      <Sequence from={840} durationInFrames={270}>
        <CtaScene />
      </Sequence>
    </AbsoluteFill>
  );
};
