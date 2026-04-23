import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  interpolate,
} from "remotion";

const BG = "#0a0a1a";
const ACCENT = "#6C5CE7";
const ACCENT2 = "#00CEC9";
const WHITE = "#FFFFFF";
const GRAY = "#A0A0B8";
const FPS = 30;

const FadeIn: React.FC<{ children: React.ReactNode; delay?: number }> = ({
  children,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame - delay, [0, 25], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return <div style={{ opacity }}>{children}</div>;
};

const Title: React.FC<{
  children: React.ReactNode;
  size?: number;
  color?: string;
  delay?: number;
  weight?: number;
}> = ({ children, size = 72, color = WHITE, delay = 0, weight = 700 }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame - delay, [0, 25], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div
      style={{
        opacity,
        fontSize: size,
        fontWeight: weight,
        color,
        textAlign: "center",
        lineHeight: 1.3,
        padding: "0 60px",
      }}
    >
      {children}
    </div>
  );
};

const Bullet: React.FC<{
  text: string;
  delay: number;
  icon?: string;
}> = ({ text, delay, icon = "●" }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame - delay, [0, 25], [0, 1], {
    extrapolLeftLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div
      style={{
        opacity,
        display: "flex",
        alignItems: "center",
        gap: 20,
        marginBottom: 28,
        padding: "0 80px",
      }}
    >
      <span style={{ color: ACCENT2, fontSize: 36, minWidth: 50, textAlign: "center" }}>{icon}</span>
      <span style={{ color: GRAY, fontSize: 44, lineHeight: 1.4 }}>{text}</span>
    </div>
  );
};

const Divider: React.FC<{ delay?: number }> = ({ delay = 0 }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame - delay, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div
      style={{
        opacity,
        width: 140,
        height: 4,
        background: `linear-gradient(90deg, ${ACCENT}, ${ACCENT2})`,
        borderRadius: 2,
        margin: "28px auto",
      }}
    />
  );
};

const LogoMark: React.FC<{ delay?: number; size?: number }> = ({ delay = 0, size = 200 }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame - delay, [0, 25], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <FadeIn delay={delay}>
      <div
        style={{
          width: size,
          height: size,
          borderRadius: 50,
          background: `linear-gradient(135deg, ${ACCENT}, ${ACCENT2})`,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          marginBottom: 48,
          boxShadow: `0 0 100px ${ACCENT}40`,
        }}
      >
        <span style={{ fontSize: size * 0.45, color: WHITE, fontWeight: 800 }}>D</span>
      </div>
    </FadeIn>
  );
};

const SceneNumber: React.FC<{ num: string; delay?: number }> = ({ num, delay = 0 }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame - delay, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div style={{
      position: "absolute",
      top: 80,
      left: 80,
      opacity,
      fontSize: 48,
      fontWeight: 800,
      color: `${ACCENT}30`,
    }}>
      {num}
    </div>
  );
};

// Scene 1: Cover (10s = 300 frames)
const CoverScene: React.FC = () => (
  <AbsoluteFill
    style={{
      background: `linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 50%, #0a0a1a 100%)`,
      justifyContent: "center",
      alignItems: "center",
    }}
  >
    <LogoMark delay={0} size={220} />
    <Title size={100} delay={10} weight={800}>Dokobot</Title>
    <Divider delay={20} />
    <Title size={44} color={GRAY} delay={28} weight={400}>
      隐私优先的浏览器抓取工具
    </Title>
    <FadeIn delay={45}>
      <div style={{
        marginTop: 80,
        padding: "14px 48px",
        borderRadius: 32,
        border: `2px solid ${ACCENT}60`,
        color: ACCENT2,
        fontSize: 34,
      }}>
        免费开源 · 本地运行 · 无需注册
      </div>
    </FadeIn>
    <FadeIn delay={60}>
      <div style={{ position: "absolute", bottom: 120, fontSize: 28, color: `${GRAY}60` }}>
        dokobot.ai
      </div>
    </FadeIn>
  </AbsoluteFill>
);

// Scene 2: Privacy (8s)
const PrivacyScene: React.FC = () => (
  <AbsoluteFill style={{ background: BG, justifyContent: "center", alignItems: "center" }}>
    <SceneNumber num="01" delay={0} />
    <Title size={60} delay={0} weight={700} color={ACCENT}>🔒 隐私是一切的核心</Title>
    <Divider delay={10} />
    <div style={{ marginTop: 50 }}>
      <Bullet text="本地优先，无需登录" delay={18} icon="🖥" />
      <Bullet text="AES-256-GCM 端到端加密" delay={35} icon="🔐" />
      <Bullet text="内容绝不存储，即用即销" delay={52} icon="💨" />
      <Bullet text="支付页面和验证码完全排除" delay={69} icon="🛡" />
    </div>
    <FadeIn delay={85}>
      <div style={{ marginTop: 40, fontSize: 32, color: `${GRAY}50`, padding: "0 60px", textAlign: "center" }}>
        数据始终在你的掌控之中
      </div>
    </FadeIn>
  </AbsoluteFill>
);

