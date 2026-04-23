import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { CoverScene } from './scenes/CoverScene';
import { CSPScene } from './scenes/CSPScene';
import { UIScene } from './scenes/UIScene';
import { QwenScene } from './scenes/QwenScene';
import { FixesScene } from './scenes/FixesScene';
import { EndingScene } from './scenes/EndingScene';

export const OpenClawUpdateVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {/* 场景1: 封面 (0-3秒) */}
      <Sequence from={0} durationInFrames={90}>
        <CoverScene />
      </Sequence>

      {/* 场景2: CSP 安全加固 (3-9秒) */}
      <Sequence from={90} durationInFrames={180}>
        <CSPScene />
      </Sequence>

      {/* 场景3: 全新 UI 主题 (9-15秒) */}
      <Sequence from={270} durationInFrames={180}>
        <UIScene />
      </Sequence>

      {/* 场景4: Qwen 模型支持 (15-21秒) */}
      <Sequence from={450} durationInFrames={180}>
        <QwenScene />
      </Sequence>

      {/* 场景5: 50+ Bug 修复 (21-27秒) */}
      <Sequence from={630} durationInFrames={180}>
        <FixesScene />
      </Sequence>

      {/* 场景6: 结尾 (27-30秒) */}
      <Sequence from={810} durationInFrames={90}>
        <EndingScene />
      </Sequence>
    </AbsoluteFill>
  );
};
