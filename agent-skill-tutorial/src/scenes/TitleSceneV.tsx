import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, spring, useVideoConfig } from "remotion";

export const TitleSceneV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const titleScale = spring({ frame, fps, config: { damping: 200 } });
  const subtitleOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateRight: "clamp" });
  
  // 粒子效果
  const particles = Array.from({ length: 20 }, (_, i) => ({
    x: Math.random() * 1080,
    y: Math.random() * 1920,
    size: Math.random() * 6 + 2,
    delay: Math.random() * 30,
  }));
  
  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* 粒子 */}
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: p.x,
            top: p.y,
            width: p.size,
            height: p.size,
            borderRadius: "50%",
            backgroundColor: "rgba(255,255,255,0.3)",
            opacity: interpolate(frame, [p.delay, p.delay + 20], [0, 0.8], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [p.delay, p.delay + 30], [0, 1], { extrapolateRight: "clamp" })})`,
          }}
        />
      ))}
      
      {/* Logo */}
      <div
        style={{
          width: 200,
          height: 200,
          borderRadius: 40,
          backgroundColor: "rgba(255,255,255,0.2)",
          marginBottom: 60,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: 100,
          transform: `scale(${titleScale})`,
        }}
      >
        🤖
      </div>
      
      {/* 标题 */}
      <h1
        style={{
          fontSize: 72,
          fontWeight: "bold",
          color: "white",
          textAlign: "center",
          margin: 0,
          transform: `scale(${titleScale})`,
          textShadow: "0 4px 20px rgba(0,0,0,0.3)",
        }}
      >
        Agent Skill
      </h1>
      
      <h2
        style={{
          fontSize: 36,
          color: "rgba(255,255,255,0.9)",
          marginTop: 30,
          opacity: subtitleOpacity,
        }}
      >
        Anthropic 技能系统教程
      </h2>
      
      {/* 底部提示 */}
      <p
        style={{
          position: "absolute",
          bottom: 200,
          fontSize: 28,
          color: "rgba(255,255,255,0.7)",
          opacity: interpolate(frame, [60, 80], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        45 秒掌握核心概念
      </p>
    </AbsoluteFill>
  );
};
