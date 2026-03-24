import React from "react";
import { Composition } from "remotion";
import { AgentSkillTutorialVertical } from "./AgentSkillTutorialVertical";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 竖屏版本：1080x1920, 45秒, 30fps, 2倍速播放 */}
      <Composition
        id="AgentSkillTutorialVertical"
        component={AgentSkillTutorialVertical}
        durationInFrames={1350}  // 45秒 @ 30fps
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
