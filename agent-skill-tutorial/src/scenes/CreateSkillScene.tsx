import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const CreateSkillScene: React.FC = () => {
  const frame = useCurrentFrame();
  
  const code = `---
name: 会议总结助手
description: 总结会议录音内容
---

## 输出格式
1. 参会人员
2. 会议议题
3. 关键决定`;
  
  const codeLines = code.split("\n");
  const charsToShow = interpolate(frame, [30, 150], [0, code.length], {
    extrapolateRight: "clamp",
  });
  
  const visibleCode = code.substring(0, Math.floor(charsToShow));
  
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        padding: 100,
        flexDirection: "column",
      }}
    >
      {/* 标题 */}
      <h2
        style={{
          fontSize: 80,
          fontWeight: "bold",
          color: "white",
          marginBottom: 60,
          opacity: titleOpacity,
        }}
      >
        如何创建 Skill？
      </h2>
      
      {/* 步骤 */}
      <div
        style={{
          display: "flex",
          marginBottom: 60,
          opacity: titleOpacity,
        }}
      >
        <div style={{ marginRight: 40 }}>
          <div
            style={{
              fontSize: 36,
              color: "#667eea",
              fontWeight: "bold",
              marginBottom: 10,
            }}
          >
            步骤 1
          </div>
          <div style={{ fontSize: 48, color: "white" }}>
            创建文件夹
          </div>
          <div style={{ fontSize: 32, color: "#a0a0a0", marginTop: 10 }}>
            ~/.claude/skill/会议总结助手
          </div>
        </div>
        
        <div>
          <div
            style={{
              fontSize: 36,
              color: "#667eea",
              fontWeight: "bold",
              marginBottom: 10,
            }}
          >
            步骤 2
          </div>
          <div style={{ fontSize: 48, color: "white" }}>
            创建 skill.md
          </div>
          <div style={{ fontSize: 32, color: "#a0a0a0", marginTop: 10 }}>
            填写元数据和指令
          </div>
        </div>
      </div>
      
      {/* 代码编辑器 */}
      <div
        style={{
          backgroundColor: "#2d2d44",
          borderRadius: 20,
          padding: 40,
          fontFamily: "monospace",
          fontSize: 36,
          color: "#e0e0e0",
          boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
        }}
      >
        {/* 窗口控制按钮 */}
        <div style={{ display: "flex", marginBottom: 20 }}>
          <div
            style={{
              width: 16,
              height: 16,
              borderRadius: 8,
              backgroundColor: "#ff5f56",
              marginRight: 10,
            }}
          />
          <div
            style={{
              width: 16,
              height: 16,
              borderRadius: 8,
              backgroundColor: "#ffbd2e",
              marginRight: 10,
            }}
          />
          <div
            style={{
              width: 16,
              height: 16,
              borderRadius: 8,
              backgroundColor: "#27ca3f",
            }}
          />
        </div>
        
        {/* 代码内容 */}
        <pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>
          {visibleCode}
          <span style={{ opacity: 0.5 }}>|</span>
        </pre>
      </div>
    </AbsoluteFill>
  );
};
