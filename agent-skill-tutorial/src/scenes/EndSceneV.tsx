import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, spring, useVideoConfig } from "remotion";

export const EndSceneV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const scale = spring({ frame, fps, config: { damping: 200 } });
  
  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      {/* 标题 */}
      <h1
        style={{
          fontSize: 64,
          fontWeight: "bold",
          color: "white",
          textAlign: "center",
          marginBottom: 60,
          transform: `scale(${scale})`,
        }}
      >
        开始创建你的 Skill！
      </h1>
      
      {/* 链接 */}
      <div
        style={{
          backgroundColor: "rgba(255,255,255,0.2)",
          borderRadius: 30,
          padding: 40,
          opacity: interpolate(frame, [10, 25], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <p
          style={{
            fontSize: 36,
            color: "white",
            textAlign: "center",
            margin: 0,
          }}
        >
          📚 docs.openclaw.ai
        </p>
      </div>
      
      {/* 底部 */}
      <div
        style={{
          position: "absolute",
          bottom: 200,
          opacity: interpolate(frame, [20, 35], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <p
          style={{
            fontSize: 32,
            color: "rgba(255,255,255,0.7)",
            textAlign: "center",
          }}
        >
          ⭐ GitHub: openclaw/openclaw
        </p>
      </div>
    </AbsoluteFill>
  );
};
