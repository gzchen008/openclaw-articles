import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from 'remotion';

// 配色方案
const COLORS = {
  background: '#1a1a1a',
  primary: '#FF6B6B',
  secondary: '#4ECDC4',
  accent: '#FFE66D',
  text: '#ffffff',
  textSecondary: '#cccccc',
  card: '#2a2a2a',
  highlight: '#FF6B6B',
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

// 场景1：封面（3秒 = 90帧）
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
        padding: 50,
      }}>
        <div style={{ fontSize: 80, marginBottom: 15 }}>🎨</div>
        <div style={{
          fontSize: 60,
          fontWeight: 'bold',
          color: COLORS.primary,
          marginBottom: 30,
          textAlign: 'center',
        }}>
          ClawHub 图片视频神器
        </div>
        <div style={{
          fontSize: 44,
          color: COLORS.text,
          marginBottom: 25,
          textAlign: 'center',
        }}>
          169 个 AI 创作工具
        </div>
        <div style={{
          fontSize: 36,
          color: COLORS.secondary,
          textAlign: 'center',
          padding: '20px 40px',
          backgroundColor: COLORS.card,
          borderRadius: 12,
        }}>
          让你的内容生产效率翻 10 倍！
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景2：痛点（4秒 = 120帧）
const PainPointScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);
  const titleY = slideUp(localFrame, 0, 20);
  
  const painPoints = [
    { icon: '😩', text: '找配图找到眼花，还怕版权问题' },
    { icon: '⏰', text: '想做个封面，PS 又不会用' },
    { icon: '😰', text: '视频剪辑太慢，一条视频搞半天' },
    { icon: '🤯', text: 'AI 工具太多，不知道选哪个' },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{
        padding: 50,
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
      }}>
        <div style={{
          fontSize: 52,
          fontWeight: 'bold',
          color: COLORS.accent,
          marginBottom: 50,
          textAlign: 'center',
          transform: `translateY(${titleY}px)`,
        }}>
          内容创作者日常痛点
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 30, width: '100%', maxWidth: 600 }}>
          {painPoints.map((point, index) => {
            const pointOpacity = fadeIn(localFrame, index * 10 + 10, 15);
            const pointY = slideUp(localFrame, index * 10 + 10, 20);
            return (
              <div key={index} style={{
                fontSize: 32,
                color: COLORS.text,
                opacity: pointOpacity,
                transform: `translateY(${pointY}px)`,
                display: 'flex',
                alignItems: 'center',
                gap: 18,
                backgroundColor: COLORS.card,
                padding: 25,
                borderRadius: 15,
                justifyContent: 'center',
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

// 场景3：分类（5秒 = 150帧）
const CategoryScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);

  const categories = [
    { icon: '🎨', title: 'AI 图片生成', tools: 'best-image\nbeauty-gen', color: COLORS.primary },
    { icon: '🎬', title: '视频创作工具', tools: 'ai-video-gen\nacestep-mv', color: COLORS.secondary },
    { icon: '🛠️', title: '设计工具整合', tools: 'canva-connect\nalgorithmic-art', color: COLORS.accent },
    { icon: '🎮', title: '3D 模型生成', tools: '3d-model-gen\ngltf-tools', color: '#9c27b0' },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{ padding: 50, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{
          fontSize: 48,
          fontWeight: 'bold',
          color: COLORS.text,
          marginBottom: 40,
          textAlign: 'center',
        }}>
          169 个技能分类
        </div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: 20,
          width: '100%',
          maxWidth: 600,
        }}>
          {categories.map((cat, index) => {
            const cardOpacity = fadeIn(localFrame, index * 8 + 5, 12);
            const cardScale = spring({
              frame: localFrame - index * 8,
              fps,
              config: { damping: 100, stiffness: 200 },
            });
            return (
              <div key={index} style={{
                backgroundColor: COLORS.card,
                borderRadius: 15,
                padding: 25,
                opacity: cardOpacity,
                transform: `scale(${cardScale})`,
                borderTop: `5px solid ${cat.color}`,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
              }}>
                <div style={{ fontSize: 40, marginBottom: 10 }}>{cat.icon}</div>
                <div style={{
                  fontSize: 22,
                  fontWeight: 'bold',
                  color: COLORS.text,
                  marginBottom: 10,
                  textAlign: 'center',
                }}>
                  {cat.title}
                </div>
                <div style={{ 
                  fontSize: 16, 
                  color: COLORS.textSecondary,
                  textAlign: 'center',
                  whiteSpace: 'pre-line',
                }}>
                  {cat.tools}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景4：热门图片工具（5秒 = 150帧）
const ImageToolsScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);

  const tools = [
    { icon: '🖼️', name: 'best-image', desc: '高质量 AI 图片生成', color: COLORS.primary },
    { icon: '🆓', name: 'beauty-generation-api', desc: '完全免费，适合日常使用', color: COLORS.secondary },
    { icon: '👤', name: 'ai-avatar-generation', desc: '从照片生成个性化头像', color: COLORS.accent },
    { icon: '📸', name: 'ai-headshot-generation', desc: '随手拍变职业照', color: '#9c27b0' },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{ padding: 50, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: COLORS.primary,
          marginBottom: 35,
          textAlign: 'center',
        }}>
          🎨 热门图片工具
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 22, width: '100%', maxWidth: 650 }}>
          {tools.map((tool, index) => {
            const cardOpacity = fadeIn(localFrame, index * 8 + 5, 12);
            const cardY = slideUp(localFrame, index * 8 + 5, 15);
            return (
              <div key={index} style={{
                backgroundColor: COLORS.card,
                borderRadius: 15,
                padding: 25,
                display: 'flex',
                alignItems: 'center',
                gap: 18,
                opacity: cardOpacity,
                transform: `translateY(${cardY}px)`,
                borderLeft: `6px solid ${tool.color}`,
                justifyContent: 'center',
              }}>
                <div style={{ fontSize: 40 }}>{tool.icon}</div>
                <div style={{ flex: 1, textAlign: 'center' }}>
                  <div style={{
                    fontSize: 28,
                    fontWeight: 'bold',
                    color: COLORS.text,
                    marginBottom: 6,
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

// 场景5：视频创作工具（5秒 = 150帧）
const VideoToolsScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);

  const tools = [
    { icon: '🎥', name: 'ai-video-gen', desc: '文字直接变视频', color: COLORS.primary },
    { icon: '🎵', name: 'acestep-simplemv', desc: '用歌词和音频生成 MV', color: COLORS.secondary },
    { icon: '🎮', name: '3d-model-generation', desc: '产品展示、游戏素材', color: COLORS.accent },
    { icon: '🎨', name: 'canva-connect', desc: 'AI 控制 Canva 设计', color: '#9c27b0' },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{ padding: 50, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: COLORS.secondary,
          marginBottom: 35,
          textAlign: 'center',
        }}>
          🎬 视频创作工具
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 22, width: '100%', maxWidth: 650 }}>
          {tools.map((tool, index) => {
            const cardOpacity = fadeIn(localFrame, index * 8 + 5, 12);
            const cardY = slideUp(localFrame, index * 8 + 5, 15);
            return (
              <div key={index} style={{
                backgroundColor: COLORS.card,
                borderRadius: 15,
                padding: 25,
                display: 'flex',
                alignItems: 'center',
                gap: 18,
                opacity: cardOpacity,
                transform: `translateY(${cardY}px)`,
                borderLeft: `6px solid ${tool.color}`,
                justifyContent: 'center',
              }}>
                <div style={{ fontSize: 40 }}>{tool.icon}</div>
                <div style={{ flex: 1, textAlign: 'center' }}>
                  <div style={{
                    fontSize: 28,
                    fontWeight: 'bold',
                    color: COLORS.text,
                    marginBottom: 6,
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

// 场景6：实战案例（5秒 = 150帧）
const CaseStudyScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);

  const cases = [
    { icon: '🚀', title: '公众号配图一键生成', improvement: '10 秒出图，无版权问题', color: COLORS.primary },
    { icon: '👤', title: '小红书头像快速制作', improvement: '30 秒生成 4 张不同风格', color: COLORS.secondary },
    { icon: '🎮', title: '产品 3D 展示视频', improvement: '直接生成可用的 3D 模型', color: COLORS.highlight },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background, opacity }}>
      <div style={{ padding: 50, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{
          fontSize: 48,
          fontWeight: 'bold',
          color: COLORS.text,
          marginBottom: 45,
          textAlign: 'center',
        }}>
          🎯 实战案例
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 30, width: '100%', maxWidth: 600 }}>
          {cases.map((caseItem, index) => {
            const cardOpacity = fadeIn(localFrame, index * 12 + 10, 15);
            const cardScale = spring({
              frame: localFrame - index * 12,
              fps,
              config: { damping: 100, stiffness: 200 },
            });
            return (
              <div key={index} style={{
                backgroundColor: COLORS.card,
                borderRadius: 18,
                padding: 30,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                opacity: cardOpacity,
                transform: `scale(${cardScale})`,
                borderBottom: `5px solid ${caseItem.color}`,
              }}>
                <div style={{ fontSize: 50, marginBottom: 15 }}>{caseItem.icon}</div>
                <div style={{
                  fontSize: 28,
                  fontWeight: 'bold',
                  color: COLORS.text,
                  marginBottom: 12,
                  textAlign: 'center',
                }}>
                  {caseItem.title}
                </div>
                <div style={{
                  fontSize: 24,
                  color: caseItem.color,
                  textAlign: 'center',
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

// 场景7：ClawHub 平台（4秒 = 120帧）
const PlatformScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);
  const scale = spring({ frame: localFrame, fps, config: { damping: 100, stiffness: 200 } });

  const stats = [
    { value: '169+', label: '创作工具', icon: '🎨' },
    { value: '100%', label: '免费使用', icon: '🎁' },
    { value: '100x', label: '效率提升', icon: '🚀' },
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
        padding: 50,
      }}>
        <div style={{
          fontSize: 68,
          fontWeight: 'bold',
          color: COLORS.primary,
          marginBottom: 15,
        }}>
          ClawHub
        </div>
        <div style={{
          fontSize: 32,
          color: COLORS.textSecondary,
          marginBottom: 60,
        }}>
          OpenClaw 技能市场
        </div>
        <div style={{ display: 'flex', gap: 40 }}>
          {stats.map((stat, index) => {
            const statOpacity = fadeIn(localFrame, index * 12 + 10, 15);
            const statScale = spring({
              frame: localFrame - index * 12,
              fps,
              config: { damping: 100, stiffness: 200 },
            });
            return (
              <div key={index} style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                opacity: statOpacity,
                transform: `scale(${statScale})`,
                backgroundColor: COLORS.card,
                padding: 25,
                borderRadius: 15,
                minWidth: 110,
              }}>
                <div style={{ fontSize: 36, marginBottom: 10 }}>{stat.icon}</div>
                <div style={{
                  fontSize: 44,
                  fontWeight: 'bold',
                  color: COLORS.secondary,
                }}>
                  {stat.value}
                </div>
                <div style={{
                  fontSize: 20,
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

// 场景8：行动号召（3秒 = 90帧）
const CTAScene: React.FC<{ frame: number; startFrame: number; fps: number }> = ({ frame, startFrame, fps }) => {
  const localFrame = frame - startFrame;
  const opacity = fadeIn(localFrame, 0, 15);
  const scale = spring({ frame: localFrame, fps, config: { damping: 100, stiffness: 200 } });

  const steps = [
    { cmd: 'npm i -g clawhub', desc: '安装 CLI' },
    { cmd: 'clawhub install beauty-generation-api', desc: '安装技能' },
    { cmd: '开始创作 🚀', desc: '立即使用' },
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
        padding: 50,
      }}>
        <div style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: COLORS.primary,
          marginBottom: 25,
        }}>
          立即开始
        </div>
        <div style={{
          fontSize: 30,
          color: COLORS.text,
          marginBottom: 45,
        }}>
          3 步搞定
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 18, width: '100%', maxWidth: 500 }}>
          {steps.map((step, index) => {
            const stepOpacity = fadeIn(localFrame, index * 12 + 10, 15);
            const stepScale = spring({
              frame: localFrame - index * 12,
              fps,
              config: { damping: 100, stiffness: 200 },
            });
            return (
              <div key={index} style={{
                backgroundColor: COLORS.card,
                borderRadius: 12,
                padding: '20px 25px',
                display: 'flex',
                alignItems: 'center',
                gap: 15,
                opacity: stepOpacity,
                transform: `scale(${stepScale})`,
                justifyContent: 'center',
              }}>
                <div style={{
                  backgroundColor: COLORS.primary,
                  color: COLORS.text,
                  width: 36,
                  height: 36,
                  borderRadius: 18,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 20,
                  fontWeight: 'bold',
                }}>
                  {index + 1}
                </div>
                <div style={{ flex: 1, textAlign: 'center' }}>
                  <div style={{
                    fontSize: 22,
                    fontWeight: 'bold',
                    color: COLORS.text,
                    fontFamily: 'monospace',
                  }}>
                    {step.cmd}
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

// 主组件（竖屏版本）
export const ImageVideoToolsVertical: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 场景时间分配（总共1020帧 = 34秒）
  // 场景1：0-89（3秒）封面
  // 场景2：90-209（4秒）痛点
  // 场景3：210-359（5秒）分类
  // 场景4：360-509（5秒）热门图片工具
  // 场景5：510-659（5秒）视频创作工具
  // 场景6：660-809（5秒）实战案例
  // 场景7：810-929（4秒）ClawHub平台
  // 场景8：930-1019（3秒）行动号召

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.background }}>
      {frame < 90 && <CoverScene frame={frame} fps={fps} />}
      {frame >= 90 && frame < 210 && <PainPointScene frame={frame} startFrame={90} fps={fps} />}
      {frame >= 210 && frame < 360 && <CategoryScene frame={frame} startFrame={210} fps={fps} />}
      {frame >= 360 && frame < 510 && <ImageToolsScene frame={frame} startFrame={360} fps={fps} />}
      {frame >= 510 && frame < 660 && <VideoToolsScene frame={frame} startFrame={510} fps={fps} />}
      {frame >= 660 && frame < 810 && <CaseStudyScene frame={frame} startFrame={660} fps={fps} />}
      {frame >= 810 && frame < 930 && <PlatformScene frame={frame} startFrame={810} fps={fps} />}
      {frame >= 930 && <CTAScene frame={frame} startFrame={930} fps={fps} />}
    </AbsoluteFill>
  );
};
