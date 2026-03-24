import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, spring } from "remotion";

export const EndScene: React.FC = () => {
  const frame = useCurrentFrame();
  
  const scale = spring({
    frame,
    fps: 30,
    config: {
      damping: 100,
      stiffness: 200,
      mass: 0.5,
    },
  });
  
  const textOpacity = interpolate(frame, [30, 60], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      {/* 大图标 */}
      <div
        style={{
          width: 300,
          height: 300,
          borderRadius: 75,
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          marginBottom: 80,
          transform: `scale(${scale})`,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: 150,
          boxShadow: "0 20px 60px rgba(102, 126, 234, 0.5)",
        }}
      >
        ✓
      </div>
      
      {/* 标题 */}
      <h1
        style={{
          fontSize: 100,
          fontWeight: "bold",
          color: "white",
          marginBottom: 40,
          opacity: textOpacity,
        }}
      >
        学会了！
      </h1>
      
      {/* 提示 */}
      <div
        style={{
          fontSize: 48,
          color: "#a0a0a0",
          textAlign: "center",
          opacity: textOpacity,
        }}
      >
        <div style={{ marginBottom: 20 }}>👍 点赞收藏</div>
        <div style={{ marginBottom: 20 }}>🔔 关注不迷路</div>
        <div>💬 下期教你写自己的 Skill！</div>
      </div>
      
      {/* 装饰粒子 */}
      {[...Array(30)].map((_, i) => {
        const angle = (i / 30) * Math.PI * 2;
        const radius = 500;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;
        const opacity = interpolate(
          frame,
          [60 + i * 3, 60 + i * 3 + 20],
          [0, 0.5],
          { extrapolateRight: "clamp" }
        );
        
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: 960 + x,
              top: 540 + y,
              width: 12,
              height: 12,
              borderRadius: 6,
              backgroundColor: "#667eea",
              opacity,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};
