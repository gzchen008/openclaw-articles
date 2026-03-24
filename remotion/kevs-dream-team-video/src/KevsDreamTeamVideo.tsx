import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useVideoConfig,
  Img,
  interpolate,
  spring,
  useCurrentFrame,
} from "remotion";

// 场景 1：封面（3 秒 = 90 帧）
const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30, 60, 90], [0, 1, 1, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a1a", justifyContent: "center", alignItems: "center" }}>
      <Img
        src={require("../../../articles/video-cover.jpg")}
        style={{ width: "100%", height: "100%", objectFit: "cover", opacity }}
      />
    </AbsoluteFill>
  );
};

// 场景 2：痛点场景（5 秒 = 150 帧）
const PainPointScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const item1Opacity = interpolate(frame, [30, 60], [0, 1], { extrapolateRight: "clamp" });
  const item2Opacity = interpolate(frame, [60, 90], [0, 1], { extrapolateRight: "clamp" });
  const item3Opacity = interpolate(frame, [90, 120], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ 
      backgroundColor: "#1a1a1a", 
      padding: 60, 
      justifyContent: "center", 
      alignItems: "center",
      display: "flex",
      flexDirection: "column",
      textAlign: "center"
    }}>
      <div style={{ opacity: titleOpacity, marginBottom: 50 }}>
        <h1 style={{ fontSize: 64, color: "#fff", margin: 0, fontWeight: 700 }}>
          🤔 传统 AI 助手的问题
        </h1>
      </div>

      <div style={{ fontSize: 34, color: "#ccc", lineHeight: 2, maxWidth: 1400 }}>
        <p style={{ opacity: item1Opacity, margin: "20px 0" }}>
          ❌ <strong style={{ color: "#f66", fontSize: 38 }}>一个模型</strong> 做所有事情
        </p>
        <p style={{ opacity: item2Opacity, margin: "20px 0" }}>
          ❌ <strong style={{ color: "#f66", fontSize: 38 }}>效率低</strong> - 代码专家不擅长搜索
        </p>
        <p style={{ opacity: item3Opacity, margin: "20px 0" }}>
          ❌ <strong style={{ color: "#f66", fontSize: 38 }}>质量不稳定</strong> - 通用模型容易出错
        </p>
      </div>
    </AbsoluteFill>
  );
};

// 场景 3：解决方案（5 秒 = 150 帧）
const SolutionScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const subtitleOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateRight: "clamp" });
  const pointsOpacity = interpolate(frame, [60, 90], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ 
      backgroundColor: "#1a1a1a", 
      padding: 60, 
      justifyContent: "center", 
      alignItems: "center",
      display: "flex",
      flexDirection: "column",
      textAlign: "center"
    }}>
      <div style={{ opacity: titleOpacity, marginBottom: 30 }}>
        <h1 style={{ fontSize: 64, color: "#4CAF50", margin: 0, fontWeight: 700 }}>
          ✨ Kev's Dream Team
        </h1>
      </div>

      <div style={{ opacity: subtitleOpacity, marginBottom: 50 }}>
        <h2 style={{ fontSize: 44, color: "#fff", margin: 0, fontWeight: 600 }}>
          多 Agent 编排实战
        </h2>
      </div>

      <div style={{ opacity: pointsOpacity, fontSize: 34, color: "#ccc", lineHeight: 2, maxWidth: 1400 }}>
        <p style={{ margin: "18px 0" }}>✅ <strong style={{ color: "#4CAF50", fontSize: 38 }}>分工协作</strong> - 每个 Agent 专注自己领域</p>
        <p style={{ margin: "18px 0" }}>✅ <strong style={{ color: "#4CAF50", fontSize: 38 }}>模型选择</strong> - 按任务选最优模型</p>
        <p style={{ margin: "18px 0" }}>✅ <strong style={{ color: "#4CAF50", fontSize: 38 }}>自动编排</strong> - Orchestrator 协调所有 Agent</p>
      </div>
    </AbsoluteFill>
  );
};

