import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ScriptSceneV: React.FC = () => {
  const frame = useCurrentFrame();
  
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
          marginBottom: 60,
          opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        Script：可执行脚本
      </h2>
      
      {/* 代码示例 */}
      <div
        style={{
          backgroundColor: "#0d1117",
          borderRadius: 20,
          padding: 50,
          opacity: interpolate(frame, [20, 40], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <pre
          style={{
            color: "#c9d1d9",
            fontSize: 26,
            fontFamily: "monospace",
            lineHeight: 1.6,
            margin: 0,
          }}
        >
{`## Scripts
- name: "format-code"
  command: "npx prettier --write"
  
- name: "run-tests"
  command: "npm test"`}
        </pre>
      </div>
      
      {/* 特点 */}
      <div
        style={{
          marginTop: 50,
          display: "flex",
          flexDirection: "column",
          gap: 30,
        }}
      >
        {[
          "⚡ 自动执行命令",
          "🔒 安全的沙箱环境",
          "🎯 精确控制 Agent 行为",
        ].map((item, index) => {
          const delay = 50 + index * 15;
          return (
            <div
              key={index}
              style={{
                fontSize: 36,
                color: "white",
                opacity: interpolate(frame, [delay, delay + 15], [0, 1], { extrapolateRight: "clamp" }),
                transform: `translateX(${interpolate(frame, [delay, delay + 15], [-30, 0], { extrapolateRight: "clamp" })}px)`,
              }}
            >
              {item}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
