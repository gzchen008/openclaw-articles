import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { CoverScene } from './scenes/CoverScene';
import { BackupScene } from './scenes/BackupScene';
import { BraveSearchScene } from './scenes/BraveSearchScene';
import { TalkSilenceScene } from './scenes/TalkSilenceScene';
import { ACPProvenanceScene } from './scenes/ACPProvenanceScene';
import { EndingScene } from './scenes/EndingScene';

export const OpenClawUpdateVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {/* 场景1: 封面 (0-3秒) */}
      <Sequence from={0} durationInFrames={90}>
        <CoverScene />
      </Sequence>

      {/* 场景2: CLI 备份系统 (3-9秒) */}
      <Sequence from={90} durationInFrames={180}>
        <BackupScene />
      </Sequence>

      {/* 场景3: Brave 智能搜索 (9-15秒) */}
      <Sequence from={270} durationInFrames={180}>
        <BraveSearchScene />
      </Sequence>

      {/* 场景4: Talk 静默检测 (15-21秒) */}
      <Sequence from={450} durationInFrames={180}>
        <TalkSilenceScene />
      </Sequence>

      {/* 场景5: ACP 来源追踪 (21-27秒) */}
      <Sequence from={630} durationInFrames={180}>
        <ACPProvenanceScene />
      </Sequence>

      {/* 场景6: 结尾 (27-30秒) */}
      <Sequence from={810} durationInFrames={90}>
        <EndingScene />
      </Sequence>
    </AbsoluteFill>
  );
};
