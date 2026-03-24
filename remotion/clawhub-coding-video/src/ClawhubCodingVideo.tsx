import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Img,
} from 'remotion';

// 配色方案
const COLORS = {
  background: '#1a1a1a',
  primary: '#4CAF50',
  secondary: '#0366d6',
  accent: '#ff6b6b',
  text: '#ffffff',
  textSecondary: '#cccccc',
  card: '#2a2a2a',
};

// 动画辅助函数
const fadeIn = (frame: number, startFrame: number, duration: number = 15) => {
  return interpolate(frame - startFrame, [0, duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

const slideUp = (frame: number, startFrame: number, duration: number = 20) => {
  return interpolate(frame - startFrame, [0, duration], [50, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

// 场景1：封面场景
const CoverScene: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const opacity = fadeIn(frame, 0, 20);
  const scale = spring({ frame, fps, config: { damping: 100, stiffness: 200 } });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        height: '100%',
        transform: `scale(${scale})`,
      }}>
        <div style={{
          fontSize: 80,
          fontWeight: 'bold',
          color: COLORS.primary,
          marginBottom: 20,
        }}>
          💻 ClawHub 编程神器
        </div>
        <div style={{
          fontSize: 50,
          color: COLORS.text,
          marginBottom: 30,
        }}>
          133 个 AI 代码助手
        </div>
        <div style={{
          fontSize: 40,
          color: COLORS.secondary,
        }}>
          让你的开发效率翻 10 倍！
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景2：痛点场景
const PainPointScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);
  const titleY = slideUp(localFrame, 0, 20);
  const painPoints = [
    { icon: '❌', text: '代码写不完，Bug 改不停', delay: 5 },
    { icon: '❌', text: 'Code Review 占用大量时间', delay: 10 },
    { icon: '❌', text: '重构代码又怕改出问题', delay: 15 },
    { icon: '❌', text: '多个项目并行，脑子不够用', delay: 20 },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
      }}>
        <div style={{
          fontSize: 60,
          fontWeight: 'bold',
          color: COLORS.text,
          marginBottom: 40,
          transform: `translateY(${titleY}px)`,
        }}>
          程序员日常痛点
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 30 }}>
          {painPoints.map((point, index) => {
            const pointOpacity = fadeIn(localFrame, point.delay, 15);
            const pointY = slideUp(localFrame, point.delay, 20);
            return (
              <div key={index} style={{
                fontSize: 36,
                color: COLORS.textSecondary,
                opacity: pointOpacity,
                transform: `translateY(${pointY}px)`,
                display: 'flex',
                alignItems: 'center',
                gap: 15,
              }}>
                <span style={{ fontSize: 40 }}>{point.icon}</span>
                <span>{point.text}</span>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景3：功能介绍
const FeatureScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);

  const categories = [
    { icon: '🤖', title: 'AI 编程助手', desc: 'coding-agent、claude-team', color: COLORS.primary },
    { icon: '💻', title: '本地开发工具', desc: 'local-first-llm', color: COLORS.secondary },
    { icon: '🔒', title: '代码质量与安全', desc: 'security-scanner', color: COLORS.accent },
    { icon: '📊', title: '项目管理', desc: 'skill-factory-pipeline', color: '#9c27b0' },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{ padding: 60, height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div style={{
          fontSize: 60,
          fontWeight: 'bold',
          color: COLORS.text,
          marginBottom: 50,
        }}>
          133 个技能分类
        </div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: 30,
          flex: 1,
        }}>
          {categories.map((cat, index) => {
            const cardOpacity = fadeIn(localFrame, index * 8 + 5, 15);
            const cardY = slideUp(localFrame, index * 8 + 5, 20);
            return (
              <div key={index} style={{
                backgroundColor: COLORS.card,
                borderRadius: 15,
                padding: 30,
                opacity: cardOpacity,
                transform: `translateY(${cardY}px)`,
                borderLeft: `5px solid ${cat.color}`,
              }}>
                <div style={{ fontSize: 40, marginBottom: 15 }}>{cat.icon}</div>
                <div style={{
                  fontSize: 32,
                  fontWeight: 'bold',
                  color: COLORS.text,
                  marginBottom: 10,
                }}>
                  {cat.title}
                </div>
                <div style={{ fontSize: 24, color: COLORS.textSecondary }}>
                  {cat.desc}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景4：实战案例
const CaseStudyScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);

  const cases = [
    { title: '多 Agent 并行开发', improvement: '效率提升 3 倍', icon: '🚀' },
    { title: '自动 Code Review', improvement: '节省 80% 时间', icon: '⏱️' },
    { title: '本地 LLM 优先', improvement: '成本降低 90%', icon: '💰' },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{ padding: 60, height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div style={{
          fontSize: 60,
          fontWeight: 'bold',
          color: COLORS.text,
          marginBottom: 50,
        }}>
          实战案例
        </div>
        <div style={{ display: 'flex', gap: 40, flex: 1 }}>
          {cases.map((caseItem, index) => {
            const cardOpacity = fadeIn(localFrame, index * 10 + 10, 15);
            const cardScale = spring({
              frame: localFrame - index * 10,
              fps,
              config: { damping: 100, stiffness: 200 },
            });
            return (
              <div key={index} style={{
                flex: 1,
                backgroundColor: COLORS.card,
                borderRadius: 15,
                padding: 40,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                opacity: cardOpacity,
                transform: `scale(${cardScale})`,
              }}>
                <div style={{ fontSize: 60, marginBottom: 20 }}>{caseItem.icon}</div>
                <div style={{
                  fontSize: 32,
                  fontWeight: 'bold',
                  color: COLORS.text,
                  marginBottom: 20,
                  textAlign: 'center',
                }}>
                  {caseItem.title}
                </div>
                <div style={{
                  fontSize: 40,
                  fontWeight: 'bold',
                  color: COLORS.primary,
                }}>
                  {caseItem.improvement}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景5：热门编程工具
const ToolsScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);

  const tools = [
    { icon: '🤖', name: 'coding-agent', desc: 'AI 编程助手，支持 Codex/Claude Code', color: COLORS.primary },
    { icon: '👥', name: 'claude-team', desc: '多 Agent 并行开发', color: COLORS.secondary },
    { icon: '🔐', name: 'cc-godmode', desc: '8 Agent 编排 + 双质量门', color: COLORS.accent },
    { icon: '💻', name: 'local-first-llm', desc: '本地模型优先，成本降 90%', color: '#9c27b0' },
    { icon: '🔍', name: 'code-review-agent', desc: '自动 Code Review', color: '#ff9800' },
    { icon: '🛡️', name: 'security-scanner', desc: '安全漏洞扫描，68项检查', color: '#e91e63' },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{ padding: 50, height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: COLORS.text,
          marginBottom: 40,
        }}>
          🔥 热门编程工具
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 20, flex: 1 }}>
          {tools.map((tool, index) => {
            const cardOpacity = fadeIn(localFrame, index * 6 + 5, 12);
            const cardY = slideUp(localFrame, index * 6 + 5, 15);
            return (
              <div key={index} style={{
                backgroundColor: COLORS.card,
                borderRadius: 12,
                padding: 25,
                display: 'flex',
                alignItems: 'center',
                gap: 20,
                opacity: cardOpacity,
                transform: `translateY(${cardY}px)`,
                borderLeft: `4px solid ${tool.color}`,
              }}>
                <div style={{ fontSize: 36 }}>{tool.icon}</div>
                <div style={{ flex: 1 }}>
                  <div style={{
                    fontSize: 28,
                    fontWeight: 'bold',
                    color: COLORS.text,
                    marginBottom: 5,
                  }}>
                    {tool.name}
                  </div>
                  <div style={{ fontSize: 20, color: COLORS.textSecondary }}>
                    {tool.desc}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景6：ClawHub 平台介绍
const PlatformScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);
  const scale = spring({ frame: localFrame, fps, config: { damping: 100, stiffness: 200 } });

  const stats = [
    { value: '133+', label: '编程技能' },
    { value: '100%', label: '免费使用' },
    { value: '10x', label: '效率提升' },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        height: '100%',
        transform: `scale(${scale})`,
      }}>
        <div style={{
          fontSize: 70,
          fontWeight: 'bold',
          color: COLORS.primary,
          marginBottom: 20,
        }}>
          ClawHub
        </div>
        <div style={{
          fontSize: 36,
          color: COLORS.text,
          marginBottom: 50,
        }}>
          OpenClaw 技能市场
        </div>
        <div style={{ display: 'flex', gap: 60 }}>
          {stats.map((stat, index) => {
            const statOpacity = fadeIn(localFrame, index * 10 + 10, 15);
            return (
              <div key={index} style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                opacity: statOpacity,
              }}>
                <div style={{
                  fontSize: 60,
                  fontWeight: 'bold',
                  color: COLORS.secondary,
                }}>
                  {stat.value}
                </div>
                <div style={{
                  fontSize: 24,
                  color: COLORS.textSecondary,
                }}>
                  {stat.label}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景7：行动号召
const CTAScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);
  const scale = spring({ frame: localFrame, fps, config: { damping: 100, stiffness: 200 } });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        height: '100%',
        transform: `scale(${scale})`,
      }}>
        <div style={{
          fontSize: 70,
          fontWeight: 'bold',
          color: COLORS.primary,
          marginBottom: 30,
        }}>
          立即开始
        </div>
        <div style={{
          fontSize: 36,
          color: COLORS.text,
          marginBottom: 50,
        }}>
          3 步搞定
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {['npm i -g clawhub', 'clawhub install coding-agent', '开始编程 🚀'].map((step, index) => {
            const stepOpacity = fadeIn(localFrame, index * 10 + 10, 15);
            return (
              <div key={index} style={{
                backgroundColor: COLORS.card,
                borderRadius: 10,
                padding: '20px 40px',
                fontSize: 32,
                color: COLORS.text,
                fontFamily: 'monospace',
                opacity: stepOpacity,
              }}>
                {step}
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 主组件
export const ClawhubCodingVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 场景时间分配（总共270帧 = 9秒）
  // 场景1：0-89（3秒）封面
  // 场景2：90-209（4秒）痛点
  // 场景3：210-359（5秒）功能介绍
  // 场景4：360-509（5秒）热门工具
  // 场景5：510-659（5秒）实战案例
  // 场景6：660-779（4秒）ClawHub平台
  // 场景7：780-869（3秒）行动号召

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      {frame < 90 && <CoverScene frame={frame} fps={fps} />}
      {frame >= 90 && frame < 210 && <PainPointScene frame={frame} startFrame={90} fps={fps} />}
      {frame >= 210 && frame < 360 && <FeatureScene frame={frame} startFrame={210} fps={fps} />}
      {frame >= 360 && frame < 510 && <ToolsScene frame={frame} startFrame={360} fps={fps} />}
      {frame >= 510 && frame < 660 && <CaseStudyScene frame={frame} startFrame={510} fps={fps} />}
      {frame >= 660 && frame < 780 && <PlatformScene frame={frame} startFrame={660} fps={fps} />}
      {frame >= 780 && <CTAScene frame={frame} startFrame={780} fps={fps} />}
    </AbsoluteFill>
  );
};
