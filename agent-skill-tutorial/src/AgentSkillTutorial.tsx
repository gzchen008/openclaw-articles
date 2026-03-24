import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
  interpolate,
  spring,
  useCurrentFrame,
} from "remotion";
import { TitleScene } from "./scenes/TitleScene";
import { ConceptScene } from "./scenes/ConceptScene";
import { CreateSkillScene } from "./scenes/CreateSkillScene";
import { ThreeLayersScene } from "./scenes/ThreeLayersScene";
import { ReferenceScene } from "./scenes/ReferenceScene";
import { ScriptScene } from "./scenes/ScriptScene";
import { MCPCompareScene } from "./scenes/MCPCompareScene";
import { EndScene } from "./scenes/EndScene";

export const AgentSkillTutorial: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a2e" }}>
      {/* 场景1: 开场标题 (0-3秒) */}
      <Sequence from={0} durationInFrames={90}>
        <TitleScene />
      </Sequence>

      {/* 场景2: 核心概念 (3-8秒) */}
      <Sequence from={90} durationInFrames={150}>
        <ConceptScene />
      </Sequence>

      {/* 场景3: 创建 Skill (8-18秒) */}
      <Sequence from={240} durationInFrames={300}>
        <CreateSkillScene />
      </Sequence>

      {/* 场景4: 三层架构 (18-35秒) */}
      <Sequence from={540} durationInFrames={510}>
        <ThreeLayersScene />
      </Sequence>

      {/* 场景5: Reference 示例 (35-50秒) */}
      <Sequence from={1050} durationInFrames={450}>
        <ReferenceScene />
      </Sequence>

      {/* 场景6: Script 示例 (50-65秒) */}
      <Sequence from={1500} durationInFrames={450}>
        <ScriptScene />
      </Sequence>

      {/* 场景7: MCP 对比 (65-80秒) */}
      <Sequence from={1950} durationInFrames={450}>
        <MCPCompareScene />
      </Sequence>

      {/* 场景8: 结尾 (80-90秒) */}
      <Sequence from={2400} durationInFrames={300}>
        <EndScene />
      </Sequence>
    </AbsoluteFill>
  );
};
