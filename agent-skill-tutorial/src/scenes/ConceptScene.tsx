import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ConceptScene: React.FC = () => {
  const frame = useCurrentFrame();
  
  const textOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const listItems = [
    "大模型可以随时翻阅的说明文档",
    "做智能客服：规定投诉处理流程",
    "做会议总结：规定输出格式",
    "不用每次粘贴长提示词",
    "AI 自己看文档就知道怎么干活",
  ];
  
  const itemDelay = 15;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        padding: 100,
        justifyContent: "flex-start",
        paddingTop: 150,
      }}
    >
      {/* 标题 */}
      <h2
        style={{
          fontSize: 80,
          fontWeight: "bold",
          color: "white",
          marginBottom: 80,
          opacity: textOpacity,
        }}
      >
        什么是 Agent Skill？
      </h2>
      
      {/* 列表项 */}
      {listItems.map((item, index) => {
        const itemOpacity = interpolate(
          frame,
          [index * itemDelay, index * itemDelay + 15],
          [0, 1],
          { extrapolateRight: "clamp" }
        );
        
        const itemX = interpolate(
          frame,
          [index * itemDelay, index * itemDelay + 15],
          [-50, 0],
          { extrapolateRight: "clamp" }
        );
        
        return (
          <div
            key={index}
            style={{
              display: "flex",
              alignItems: "center",
              marginBottom: 40,
              opacity: itemOpacity,
              transform: `translateX(${itemX}px)`,
            }}
          >
            {/* 图标 */}
            <div
              style={{
                width: 60,
                height: 60,
                borderRadius: 30,
                background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                marginRight: 40,
                fontSize: 32,
                color: "white",
                fontWeight: "bold",
              }}
            >
              ✓
            </div>
            
            {/* 文本 */}
            <p
              style={{
                fontSize: 48,
                color: "white",
                margin: 0,
              }}
            >
              {item}
            </p>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
