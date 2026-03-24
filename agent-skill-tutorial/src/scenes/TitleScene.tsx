import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, spring } from "remotion";

export const TitleScene: React.FC = () => {
  const frame = useCurrentFrame();
  
  const titleOpacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const titleScale = spring({
    frame,
    fps: 30,
    config: {
      damping: 100,
      stiffness: 200,
      mass: 0.5,
    },
  });
  
  const subtitleOpacity = interpolate(frame, [30, 60], [0, 1], {
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
      {/* Logo */}
      <div
        style={{
          width: 200,
          height: 200,
          borderRadius: 50,
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          marginBottom: 60,
          opacity: titleOpacity,
          transform: `scale(${titleScale})`,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: 100,
          color: "white",
          fontWeight: "bold",
        }}
      >
        AS
      </div>
      
      {/* 标题 */}
      <h1
        style={{
          fontSize: 120,
          fontWeight: "bold",
          color: "white",
          opacity: titleOpacity,
          transform: `scale(${titleScale})`,
          margin: 0,
          textShadow: "0 10px 30px rgba(0,0,0,0.3)",
        }}
      >
        Agent Skill 教程
      </h1>
      
      {/* 副标题 */}
      <p
        style={{
          fontSize: 48,
          color: "#a0a0a0",
          marginTop: 40,
          opacity: subtitleOpacity,
        }}
      >
        3分钟学会 AI 自动化
      </p>
      
      {/* 装饰粒子 */}
      {[...Array(20)].map((_, i) => {
        const x = (i * 100) % 1920;
        const y = (i * 80) % 1080;
        const opacity = interpolate(
          frame,
          [i * 3, i * 3 + 20],
          [0, 0.3],
          { extrapolateRight: "clamp" }
        );
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x,
              top: y,
              width: 8,
              height: 8,
              borderRadius: 4,
              backgroundColor: "#667eea",
              opacity,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};
