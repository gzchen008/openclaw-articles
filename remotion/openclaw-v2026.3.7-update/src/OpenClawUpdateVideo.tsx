import React from 'react';
import { AbsoluteFill, Sequence, useCurrentFrame, interpolate, spring } from 'remotion';
import { CoverScene } from './scenes/CoverScene';
import { ContextEngineScene } from './scenes/ContextEngineScene';
import { ACPBindingScene } from './scenes/ACPBindingScene';
import { TelegramTopicScene } from './scenes/TelegramTopicScene';
import { WebUIScene } from './scenes/WebUIScene';
import { WebSearchScene } from './scenes/WebSearchScene';
import { EndingScene } from './scenes/EndingScene';

export const OpenClawUpdateVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {/* 场景1: 封面 (0-3秒) */}
      <Sequence from={0} durationInFrames={90}>
        <CoverScene />
      </Sequence>

      {/* 场景2: Context Engine (3-8秒) */}
      <Sequence from={90} durationInFrames={150}>
        <ContextEngineScene />
      </Sequence>

      {/* 场景3: ACP 持久化绑定 (8-13秒) */}
      <Sequence from={240} durationInFrames={150}>
        <ACPBindingScene />
      </Sequence>

      {/* 场景4: Telegram 话题路由 (13-18秒) */}
      <Sequence from={390} durationInFrames={150}>
        <TelegramTopicScene />
      </Sequence>

      {/* 场景5: Web UI 国际化 (18-23秒) */}
      <Sequence from={540} durationInFrames={150}>
        <WebUIScene />
      </Sequence>

      {/* 场景6: Web Search 增强 (23-28秒) */}
      <Sequence from={690} durationInFrames={150}>
        <WebSearchScene />
      </Sequence>

      {/* 场景7: 结尾 (28-30秒) */}
      <Sequence from={840} durationInFrames={60}>
        <EndingScene />
      </Sequence>
    </AbsoluteFill>
  );
};
