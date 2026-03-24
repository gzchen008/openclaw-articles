import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const CreateSkillSceneV: React.FC = () => {
  const frame = useCurrentFrame();
  
  const steps = [
    { cmd: "mkdir my-skill", desc: "创建技能目录" },
    { cmd: "cd my-skill", desc: "进入目录" },
    { cmd: "echo 'description' > skill.md", desc: "创建技能文件" },
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
        创建你的第一个 Skill
      </h2>
      
      {/* 终端窗口 */}
      <div
        style={{
          backgroundColor: "#0d1117",
          borderRadius: 20,
          padding: 40,
          width: "100%",
          opacity: interpolate(frame, [20, 40], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        {/* 终端标题栏 */}
        <div
          style={{
            display: "flex",
            gap: 12,
            marginBottom: 30,
          }}
        >
          <div style={{ width: 20, height: 20, borderRadius: 10, backgroundColor: "#ff5f56" }} />
          <div style={{ width: 20, height: 20, borderRadius: 10, backgroundColor: "#ffbd2e" }} />
          <div style={{ width: 20, height: 20, borderRadius: 10, backgroundColor: "#27ca40" }} />
        </div>
        
        {/* 命令行 - 垂直排列，不重叠 */}
        {steps.map((step, index) => {
          const delay = 40 + index * 60;
          const opacity = interpolate(
            frame,
            [delay, delay + 20],
            [0, 1],
            { extrapolateRight: "clamp" }
          );
          
          return (
            <div
              key={index}
              style={{
                display: "flex",
                flexDirection: "column",
                marginBottom: 40,
                opacity,
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 15,
                  marginBottom: 10,
                }}
              >
                <span style={{ color: "#58a6ff", fontSize: 32 }}>$</span>
                <code
                  style={{
                    color: "#c9d1d9",
                    fontSize: 32,
                    fontFamily: "monospace",
                  }}
                >
                  {step.cmd}
                </code>
              </div>
              <span
                style={{
                  color: "#8b949e",
                  fontSize: 28,
                  marginLeft: 50,
                }}
              >
                # {step.desc}
              </span>
            </div>
          );
        })}
      </div>
      
      {/* 提示 */}
      <p
        style={{
          position: "absolute",
          bottom: 150,
          fontSize: 32,
          color: "#a0a0a0",
          textAlign: "center",
          width: "100%",
          opacity: interpolate(frame, [200, 230], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        只需一个 skill.md 文件！
      </p>
    </AbsoluteFill>
  );
};
