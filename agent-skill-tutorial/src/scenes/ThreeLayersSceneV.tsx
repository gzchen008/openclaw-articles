import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ThreeLayersSceneV: React.FC = () => {
  const frame = useCurrentFrame();
  
  const layers = [
    {
      name: "元数据层",
      description: "始终加载 · 名称 + 描述",
      color: "#667eea",
      delay: 0,
    },
    {
      name: "指令层",
      description: "按需加载 · skill.md 内容",
      color: "#764ba2",
      delay: 40,
    },
    {
      name: "资源层",
      description: "条件触发 · Reference + Script",
      color: "#f093fb",
      delay: 80,
    },
  ];
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        padding: 80,
        paddingTop: 120,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* 标题 */}
      <h2
        style={{
          fontSize: 52,
          fontWeight: "bold",
          color: "white",
          textAlign: "center",
          marginBottom: 60,
          opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        三层架构：渐进式披露
      </h2>
      
      {/* 图解说明 */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginBottom: 50,
          opacity: interpolate(frame, [20, 40], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <div
          style={{
            fontSize: 28,
            color: "#a0a0a0",
            textAlign: "center",
          }}
        >
          越深层越省 Token ⚡
        </div>
      </div>
      
      {/* 三层卡片 - 垂直排列，不重叠 */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 40,
          flex: 1,
          justifyContent: "center",
        }}
      >
        {layers.map((layer, index) => {
          const layerOpacity = interpolate(
            frame,
            [layer.delay, layer.delay + 20],
            [0, 1],
            { extrapolateRight: "clamp" }
          );
          
          const layerScale = interpolate(
            frame,
            [layer.delay, layer.delay + 20],
            [0.8, 1],
            { extrapolateRight: "clamp" }
          );
          
          return (
            <div
              key={index}
              style={{
                backgroundColor: layer.color,
                borderRadius: 30,
                padding: 50,
                opacity: layerOpacity,
                transform: `scale(${layerScale})`,
                boxShadow: "0 10px 40px rgba(0,0,0,0.4)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                <div>
                  <div
                    style={{
                      fontSize: 48,
                      fontWeight: "bold",
                      color: "white",
                      marginBottom: 15,
                    }}
                  >
                    {layer.name}
                  </div>
                  <div
                    style={{
                      fontSize: 30,
                      color: "rgba(255,255,255,0.85)",
                    }}
                  >
                    {layer.description}
                  </div>
                </div>
                <div
                  style={{
                    fontSize: 60,
                    opacity: 0.3,
                  }}
                >
                  {index + 1}
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* 底部说明 */}
      <div
        style={{
          marginTop: 50,
          opacity: interpolate(frame, [140, 160], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <p
          style={{
            fontSize: 30,
            color: "#8b949e",
            textAlign: "center",
          }}
        >
          💡 核心思想：只在需要时加载详细信息
        </p>
      </div>
    </AbsoluteFill>
  );
};
