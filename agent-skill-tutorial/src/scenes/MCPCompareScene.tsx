import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const MCPCompareScene: React.FC = () => {
  const frame = useCurrentFrame();
  
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const leftOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const rightOpacity = interpolate(frame, [60, 80], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const centerOpacity = interpolate(frame, [90, 110], [0, 1], {
    extrapolateRight: "clamp",
  });

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
          opacity: titleOpacity,
        }}
      >
        MCP vs Agent Skill
      </h2>
      
      {/* 对比卡片 */}
      <div
        style={{
          display: "flex",
          gap: 100,
          marginTop: 100,
        }}
      >
        {/* MCP */}
        <div
          style={{
            width: 700,
            height: 500,
            backgroundColor: "#2d2d44",
            borderRadius: 30,
            padding: 50,
            opacity: leftOpacity,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <div
            style={{
              width: 120,
              height: 120,
              borderRadius: 60,
              backgroundColor: "#3b82f6",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: 60,
              marginBottom: 40,
            }}
          >
            🔌
          </div>
          
          <h3 style={{ fontSize: 60, color: "white", marginBottom: 30 }}>
            MCP
          </h3>
          
          <div style={{ fontSize: 36, color: "#a0a0a0", textAlign: "center" }}>
            <div style={{ marginBottom: 20 }}>连接数据</div>
            <div style={{ marginBottom: 20 }}>• 查询数据库</div>
            <div style={{ marginBottom: 20 }}>• 读取文件</div>
            <div style={{ marginBottom: 20 }}>• API 调用</div>
          </div>
        </div>
        
        {/* VS */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            opacity: centerOpacity,
          }}
        >
          <div
            style={{
              fontSize: 80,
              fontWeight: "bold",
              color: "#a0a0a0",
            }}
          >
            VS
          </div>
        </div>
        
        {/* Agent Skill */}
        <div
          style={{
            width: 700,
            height: 500,
            backgroundColor: "#2d2d44",
            borderRadius: 30,
            padding: 50,
            opacity: rightOpacity,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <div
            style={{
              width: 120,
              height: 120,
              borderRadius: 60,
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: 60,
              marginBottom: 40,
            }}
          >
            📚
          </div>
          
          <h3 style={{ fontSize: 60, color: "white", marginBottom: 30 }}>
            Agent Skill
          </h3>
          
          <div style={{ fontSize: 36, color: "#a0a0a0", textAlign: "center" }}>
            <div style={{ marginBottom: 20 }}>处理数据</div>
            <div style={{ marginBottom: 20 }}>• 会议总结格式</div>
            <div style={{ marginBottom: 20 }}>• 分析规则</div>
            <div style={{ marginBottom: 20 }}>• 输出模板</div>
          </div>
        </div>
      </div>
      
      {/* 底部说明 */}
      <p
        style={{
          position: "absolute",
          bottom: 100,
          fontSize: 48,
          color: "white",
          textAlign: "center",
          opacity: interpolate(frame, [120, 140], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        配合使用效果最佳！
      </p>
    </AbsoluteFill>
  );
};
