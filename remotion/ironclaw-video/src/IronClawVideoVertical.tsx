import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

// 场景 1: 品牌封面（3秒）
const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30, 60, 90], [0, 1, 1, 0]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#1a1a1a",
        justifyContent: "center",
        alignItems: "center",
        opacity,
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1
          style={{
            fontSize: 100,
            fontWeight: "bold",
            color: "#0366d6",
            margin: 0,
            textShadow: "0 4px 20px rgba(3, 102, 214, 0.5)",
          }}
        >
          IronClaw
        </h1>
        <p
          style={{
            fontSize: 40,
            color: "#ffffff",
            marginTop: 20,
            opacity: 0.9,
          }}
        >
          安全优先的 AI 助手
        </p>
      </div>
    </AbsoluteFill>
  );
};

// 场景 2: 痛点场景（5秒）
const PainPointScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleProgress = spring({
    frame,
    fps,
    config: { damping: 100 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0d1117",
        padding: 60,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ textAlign: "center", width: "100%" }}>
        <h2
          style={{
            fontSize: 56,
            fontWeight: "bold",
            color: "#f66",
            marginBottom: 50,
            transform: `translateY(${interpolate(titleProgress, [0, 1], [-50, 0])}px)`,
            opacity: titleProgress,
          }}
        >
          ⚠️ 你的 AI 助手安全吗？
        </h2>

        <div style={{ display: "flex", flexDirection: "column", gap: 35, alignItems: "center" }}>
          {["❌ API 密钥泄露", "❌ 凭证被恶意工具窃取", "❌ 加密货币资产丢失"].map((text, index) => {
            const progress = spring({
              frame: frame - (index + 1) * 20,
              fps,
              config: { damping: 100 },
            });

            return (
              <div
                key={index}
                style={{
                  fontSize: 40,
                  color: "#ffffff",
                  opacity: progress,
                  transform: `translateX(${interpolate(progress, [0, 1], [-100, 0])}px)`,
                }}
              >
                {text}
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景 3: 功能介绍（6秒）
const FeaturesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const features = [
    { icon: "🔐", title: "凭证保护", desc: "加密保险库 + TEE" },
    { icon: "🛡️", title: "提示注入防御", desc: "多层安全过滤" },
    { icon: "🔍", title: "泄露检测", desc: "实时扫描请求响应" },
    { icon: "✅", title: "端点白名单", desc: "禁止未授权请求" },
  ];

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0d1117",
        padding: 60,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ textAlign: "center", width: "100%" }}>
        <h2
          style={{
            fontSize: 56,
            fontWeight: "bold",
            color: "#0366d6",
            marginBottom: 50,
          }}
        >
          🛡️ 6 层安全防护
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 30,
          }}
        >
          {features.map((feature, index) => {
            const progress = spring({
              frame: frame - index * 15,
              fps,
              config: { damping: 100 },
            });

            return (
              <div
                key={index}
                style={{
                  backgroundColor: "#161b22",
                  padding: 30,
                  borderRadius: 15,
                  opacity: progress,
                  transform: `scale(${progress})`,
                  textAlign: "center",
                }}
              >
                <div style={{ fontSize: 50, marginBottom: 15 }}>{feature.icon}</div>
                <h3 style={{ fontSize: 36, color: "#ffffff", marginBottom: 10 }}>
                  {feature.title}
                </h3>
                <p style={{ fontSize: 26, color: "#8b949e" }}>{feature.desc}</p>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景 4: 实战案例（6秒）
const ComparisonScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const leftProgress = spring({
    frame: frame - 20,
    fps,
    config: { damping: 100 },
  });

  const rightProgress = spring({
    frame: frame - 60,
    fps,
    config: { damping: 100 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0d1117",
        padding: 60,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ textAlign: "center", width: "100%" }}>
        <h2
          style={{
            fontSize: 56,
            fontWeight: "bold",
            color: "#ffffff",
            marginBottom: 50,
          }}
        >
          OpenClaw vs IronClaw
        </h2>

        <div style={{ display: "flex", flexDirection: "column", gap: 40, alignItems: "center" }}>
          {/* OpenClaw */}
          <div
            style={{
              backgroundColor: "#161b22",
              padding: 40,
              borderRadius: 15,
              opacity: leftProgress,
              transform: `translateX(${interpolate(leftProgress, [0, 1], [-100, 0])}px)`,
              textAlign: "left",
              width: "90%",
            }}
          >
            <h3 style={{ fontSize: 44, color: "#f66", marginBottom: 30 }}>
              OpenClaw
            </h3>
            <div style={{ fontSize: 30, color: "#8b949e", lineHeight: 1.8 }}>
              <p>• TypeScript</p>
              <p>• Docker 沙箱</p>
              <p>• 启动 ~6 秒</p>
            </div>
          </div>

          {/* IronClaw */}
          <div
            style={{
              backgroundColor: "#0366d6",
              padding: 40,
              borderRadius: 15,
              opacity: rightProgress,
              transform: `translateX(${interpolate(rightProgress, [0, 1], [100, 0])}px)`,
              textAlign: "left",
              width: "90%",
            }}
          >
            <h3 style={{ fontSize: 44, color: "#ffffff", marginBottom: 30 }}>
              IronClaw ✨
            </h3>
            <div style={{ fontSize: 30, color: "#ffffff", lineHeight: 1.8 }}>
              <p>• Rust</p>
              <p>• WASM 沙箱</p>
              <p>• 启动 &lt;1 秒</p>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景 5: 资源推荐（5秒）
const ResourceScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 100 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0d1117",
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
      }}
    >
      <div
        style={{
          textAlign: "center",
          opacity: progress,
          transform: `scale(${interpolate(progress, [0, 1], [0.8, 1])})`,
        }}
      >
        <div style={{ fontSize: 100, marginBottom: 30 }}>📦</div>
        <h2 style={{ fontSize: 56, color: "#0366d6", marginBottom: 30 }}>
          开源项目
        </h2>
        <div
          style={{
            backgroundColor: "#161b22",
            padding: "30px 50px",
            borderRadius: 15,
            marginBottom: 30,
          }}
        >
          <p style={{ fontSize: 32, color: "#58a6ff", fontFamily: "monospace" }}>
            github.com/nearai/ironclaw
          </p>
        </div>
        <div style={{ fontSize: 32, color: "#8b949e" }}>
          🌟 Stars: 500+
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景 6: 效率对比（5秒）
const PerformanceScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bar1Width = spring({
    frame: frame - 20,
    fps,
    config: { damping: 100 },
  });

  const bar2Width = spring({
    frame: frame - 40,
    fps,
    config: { damping: 100 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0d1117",
        padding: 60,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ textAlign: "center", width: "100%" }}>
        <h2
          style={{
            fontSize: 56,
            fontWeight: "bold",
            color: "#ffffff",
            marginBottom: 60,
          }}
        >
          📊 性能对比
        </h2>

        <div style={{ display: "flex", flexDirection: "column", gap: 50, alignItems: "center" }}>
          {/* 启动时间 */}
          <div style={{ width: "100%", textAlign: "left" }}>
            <div style={{ fontSize: 40, color: "#8b949e", marginBottom: 20 }}>
              启动时间
            </div>
            <div style={{ display: "flex", gap: 30, alignItems: "center", marginBottom: 20 }}>
              <div
                style={{
                  width: `${interpolate(bar1Width, [0, 1], [0, 500])}px`,
                  height: 60,
                  backgroundColor: "#f66",
                  borderRadius: 8,
                }}
              />
              <span style={{ fontSize: 36, color: "#ffffff" }}>~6 秒</span>
            </div>
            <div style={{ display: "flex", gap: 30, alignItems: "center" }}>
              <div
                style={{
                  width: `${interpolate(bar2Width, [0, 1], [0, 80])}px`,
                  height: 60,
                  backgroundColor: "#0366d6",
                  borderRadius: 8,
                }}
              />
              <span style={{ fontSize: 36, color: "#ffffff" }}>&lt;1 秒</span>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景 7: 行动号召（4秒）
const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 100 },
  });

  const scale = interpolate(
    frame,
    [0, 30, 60, 90, 120],
    [0.8, 1, 1, 1, 0.9]
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0366d6",
        justifyContent: "center",
        alignItems: "center",
        padding: 60,
      }}
    >
      <div
        style={{
          textAlign: "center",
          opacity: progress,
          transform: `scale(${scale})`,
        }}
      >
        <h2
          style={{
            fontSize: 64,
            fontWeight: "bold",
            color: "#ffffff",
            marginBottom: 50,
          }}
        >
          🚀 开始使用
        </h2>

        <div style={{ display: "flex", flexDirection: "column", gap: 25, alignItems: "center" }}>
          <div
            style={{
              backgroundColor: "rgba(255,255,255,0.2)",
              padding: "25px 40px",
              borderRadius: 12,
              fontSize: 32,
              color: "#ffffff",
            }}
          >
            brew install ironclaw
          </div>
          <div
            style={{
              backgroundColor: "rgba(255,255,255,0.2)",
              padding: "25px 40px",
              borderRadius: 12,
              fontSize: 32,
              color: "#ffffff",
            }}
          >
            ironclaw onboard
          </div>
        </div>

        <p
          style={{
            fontSize: 36,
            color: "#ffffff",
            marginTop: 50,
            opacity: 0.9,
          }}
        >
          🔒 值得更好的安全保护
        </p>
      </div>
    </AbsoluteFill>
  );
};

// 主组件
export const IronClawVideoVertical: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0d1117" }}>
      <Sequence from={0} durationInFrames={90}>
        <CoverScene />
      </Sequence>
      <Sequence from={90} durationInFrames={150}>
        <PainPointScene />
      </Sequence>
      <Sequence from={240} durationInFrames={180}>
        <FeaturesScene />
      </Sequence>
      <Sequence from={420} durationInFrames={180}>
        <ComparisonScene />
      </Sequence>
      <Sequence from={600} durationInFrames={150}>
        <ResourceScene />
      </Sequence>
      <Sequence from={750} durationInFrames={150}>
        <PerformanceScene />
      </Sequence>
      <Sequence from={900} durationInFrames={120}>
        <CtaScene />
      </Sequence>
    </AbsoluteFill>
  );
};