// Scene 3: Pixel Vision (8s)
const PixelVisionScene: React.FC = () => (
  <AbsoluteFill style={{ background: BG, justifyContent: "center", alignItems: "center" }}>
    <SceneNumber num="02" delay={0} />
    <Title size={60} delay={0} weight={700} color={ACCENT2}>👁 像素级视觉提取</Title>
    <Divider delay={10} />
    <div style={{ marginTop: 50 }}>
      <Bullet text="基于视觉，而非 DOM 树" delay={18} icon="🎯" />
      <Bullet text="无需站点适配器，任意网页通用" delay={35} icon="🌐" />
      <Bullet text="HTML/CSS 改版完全不影响" delay={52} icon="🛡" />
    </div>
    <FadeIn delay={70}>
      <div style={{
        marginTop: 50,
        padding: "20px 50px",
        borderRadius: 20,
        background: `linear-gradient(135deg, ${ACCENT2}10, ${ACCENT2}05)`,
        border: `1px solid ${ACCENT2}30`,
        fontSize: 34,
        color: GRAY,
        textAlign: "center",
      }}>
        你看到的，它都能提取
      </div>
    </FadeIn>
  </AbsoluteFill>
);

// Scene 4: Auto Scroll (8s)
const AutoScrollScene: React.FC = () => (
  <AbsoluteFill style={{ background: BG, justifyContent: "center", alignItems: "center" }}>
    <SceneNumber num="03" delay={0} />
    <Title size={60} delay={0} weight={700} color={ACCENT}>📜 自动滚动续读无忧</Title>
    <Divider delay={10} />
    <div style={{ marginTop: 50 }}>
      <Bullet text="智能自动滚动 + 懒加载检测" delay={18} icon="⚡" />
      <Bullet text="会话级续读，暂停精确恢复" delay={35} icon="📌" />
      <Bullet text="自适应检测，无内容提前停止" delay={52} icon="🧠" />
    </div>
    <FadeIn delay={70}>
      <div style={{
        marginTop: 50,
        padding: "20px 50px",
        borderRadius: 20,
        background: `linear-gradient(135deg, ${ACCENT}10, ${ACCENT}05)`,
        border: `1px solid ${ACCENT}30`,
        fontSize: 34,
        color: GRAY,
        textAlign: "center",
      }}>
        长页面、无限滚动？统统搞定
      </div>
    </FadeIn>
  </AbsoluteFill>
);

// Scene 5: LLM Ready (8s)
const LLMReadyScene: React.FC = () => (
  <AbsoluteFill style={{ background: BG, justifyContent: "center", alignItems: "center" }}>
    <SceneNumber num="04" delay={0} />
    <Title size={60} delay={0} weight={700} color={ACCENT2}>🤖 任意网页 LLM 直接可用</Title>
    <Divider delay={10} />
    <div style={{ marginTop: 50 }}>
      <Bullet text="按栏分组，保留页面实际布局" delay={18} icon="📊" />
      <Bullet text="图片提取 + 链接编号引用" delay={35} icon="🔗" />
    </div>
    <FadeIn delay={55}>
      <div style={{
        marginTop: 60,
        padding: "24px 70px",
        borderRadius: 24,
        background: `linear-gradient(135deg, ${ACCENT}15, ${ACCENT2}15)`,
        border: `2px solid ${ACCENT2}40`,
      }}>
        <span style={{ fontSize: 60, fontWeight: 800, color: ACCENT2 }}>
          Token 减少 99%
        </span>
      </div>
    </FadeIn>
    <FadeIn delay={80}>
      <div style={{ marginTop: 30, fontSize: 30, color: `${GRAY}50`, textAlign: "center" }}>
        干净的结构化输出，LLM 一目了然
      </div>
    </FadeIn>
  </AbsoluteFill>
);

// Scene 6: Pricing (8s)
const PricingScene: React.FC = () => (
  <AbsoluteFill style={{ background: BG, justifyContent: "center", alignItems: "center" }}>
    <SceneNumber num="05" delay={0} />
    <Title size={60} delay={0} weight={700} color={ACCENT}>💰 免费无限抓取</Title>
    <Divider delay={10} />
    <FadeIn delay={18}>
      <div style={{
        marginTop: 40,
        padding: "28px 60px",
        borderRadius: 24,
        background: `linear-gradient(135deg, ${ACCENT}15, ${ACCENT2}15)`,
        border: `2px solid ${ACCENT}40`,
        textAlign: "center",
      }}>
        <div style={{ fontSize: 38, color: GRAY, marginBottom: 16 }}>Dokobot 本地模式</div>
        <div style={{ fontSize: 64, fontWeight: 800, color: WHITE }}>完全免费</div>
        <div style={{ fontSize: 34, color: GRAY, marginTop: 12 }}>无限抓取 · 无需注册 · 无限制</div>
      </div>
    </FadeIn>
    <FadeIn delay={40}>
      <div style={{ marginTop: 50, fontSize: 30, color: GRAY, padding: "0 60px", textAlign: "center", lineHeight: 1.8 }}>
        远程模式仅需 <span style={{ color: ACCENT2, fontWeight: 700 }}>$9.90/月</span><br />
        Firecrawl $16 · Browserbase $20 · Apify $29
      </div>
    </FadeIn>
  </AbsoluteFill>
);