// 场景 4：团队角色（5 秒 = 150 帧）
const TeamScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const agents = [
    { name: "🧠 Kev", role: "Orchestrator", model: "Opus 4.5", desc: "任务分配" },
    { name: "👷 Rex", role: "Engineer", model: "Codex GPT-5.2", desc: "代码专家" },
    { name: "🔒 Hawk", role: "Security", model: "Opus 4.5", desc: "安全审计" },
    { name: "🔎 Scout", role: "Research", model: "Gemini 3 Flash", desc: "快速搜索" },
    { name: "📊 Dash", role: "Analytics", model: "Data Model", desc: "数据分析" },
    { name: "⚙️ Dot", role: "DevOps", model: "IaC Specialist", desc: "运维部署" },
    { name: "🎨 Pixel", role: "Design", model: "Gemini 3 Pro", desc: "UI/UX设计" },
  ];

  return (
    <AbsoluteFill style={{ 
      backgroundColor: "#1a1a1a", 
      padding: 60, 
      justifyContent: "center", 
      alignItems: "center",
      display: "flex",
      flexDirection: "column",
      textAlign: "center"
    }}>
      <div style={{ opacity: titleOpacity, marginBottom: 40 }}>
        <h1 style={{ fontSize: 64, color: "#fff", margin: 0, fontWeight: 700 }}>
          🦞 7 个专业 Agent
        </h1>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 24, maxWidth: 1400 }}>
        {agents.map((agent, index) => {
          const opacity = interpolate(frame, [30 + index * 15, 60 + index * 15], [0, 1], {
            extrapolateRight: "clamp",
          });

          return (
            <div
              key={index}
              style={{
                opacity,
                background: "#2a2a2a",
                padding: 24,
                borderRadius: 12,
                borderLeft: "4px solid #4CAF50",
                textAlign: "left",
              }}
            >
              <p style={{ fontSize: 32, color: "#fff", margin: 0, fontWeight: 600 }}>
                {agent.name}
              </p>
              <p style={{ fontSize: 24, color: "#4CAF50", margin: "8px 0", fontWeight: 600 }}>
                {agent.role}
              </p>
              <p style={{ fontSize: 20, color: "#999", margin: "4px 0" }}>
                {agent.model} • {agent.desc}
              </p>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// 场景 5：技术实现（5 秒 = 150 帧）
const TechScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const tools = [
    { name: "sessions_spawn", desc: "派生子 Agent 并行执行" },
    { name: "模型选择", desc: "按任务选最优模型（Codex/Opus/Flash）" },
    { name: "Docker 沙箱", desc: "安全隔离，限制权限" },
    { name: "Heartbeat", desc: "定时主动工作，无需触发" },
    { name: "Webhooks", desc: "外部事件注入，实时响应" },
  ];

  return (
    <AbsoluteFill style={{ 
      backgroundColor: "#1a1a1a", 
      padding: 60, 
      justifyContent: "center", 
      alignItems: "center",
      display: "flex",
      flexDirection: "column",
      textAlign: "center"
    }}>
      <div style={{ opacity: titleOpacity, marginBottom: 40 }}>
        <h1 style={{ fontSize: 64, color: "#fff", margin: 0, fontWeight: 700 }}>
          🔧 核心技术
        </h1>
      </div>

      <div style={{ fontSize: 32, color: "#ccc", lineHeight: 2, maxWidth: 1400 }}>
        {tools.map((tool, index) => {
          const opacity = interpolate(frame, [30 + index * 20, 60 + index * 20], [0, 1], {
            extrapolateRight: "clamp",
          });

          return (
            <p key={index} style={{ opacity, margin: "20px 0" }}>
              ⚙️ <strong style={{ color: "#4CAF50", fontSize: 36 }}>{tool.name}</strong> - {tool.desc}
            </p>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// 场景 6：效率对比（5 秒 = 150 帧）
const EfficiencyScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const humanOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateRight: "clamp" });
  const agentOpacity = interpolate(frame, [60, 90], [0, 1], { extrapolateRight: "clamp" });
  const resultOpacity = interpolate(frame, [90, 120], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ 
      backgroundColor: "#1a1a1a", 
      padding: 60, 
      justifyContent: "center", 
      alignItems: "center",
      display: "flex",
      flexDirection: "column",
      textAlign: "center"
    }}>
      <div style={{ opacity: titleOpacity, marginBottom: 50 }}>
        <h1 style={{ fontSize: 64, color: "#fff", margin: 0, fontWeight: 700 }}>
          📊 效率对比
        </h1>
      </div>

      <div style={{ display: "flex", gap: 60, alignItems: "center", maxWidth: 1400 }}>
        <div style={{ opacity: humanOpacity, flex: 1, background: "#2a2a2a", padding: 40, borderRadius: 16 }}>
          <p style={{ fontSize: 32, color: "#ccc", margin: 0, marginBottom: 20, fontWeight: 600 }}>传统方式</p>
          <p style={{ fontSize: 56, color: "#f66", margin: 0, fontWeight: 700 }}>3 小时</p>
          <p style={{ fontSize: 24, color: "#999", margin: "16px 0 0 0", lineHeight: 1.6 }}>手动编写<br/>手动测试<br/>手动部署</p>
        </div>

        <div style={{ opacity: 1, fontSize: 72, color: "#4CAF50", fontWeight: 700 }}>→</div>

        <div style={{ opacity: agentOpacity, flex: 1, background: "#4CAF50", padding: 40, borderRadius: 16 }}>
          <p style={{ fontSize: 32, color: "#fff", margin: 0, marginBottom: 20, fontWeight: 600 }}>Dream Team</p>
          <p style={{ fontSize: 56, color: "#fff", margin: 0, fontWeight: 700 }}>3 分钟</p>
          <p style={{ fontSize: 24, color: "#e8f5e9", margin: "16px 0 0 0", lineHeight: 1.6 }}>自动编写<br/>自动测试<br/>自动部署</p>
        </div>
      </div>

      <div style={{ opacity: resultOpacity, marginTop: 50, textAlign: "center" }}>
        <p style={{ fontSize: 40, color: "#4CAF50", margin: 0, fontWeight: 700 }}>
          ⚡ 人类参与：15 秒
        </p>
        <p style={{ fontSize: 28, color: "#999", margin: "12px 0 0 0" }}>
          Agent 自动完成全流程
        </p>
      </div>
    </AbsoluteFill>
  );
};

// 场景 7：行动号召（5 秒 = 160 帧）
const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  const stepsOpacity = interpolate(frame, [30, 60], [0, 1], { extrapolateRight: "clamp" });
  const ctaOpacity = interpolate(frame, [60, 90], [0, 1], { extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ 
      backgroundColor: "#1a1a1a", 
      padding: 60, 
      justifyContent: "center", 
      alignItems: "center",
      display: "flex",
      flexDirection: "column",
      textAlign: "center"
    }}>
      <div style={{ opacity: titleOpacity, marginBottom: 50 }}>
        <h1 style={{ fontSize: 64, color: "#4CAF50", margin: 0, fontWeight: 700 }}>
          🚀 构建你的 Dream Team
        </h1>
      </div>

      <div style={{ opacity: stepsOpacity, fontSize: 34, color: "#ccc", lineHeight: 2, marginBottom: 50, maxWidth: 1400 }}>
        <p style={{ margin: "20px 0" }}>1️⃣ <strong style={{ color: "#4CAF50", fontSize: 38 }}>配置 Agent 列表</strong>（3-5 个专家）</p>
        <p style={{ margin: "20px 0" }}>2️⃣ <strong style={{ color: "#4CAF50", fontSize: 38 }}>使用 sessions_spawn</strong> 委托任务</p>
        <p style={{ margin: "20px 0" }}>3️⃣ <strong style={{ color: "#4CAF50", fontSize: 38 }}>设置 Heartbeat</strong> 主动工作</p>
      </div>

      <div
        style={{
          opacity: ctaOpacity,
          background: "#4CAF50",
          padding: 40,
          borderRadius: 16,
          textAlign: "center",
          maxWidth: 1200,
        }}
      >
        <p style={{ fontSize: 40, color: "#fff", margin: 0, fontWeight: 700 }}>
          🦞 OpenClaw - 让 AI 团队为你工作
        </p>
        <p style={{ fontSize: 28, color: "#e8f5e9", margin: "20px 0 0 0" }}>
          docs.openclaw.ai | discord.gg/clawd
        </p>
      </div>
    </AbsoluteFill>
  );
};

// 主视频组件（横屏，含封面）
export const KevsDreamTeamVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a1a" }}>
      <Sequence from={0} durationInFrames={90}>
        <CoverScene />
      </Sequence>

      <Sequence from={90} durationInFrames={150}>
        <PainPointScene />
      </Sequence>

      <Sequence from={240} durationInFrames={150}>
        <SolutionScene />
      </Sequence>

      <Sequence from={390} durationInFrames={150}>
        <TeamScene />
      </Sequence>

      <Sequence from={540} durationInFrames={150}>
        <TechScene />
      </Sequence>

      <Sequence from={690} durationInFrames={150}>
        <EfficiencyScene />
      </Sequence>

      <Sequence from={840} durationInFrames={160}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};

// 竖屏版本（无封面）
export const KevsDreamTeamVideoVertical: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a1a" }}>
      <Sequence from={0} durationInFrames={150}>
        <PainPointScene />
      </Sequence>

      <Sequence from={150} durationInFrames={150}>
        <SolutionScene />
      </Sequence>

      <Sequence from={300} durationInFrames={150}>
        <TeamScene />
      </Sequence>

      <Sequence from={450} durationInFrames={150}>
        <TechScene />
      </Sequence>

      <Sequence from={600} durationInFrames={150}>
        <EfficiencyScene />
      </Sequence>

      <Sequence from={750} durationInFrames={160}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
