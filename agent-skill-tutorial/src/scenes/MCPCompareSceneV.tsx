import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const MCPCompareSceneV: React.FC = () => {
  const frame = useCurrentFrame();
  
  const comparisons = [
    { skill: "skill.md 文件", mcp: "JSON Schema 定义" },
    { skill: "声明式描述", mcp: "协议级通信" },
    { skill: "零配置启动", mcp: "需要服务器" },
    { skill: "人类可读", mcp: "机器优先" },
  ];
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        padding: 80,
        paddingTop: 120,
      }}
    >
      {/* 标题 */}
      <h2
        style={{
          fontSize: 56,
          fontWeight: "bold",
          color: "white",
          textAlign: "center",
          marginBottom: 60,
          opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        Agent Skill vs MCP
      </h2>
      
      {/* 对比卡片 - 垂直排列 */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 30,
        }}
      >
        {comparisons.map((item, index) => {
          const delay = 30 + index * 20;
          const opacity = interpolate(frame, [delay, delay + 15], [0, 1], { extrapolateRight: "clamp" });
          
          return (
            <div
              key={index}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                opacity,
                transform: `translateY(${interpolate(frame, [delay, delay + 15], [30, 0], { extrapolateRight: "clamp" })}px)`,
              }}
            >
              {/* Skill 侧 */}
              <div
                style={{
                  flex: 1,
                  backgroundColor: "rgba(102, 126, 234, 0.3)",
                  borderRadius: 20,
                  padding: 35,
                  textAlign: "center",
                }}
              >
                <span style={{ fontSize: 32, color: "white" }}>
                  ✅ {item.skill}
                </span>
              </div>
              
              {/* VS */}
              <div
                style={{
                  width: 100,
                  textAlign: "center",
                }}
              >
                <span style={{ fontSize: 28, color: "#a0a0a0" }}>vs</span>
              </div>
              
              {/* MCP 侧 */}
              <div
                style={{
                  flex: 1,
                  backgroundColor: "rgba(118, 75, 162, 0.3)",
                  borderRadius: 20,
                  padding: 35,
                  textAlign: "center",
                }}
              >
                <span style={{ fontSize: 32, color: "white" }}>
                  {item.mcp}
                </span>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* 结论 */}
      <div
        style={{
          marginTop: 50,
          opacity: interpolate(frame, [110, 130], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <p
          style={{
            fontSize: 32,
            color: "#8b949e",
            textAlign: "center",
          }}
        >
          💡 Skill 更轻量，MCP 更强大
        </p>
      </div>
    </AbsoluteFill>
  );
};