// Scene 7: Your Browser (8s)
const BrowserScene: React.FC = () => (
  <AbsoluteFill style={{ background: BG, justifyContent: "center", alignItems: "center" }}>
    <SceneNumber num="06" delay={0} />
    <Title size={60} delay={0} weight={700} color={ACCENT2}>🌐 你的浏览器随处可达</Title>
    <Divider delay={10} />
    <div style={{ marginTop: 50 }}>
      <Bullet text="一个 API 调度多个浏览器" delay={18} icon="🔗" />
      <Bullet text="登录墙、JS 渲染、反爬全支持" delay={35} icon="🔓" />
      <Bullet text="复用浏览器登录态" delay={52} icon="🔑" />
      <Bullet text="内网站点一键抓取" delay={69} icon="🏢" />
    </div>
  </AbsoluteFill>
);

// Scene 8: Agent (8s)
const AgentScene: React.FC = () => (
  <AbsoluteFill style={{ background: BG, justifyContent: "center", alignItems: "center" }}>
    <SceneNumber num="07" delay={0} />
    <Title size={60} delay={0} weight={700} color={ACCENT}>🤝 Agent 的最佳搭档</Title>
    <Divider delay={10} />
    <div style={{ marginTop: 50 }}>
      <Bullet text="Claude Code / OpenClaw / 任何 MCP Agent" delay={18} icon="🤖" />
      <Bullet text="doko read — 读取任意网页" delay={35} icon="📖" />
      <Bullet text="doko search — 搜索全网信息" delay={52} icon="🔍" />
    </div>
    <FadeIn delay={70}>
      <div style={{ marginTop: 40, fontSize: 30, color: `${GRAY}50`, textAlign: "center" }}>
        一个 Skill，全部搞定
      </div>
    </FadeIn>
  </AbsoluteFill>
);

// Scene 9: CTA (8s)
const CTAScene: React.FC = () => (
  <AbsoluteFill
    style={{
      background: `linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 50%, #0a0a1a 100%)`,
      justifyContent: "center",
      alignItems: "center",
    }}
  >
    <LogoMark delay={0} size={180} />
    <Title size={70} delay={12} weight={800}>立即体验 Dokobot</Title>
    <Divider delay={22} />
    <FadeIn delay={32}>
      <div style={{
        marginTop: 50,
        padding: "18px 60px",
        borderRadius: 32,
        background: `linear-gradient(135deg, ${ACCENT}, ${ACCENT2})`,
        fontSize: 44,
        fontWeight: 700,
        color: WHITE,
        boxShadow: `0 0 80px ${ACCENT}40`,
      }}>
        dokobot.ai
      </div>
    </FadeIn>
    <FadeIn delay={55}>
      <div style={{ marginTop: 50, fontSize: 32, color: GRAY, textAlign: "center", lineHeight: 1.8 }}>
        Chrome 扩展商店免费安装<br />
        隐私优先 · 开源免费 · 本地运行
      </div>
    </FadeIn>
    <FadeIn delay={80}>
      <div style={{ position: "absolute", bottom: 100, fontSize: 28, color: `${ACCENT2}80` }}>
        ⭐ 欢迎评分和推荐
      </div>
    </FadeIn>
  </AbsoluteFill>
);

export const DokobotVideo: React.FC = () => {
  const sceneDur = 240; // 8s per scene
  return (
    <AbsoluteFill style={{ backgroundColor: BG }}>
      <Sequence from={0} durationInFrames={300}>
        <CoverScene />
      </Sequence>
      <Sequence from={300} durationInFrames={sceneDur}>
        <PrivacyScene />
      </Sequence>
      <Sequence from={540} durationInFrames={sceneDur}>
        <PixelVisionScene />
      </Sequence>
      <Sequence from={780} durationInFrames={sceneDur}>
        <AutoScrollScene />
      </Sequence>
      <Sequence from={1020} durationInFrames={sceneDur}>
        <LLMReadyScene />
      </Sequence>
      <Sequence from={1260} durationInFrames={sceneDur}>
        <PricingScene />
      </Sequence>
      <Sequence from={1500} durationInFrames={sceneDur}>
        <BrowserScene />
      </Sequence>
      <Sequence from={1740} durationInFrames={sceneDur}>
        <AgentScene />
      </Sequence>
      <Sequence from={1980} durationInFrames={sceneDur}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
