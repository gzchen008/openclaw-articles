import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ThreeLayersScene: React.FC = () => {
  const frame = useCurrentFrame();
  
  const layers = [
    {
      name: "元数据层",
      description: "始终加载，名称+描述",
      color: "#667eea",
      delay: 0,
    },
    {
      name: "指令层",
      description: "按需加载，skill.md 内容",
      color: "#764ba2",
      delay: 60,
    },
    {
      name: "资源层",
      description: "条件触发，Reference + Script",
      color: "#f093fb",
      delay: 120,
    },
  ];

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        padding: 100,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* 标题 */}
      <h2
        style={{
          fontSize: 80,
          fontWeight: "bold",
          color: "white",
          position: "absolute",
          top: 100,
          opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        三层架构：渐进式披露
      </h2>
      
      {/* 金字塔 */}
      <div
        style={{
          position: "relative",
          width: 800,
          height: 600,
        }}
      >
        {layers.map((layer, index) => {
          const layerOpacity = interpolate(
            frame,
            [layer.delay, layer.delay + 30],
            [0, 1],
            { extrapolateRight: "clamp" }
          );
          
          const layerY = interpolate(
            frame,
            [layer.delay, layer.delay + 30],
            [100, 0],
            { extrapolateRight: "clamp" }
          );
          
          const width = 800 - index * 150;
          const height = 180;
          const top = index * 200;
          
          return (
            <div
              key={index}
              style={{
                position: "absolute",
                left: (800 - width) / 2,
                top: top + layerY,
                width: width,
                height: height,
                backgroundColor: layer.color,
                borderRadius: 20,
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                opacity: layerOpacity,
                boxShadow: "0 10px 30px rgba(0,0,0,0.3)",
              }}
            >
              <div
                style={{
                  fontSize: 48,
                  fontWeight: "bold",
                  color: "white",
                  marginBottom: 10,
                }}
              >
                {layer.name}
              </div>
              <div
                style={{
                  fontSize: 32,
                  color: "rgba(255,255,255,0.8)",
                }}
              >
                {layer.description}
              </div>
            </div>
          );
        })}
        
        {/* 箭头 */}
        {layers.map((_, index) => {
          if (index === layers.length - 1) return null;
          
          const arrowOpacity = interpolate(
            frame,
            [layers[index + 1].delay, layers[index + 1].delay + 30],
            [0, 1],
            { extrapolateRight: "clamp" }
          );
          
          return (
            <div
              key={`arrow-${index}`}
              style={{
                position: "absolute",
                left: 400 - 20,
                top: index * 200 + 180,
                width: 0,
                height: 0,
                borderLeft: "20px solid transparent",
                borderRight: "20px solid transparent",
                borderTop: "30px solid #a0a0a0",
                opacity: arrowOpacity,
              }}
            />
          );
        })}
      </div>
      
      {/* 底部说明 */}
      <p
        style={{
          position: "absolute",
          bottom: 100,
          fontSize: 48,
          color: "#a0a0a0",
          opacity: interpolate(frame, [180, 210], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        越深层越省 Token！
      </p>
    </AbsoluteFill>
  );
};
