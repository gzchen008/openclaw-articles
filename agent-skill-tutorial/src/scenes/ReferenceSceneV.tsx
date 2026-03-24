import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const ReferenceSceneV: React.FC = () => {
  const frame = useCurrentFrame();
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a2e",
        padding: 80,
        paddingTop: 150,
      }}
    >
      {/* 标题 */}
      <h2
        style={{
          fontSize: 56,
          fontWeight: "bold",
          color: "white",
          textAlign: "center",
          marginBottom: 60,
          opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        Reference：引用外部资源
      </h2>
      
      {/* 代码示例 */}
      <div
        style={{
          backgroundColor: "#0d1117",
          borderRadius: 20,
          padding: 50,
          opacity: interpolate(frame, [30, 50], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <pre
          style={{
            color: "#c9d1d9",
            fontSize: 26,
            fontFamily: "monospace",
            lineHeight: 1.6,
            margin: 0,
          }}
        >
{`## References
- name: "API文档"
  uri: "https://docs.example.com"
  type: "text/markdown"
  
- name: "数据库Schema"
  uri: "./schema.sql"
  type: "text/plain"`}
        </pre>
      </div>
      
      {/* 说明 - 垂直排列 */}
      <div
        style={{
          marginTop: 50,
          display: "flex",
          flexDirection: "column",
          gap: 30,
        }}
      >
        {[
          "✅ 支持远程 URL",
          "✅ 支持本地文件",
          "✅ 自动类型检测",
        ].map((item, index) => {
          const delay = 60 + index * 20;
          return (
            <div
              key={index}
              style={{
                fontSize: 36,
                color: "white",
                opacity: interpolate(frame, [delay, delay + 15], [0, 1], { extrapolateRight: "clamp" }),
                transform: `translateX(${interpolate(frame, [delay, delay + 15], [-30, 0], { extrapolateRight: "clamp" })}px)`,
              }}
            >
              {item}
            </div>
          );
        })}
      </div>
      
      {/* 优势 */}
      <div
        style={{
          position: "absolute",
          bottom: 150,
          width: "100%",
          opacity: interpolate(frame, [120, 140], [0, 1], { extrapolateRight: "clamp" }),
        }}
      >
        <p
          style={{
            fontSize: 32,
            color: "#a0a0a0",
            textAlign: "center",
          }}
        >
          📌 按需加载，不占用基础 Token
        </p>
      </div>
    </AbsoluteFill>
  );
};
