import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ScriptScene: React.FC = () => {
  const frame = useCurrentFrame();
  
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const codeOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const executeOpacity = interpolate(frame, [90, 110], [0, 1], {
    extrapolateRight: "clamp",
  });
  
  const progressWidth = interpolate(frame, [110, 180], [0, 100], {
    extrapolateRight: "clamp",
  });
  
  const successOpacity = interpolate(frame, [190, 210], [0, 1], {
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
        Script：自动执行代码
      </h2>
      
      {/* 代码编辑器 */}
      <div
        style={{
          backgroundColor: "#2d2d44",
          borderRadius: 20,
          padding: 40,
          fontFamily: "monospace",
          fontSize: 32,
          color: "#e0e0e0",
          opacity: codeOpacity,
          marginBottom: 60,
        }}
      >
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
        
        <div style={{ color: "#667eea", marginBottom: 10 }}>upload.py</div>
        <pre style={{ margin: 0 }}>
{`def upload_to_server(content):
    """上传总结到服务器"""
    response = requests.post(
        "https://api.example.com/upload",
        data={"content": content}
    )
    return response.json()`}
        </pre>
      </div>
      
      {/* 执行过程 */}
      <div
        style={{
          opacity: executeOpacity,
          display: "flex",
          flexDirection: "column",
          gap: 20,
        }}
      >
        {/* 执行命令 */}
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
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
            ▶️
          </div>
          <div style={{ fontSize: 48, color: "white" }}>
            执行 upload.py
          </div>
        </div>
        
        {/* 进度条 */}
        <div
          style={{
            width: "100%",
            height: 20,
            backgroundColor: "#2d2d44",
            borderRadius: 10,
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${progressWidth}%`,
              height: "100%",
              backgroundColor: "#667eea",
              transition: "width 0.1s",
            }}
          />
        </div>
        
        {/* 成功提示 */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 20,
            opacity: successOpacity,
          }}
        >
          <div
            style={{
              width: 60,
              height: 60,
              borderRadius: 30,
              backgroundColor: "#27ca3f",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: 32,
            }}
          >
            ✓
          </div>
          <div style={{ fontSize: 48, color: "#27ca3f" }}>
            上传成功！
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
          opacity: interpolate(frame, [220, 240], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        Script 只执行，不读取代码 → 不占用上下文！
      </p>
    </AbsoluteFill>
  );
};
