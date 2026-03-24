import React from "react";
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame } from "remotion";

// 封面场景
const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  const titleOpacity = interpolate(frame, [30, 60], [0, 1]);
  const subtitleOpacity = interpolate(frame, [60, 90], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", opacity }}>
        <div
          style={{
            fontSize: 56,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 30,
            opacity: titleOpacity,
          }}
        >
          OpenClaw 多模型架构
        </div>
        <div
          style={{
            fontSize: 32,
            color: "#f0f0f0",
            opacity: subtitleOpacity,
          }}
        >
          支持 20+ AI 模型
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景1: 国际模型
const InternationalModels: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const models = ["OpenAI", "Claude", "Gemini", "xAI"];
  const modelOpacities = models.map((_, i) =>
    interpolate(frame, [30 + i * 30, 60 + i * 30], [0, 1])
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", width: "90%", maxWidth: 960 }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 40,
            opacity: titleOpacity,
          }}
        >
          🌍 国际模型
        </div>
        {models.map((model, i) => (
          <div
            key={model}
            style={{
              fontSize: 32,
              color: "#fff",
              marginBottom: 24,
              opacity: modelOpacities[i],
              backgroundColor: "#2a2a2a",
              padding: "16px 24px",
              borderRadius: 8,
            }}
          >
            {model}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景2: 国产模型
const DomesticModels: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const models = ["GLM (智谱)", "Kimi (月之暗面)", "MiniMax", "Qwen (通义)"];
  const modelOpacities = models.map((_, i) =>
    interpolate(frame, [30 + i * 30, 60 + i * 30], [0, 1])
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", width: "90%", maxWidth: 960 }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 40,
            opacity: titleOpacity,
          }}
        >
          🇨🇳 国产模型
        </div>
        {models.map((model, i) => (
          <div
            key={model}
            style={{
              fontSize: 32,
              color: "#fff",
              marginBottom: 24,
              opacity: modelOpacities[i],
              backgroundColor: "#2a2a2a",
              padding: "16px 24px",
              borderRadius: 8,
            }}
          >
            {model}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景3: 本地模型
const LocalModels: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const features = ["Ollama - 完全免费", "LM Studio - 可视化界面", "vLLM - 高性能推理", "完全离线运行"];
  const featureOpacities = features.map((_, i) =>
    interpolate(frame, [30 + i * 30, 60 + i * 30], [0, 1])
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", width: "90%", maxWidth: 960 }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 40,
            opacity: titleOpacity,
          }}
        >
          💻 本地模型
        </div>
        {features.map((feature, i) => (
          <div
            key={feature}
            style={{
              fontSize: 32,
              color: "#fff",
              marginBottom: 24,
              opacity: featureOpacities[i],
              backgroundColor: "#2a2a2a",
              padding: "16px 24px",
              borderRadius: 8,
            }}
          >
            {feature}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景4: 自定义 Provider
const CustomProviders: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const features = ["OpenRouter - 多模型代理", "Vercel AI Gateway", "自定义 API 端点", "灵活配置"];
  const featureOpacities = features.map((_, i) =>
    interpolate(frame, [30 + i * 30, 60 + i * 30], [0, 1])
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", width: "90%", maxWidth: 960 }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 40,
            opacity: titleOpacity,
          }}
        >
          🔌 自定义 Provider
        </div>
        {features.map((feature, i) => (
          <div
            key={feature}
            style={{
              fontSize: 32,
              color: "#fff",
              marginBottom: 24,
              opacity: featureOpacities[i],
              backgroundColor: "#2a2a2a",
              padding: "16px 24px",
              borderRadius: 8,
            }}
          >
            {feature}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景5: 两层降级机制
const TwoLayerFallback: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const layer1Opacity = interpolate(frame, [30, 60], [0, 1]);
  const layer2Opacity = interpolate(frame, [60, 90], [0, 1]);
  const descOpacity = interpolate(frame, [90, 120], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", width: "90%", maxWidth: 960 }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 40,
            opacity: titleOpacity,
          }}
        >
          🔄 两层降级机制
        </div>
        <div
          style={{
            fontSize: 32,
            color: "#4CAF50",
            marginBottom: 24,
            opacity: layer1Opacity,
            backgroundColor: "#2a2a2a",
            padding: "16px 24px",
            borderRadius: 8,
          }}
        >
          第1层: Auth Profile Rotation
        </div>
        <div
          style={{
            fontSize: 28,
            color: "#ccc",
            marginBottom: 24,
            opacity: layer1Opacity,
          }}
        >
          多个 API Key 自动轮换
        </div>
        <div
          style={{
            fontSize: 32,
            color: "#2196F3",
            marginBottom: 24,
            opacity: layer2Opacity,
            backgroundColor: "#2a2a2a",
            padding: "16px 24px",
            borderRadius: 8,
          }}
        >
          第2层: Model Fallback
        </div>
        <div
          style={{
            fontSize: 28,
            color: "#ccc",
            marginBottom: 24,
            opacity: layer2Opacity,
          }}
        >
          降级到备用模型
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景6: Cooldown 机制
const CooldownMechanism: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const items = [
    "临时错误: 1分钟 → 5分钟 → 25分钟 → 1小时",
    "计费失败: 5小时 → 10小时 → 24小时",
    "24小时无失败则重置",
    "状态持久化存储",
  ];
  const itemOpacities = items.map((_, i) =>
    interpolate(frame, [30 + i * 30, 60 + i * 30], [0, 1])
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", width: "90%", maxWidth: 960 }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 40,
            opacity: titleOpacity,
          }}
        >
          ⏰ Cooldown 机制
        </div>
        {items.map((item, i) => (
          <div
            key={item}
            style={{
              fontSize: 28,
              color: "#fff",
              marginBottom: 24,
              opacity: itemOpacities[i],
              backgroundColor: "#2a2a2a",
              padding: "16px 24px",
              borderRadius: 8,
            }}
          >
            {item}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景7: 成本优化建议
const CostOptimization: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const tips = [
    "快速响应: Cerebras / Groq",
    "高质量: Claude Opus / GLM-5",
    "创意写作: MiniMax",
    "开发测试: Ollama (免费)",
  ];
  const tipOpacities = tips.map((_, i) =>
    interpolate(frame, [30 + i * 30, 60 + i * 30], [0, 1])
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", width: "90%", maxWidth: 960 }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 40,
            opacity: titleOpacity,
          }}
        >
          💰 成本优化建议
        </div>
        {tips.map((tip, i) => (
          <div
            key={tip}
            style={{
              fontSize: 28,
              color: "#fff",
              marginBottom: 24,
              opacity: tipOpacities[i],
              backgroundColor: "#2a2a2a",
              padding: "16px 24px",
              borderRadius: 8,
            }}
          >
            {tip}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// 场景8: 配置示例
const ConfigExample: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const codeOpacity = interpolate(frame, [30, 60], [0, 1]);
  const descOpacity = interpolate(frame, [60, 90], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0a0a0a",
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
        fontFamily: "monospace, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", width: "90%", maxWidth: 960 }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 40,
            opacity: titleOpacity,
            fontFamily: "system-ui, sans-serif",
          }}
        >
          ⚙️ 配置示例
        </div>
        <div
          style={{
            fontSize: 20,
            color: "#4CAF50",
            marginBottom: 24,
            opacity: codeOpacity,
            backgroundColor: "#1a1a1a",
            padding: "20px",
            borderRadius: 8,
            textAlign: "left",
            lineHeight: 1.6,
          }}
        >
          {`{
  "model": {
    "primary": "zai/glm-5",
    "fallbacks": [
      "zai/glm-4.7",
      "minimax/MiniMax-M2.5"
    ]
  }
}`}
        </div>
        <div
          style={{
            fontSize: 28,
            color: "#ccc",
            opacity: descOpacity,
            fontFamily: "system-ui, sans-serif",
          }}
        >
          自动降级，保证服务可用性
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 总结场景
const SummaryScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const points = [
    "✅ 支持 20+ AI 模型",
    "✅ 两层智能降级",
    "✅ 自动 Cooldown 机制",
    "✅ 灵活的成本优化",
  ];
  const pointOpacities = points.map((_, i) =>
    interpolate(frame, [30 + i * 30, 60 + i * 30], [0, 1])
  );
  const nextOpacity = interpolate(frame, [150, 180], [0, 1]);

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        justifyContent: "center",
        alignItems: "center",
        padding: 48,
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div style={{ textAlign: "center", width: "90%", maxWidth: 960 }}>
        <div
          style={{
            fontSize: 48,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 40,
            opacity: titleOpacity,
          }}
        >
          📚 总结
        </div>
        {points.map((point, i) => (
          <div
            key={point}
            style={{
              fontSize: 28,
              color: "#fff",
              marginBottom: 24,
              opacity: pointOpacities[i],
              backgroundColor: "rgba(255,255,255,0.1)",
              padding: "16px 24px",
              borderRadius: 8,
            }}
          >
            {point}
          </div>
        ))}
        <div
          style={{
            fontSize: 32,
            color: "#f0f0f0",
            marginTop: 40,
            opacity: nextOpacity,
          }}
        >
          下一篇：Session 管理与上下文工程
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 主视频组件
export const MultiModelVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      <Sequence from={0} durationInFrames={90}>
        <CoverScene />
      </Sequence>
      <Sequence from={90} durationInFrames={150}>
        <InternationalModels />
      </Sequence>
      <Sequence from={240} durationInFrames={150}>
        <DomesticModels />
      </Sequence>
      <Sequence from={390} durationInFrames={150}>
        <LocalModels />
      </Sequence>
      <Sequence from={540} durationInFrames={150}>
        <CustomProviders />
      </Sequence>
      <Sequence from={690} durationInFrames={150}>
        <TwoLayerFallback />
      </Sequence>
      <Sequence from={840} durationInFrames={150}>
        <CooldownMechanism />
      </Sequence>
      <Sequence from={990} durationInFrames={150}>
        <CostOptimization />
      </Sequence>
      <Sequence from={1140} durationInFrames={150}>
        <ConfigExample />
      </Sequence>
      <Sequence from={1290} durationInFrames={150}>
        <SummaryScene />
      </Sequence>
    </AbsoluteFill>
  );
};
