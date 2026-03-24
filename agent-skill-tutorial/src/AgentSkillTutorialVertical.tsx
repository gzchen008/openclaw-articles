import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { TitleSceneV } from "./scenes/TitleSceneV";
import { ConceptSceneV } from "./scenes/ConceptSceneV";
import { CreateSkillSceneV } from "./scenes/CreateSkillSceneV";
import { ThreeLayersSceneV } from "./scenes/ThreeLayersSceneV";
import { ReferenceSceneV } from "./scenes/ReferenceSceneV";
import { ScriptSceneV } from "./scenes/ScriptSceneV";
import { MCPCompareSceneV } from "./scenes/MCPCompareSceneV";
import { EndSceneV } from "./scenes/EndSceneV";

export const AgentSkillTutorialVertical: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a2e" }}>
      {/* 场景1: 开场标题 (0-3秒) */}
      <Sequence from={0} durationInFrames={90}>
        <TitleSceneV />
      </Sequence>

      {/* 场景2: 核心概念 (3-9秒) */}
      <Sequence from={90} durationInFrames={180}>
        <ConceptSceneV />
      </Sequence>

      {/* 场景3: 创建 Skill (9-18秒) */}
      <Sequence from={270} durationInFrames={270}>
        <CreateSkillSceneV />
      </Sequence>

      {/* 场景4: 三层架构 (18-30秒) */}
      <Sequence from={540} durationInFrames={360}>
        <ThreeLayersSceneV />
      </Sequence>

      {/* 场景5: Reference 示例 (30-36秒) */}
      <Sequence from={900} durationInFrames={180}>
        <ReferenceSceneV />
      </Sequence>

      {/* 场景6: Script 示例 (36-40秒) */}
      <Sequence from={1080} durationInFrames={120}>
        <ScriptSceneV />
      </Sequence>

      {/* 场景7: MCP 对比 (40-44秒) */}
      <Sequence from={1200} durationInFrames={120}>
        <MCPCompareSceneV />
      </Sequence>

      {/* 场景8: 结尾 (44-45秒) */}
      <Sequence from={1320} durationInFrames={30}>
        <EndSceneV />
      </Sequence>
    </AbsoluteFill>
  );
};
