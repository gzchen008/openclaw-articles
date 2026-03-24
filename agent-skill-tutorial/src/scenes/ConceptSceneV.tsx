import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ConceptSceneV: React.FC = () => {
  const frame = useCurrentFrame();
  
  const concepts = [
    { title: "说明文档", desc: "告诉 AI 什么时候用这个技能", icon: "📝" },
    { title: "skill.md", desc: "具体的指令内容", icon: "📄" },
    { title: "渐进披露", desc: "按需加载，节省 Token", icon: "⚡" },
  ];
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        padding: 80,
        paddingTop: 150,
      }}
    >
      {/* 标题 */}
      <h2
        style={{
          fontSize: 56,
          fontWeight: "bold",
          color: "white",
          textAlign: "center",
          marginBottom: 80,
          opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        Agent Skill 核心概念
      </h2>
      
      {/* 概念卡片 - 垂直排列，不重叠 */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 50,
          width: "100%",
        }}
      >
        {concepts.map((concept, index) => {
          const delay = index * 30;
          const opacity = interpolate(
            frame,
            [delay, delay + 20],
            [0, 1],
            { extrapolateRight: "clamp" }
          );
          
          const translateY = interpolate(
            frame,
            [delay, delay + 20],
            [50, 0],
            { extrapolateRight: "clamp" }
          );
          
          return (
            <div
              key={index}
              style={{
                backgroundColor: "rgba(255,255,255,0.1)",
                borderRadius: 30,
                padding: 50,
                display: "flex",
                alignItems: "center",
                gap: 40,
                opacity,
                transform: `translateY(${translateY}px)`,
                border: "2px solid rgba(255,255,255,0.2)",
              }}
            >
              <div
                style={{
                  fontSize: 64,
                  flexShrink: 0,
                }}
              >
                {concept.icon}
              </div>
              <div>
                <h3
                  style={{
                    fontSize: 42,
                    fontWeight: "bold",
                    color: "white",
                    marginBottom: 15,
                  }}
                >
                  {concept.title}
                </h3>
                <p
                  style={{
                    fontSize: 32,
                    color: "rgba(255,255,255,0.7)",
                    margin: 0,
                  }}
                >
                  {concept.desc}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
