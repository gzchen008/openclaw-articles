import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ReferenceScene: React.FC = () => {
  const frame = useCurrentFrame();
  
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const meetingOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const triggerOpacity = interpolate(frame, [60, 80], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const fileOpacity = interpolate(frame, [90, 110], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const resultOpacity = interpolate(frame, [120, 140], [0, 1], {
    extrapolateRight: "clamp" });

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
        Reference：条件读取
      </h2>
      
      {/* 流程图 */}
      <div style={{ display: "flex", flexDirection: "column", gap: 40 }}>
        {/* 会议内容 */}
        <div
          style={{
            backgroundColor: "#2d2d44",
            padding: 30,
            borderRadius: 15,
            opacity: meetingOpacity,
          }}
        >
          <div style={{ fontSize: 32, color: "#667eea", marginBottom: 10 }}>
            会议记录
          </div>
          <div style={{ fontSize: 48, color: "white" }}>
            "老陈让小李订 <span style={{ color: "#f093fb", fontWeight: "bold" }}>1200</span> 一晚的酒店"
          </div>
        </div>
        
        {/* 触发器 */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 20,
            opacity: triggerOpacity,
          }}
        >
          <div
            style={{
              width: 80,
              height: 80,
              borderRadius: 40,
              backgroundColor: "#f093fb",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: 48,
            }}
          >
            ⚠️
          </div>
          <div style={{ fontSize: 48, color: "white" }}>
            检测到"钱"关键词 → 触发财务提醒
          </div>
        </div>
        
        {/* 读取文件 */}
        <div
          style={{
            backgroundColor: "#2d2d44",
            padding: 30,
            borderRadius: 15,
            opacity: fileOpacity,
            display: "flex",
            alignItems: "center",
            gap: 20,
          }}
        >
          <div
            style={{
              width: 60,
              height: 60,
              borderRadius: 10,
              backgroundColor: "#667eea",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: 32,
            }}
          >
            📄
          </div>
          <div>
            <div style={{ fontSize: 32, color: "#667eea", marginBottom: 5 }}>
              读取文件
            </div>
            <div style={{ fontSize: 48, color: "white" }}>
              集团财务手册.md
            </div>
          </div>
        </div>
        
        {/* 结果 */}
        <div
          style={{
            backgroundColor: "#2d2d44",
            padding: 30,
            borderRadius: 15,
            border: "4px solid #f093fb",
            opacity: resultOpacity,
          }}
        >
          <div style={{ fontSize: 32, color: "#f093fb", marginBottom: 10 }}>
            ⚠️ 财务提醒
          </div>
          <div style={{ fontSize: 48, color: "white" }}>
            住宿标准 500/晚，超标！需审批
          </div>
        </div>
      </div>
      
      {/* 说明 */}
      <p
        style={{
          position: "absolute",
          bottom: 100,
          fontSize: 36,
          color: "#a0a0a0",
          opacity: interpolate(frame, [150, 170], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        如果没提到钱，财务文件不会被加载 → 节省 Token！
      </p>
    </AbsoluteFill>
  );
};
