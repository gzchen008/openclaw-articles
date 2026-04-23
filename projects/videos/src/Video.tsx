import React, { useCallback } from 'react';
import { AbsoluteFill, Video, Sequence, useCurrentFrame, spring } from 'remotion';

// Video configuration
const DURATION = 30; // 30 seconds
const WIDTH = 1920;
const HEIGHT = 1080;

// Feature data
const FEATURES = [
  {
    title: "任务管理革新",
    description: "/tasks 聊天原生任务板",
    subtitle: "实时显示当前会话任务详情"
  },
  {
    title: "Web搜索增强", 
    description: "集成 SearXNG 提供商",
    subtitle: "强大的本地化搜索能力"
  },
  {
    title: "Amazon Bedrock",
    description: "Guardrails 支持",
    subtitle: "企业级内容安全防护"
  },
  {
    title: "macOS 语音唤醒",
    description: "Talk Mode 激活",
    subtitle: "提升交互体验"
  },
  {
    title: "飞书评论系统",
    description: "Drive评论事件流",
    subtitle: "完善文档协作工作流"
  }
];

export const VideoComponent: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: '#1a1a2e' }}>
      <div
        style={{
          width: WIDTH,
          height: HEIGHT,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          color: 'white',
          fontFamily: 'Arial, sans-serif',
        }}
      >
        {/* Cover Scene (0-3 seconds) */}
        <Sequence from={0} duration={90}>
          <div
            style={{
              opacity: spring({
                frame,
                fps: 30,
                config: {
                  damping: 15,
                },
              }),
              textAlign: 'center',
            }}
          >
            <h1
              style={{
                fontSize: 80,
                marginBottom: 20,
                background: 'linear-gradient(45deg, #667eea, #764ba2)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              OpenClaw 2026.4.1
            </h1>
            <p
              style={{
                fontSize: 40,
                color: '#e0e0e0',
                marginTop: 20,
              }}
            >
              重大功能更新与性能优化
            </p>
          </div>
        </Sequence>

        {/* Feature Scenes (3-27 seconds) */}
        {FEATURES.map((feature, index) => (
          <Sequence
            key={index}
            from={90 + index * 144} // Start each feature after previous one
            duration={144} // 4.8 seconds per feature
          >
            <div
              style={{
                opacity: spring({
                  frame: frame - (90 + index * 144),
                  fps: 30,
                  config: {
                    damping: 15,
                  },
                  delay: 15,
                }),
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                width: '100%',
                textAlign: 'center',
                padding: '0 100px',
              }}
            >
              <h2
                style={{
                  fontSize: 60,
                  marginBottom: 20,
                  color: '#64b5f6',
                }}
              >
                {feature.title}
              </h2>
              <p
                style={{
                  fontSize: 36,
                  marginBottom: 15,
                  color: '#90caf9',
                }}
              >
                {feature.description}
              </p>
              <p
                style={{
                  fontSize: 28,
                  color: '#e0e0e0',
                  fontStyle: 'italic',
                }}
              >
                {feature.subtitle}
              </p>
              
              {/* Animated tech stack icons */}
              <div
                style={{
                  marginTop: 40,
                  display: 'flex',
                  gap: 20,
                }}
              >
                <div
                  style={{
                    width: 60,
                    height: 60,
                    backgroundColor: 'rgba(100, 181, 246, 0.2)',
                    borderRadius: 12,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 24,
                    color: '#64b5f6',
                  }}
                >
                  AI
                </div>
                <div
                  style={{
                    width: 60,
                    height: 60,
                    backgroundColor: 'rgba(129, 199, 132, 0.2)',
                    borderRadius: 12,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 24,
                    color: '#81c784',
                  }}
                >
                  API
                </div>
                <div
                  style={{
                    width: 60,
                    height: 60,
                    backgroundColor: 'rgba(255, 167, 38, 0.2)',
                    borderRadius: 12,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 24,
                    color: '#ffa726',
                  }}
                >
                  CLI
                </div>
              </div>
            </div>
          </Sequence>
        ))}

        {/* Final CTA Scene (27-30 seconds) */}
        <Sequence from={900} duration={90}>
          <div
            style={{
              opacity: spring({
                frame: frame - 900,
                fps: 30,
                config: {
                  damping: 15,
                },
              }),
              textAlign: 'center',
            }}
          >
            <h1
              style={{
                fontSize: 70,
                marginBottom: 20,
                background: 'linear-gradient(45deg, #4caf50, #81c784)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              立即升级
            </h1>
            <p
              style={{
                fontSize: 40,
                color: '#e0e0e0',
                marginBottom: 30,
              }}
            >
              体验更强大的 AI 编程助手
            </p>
            <div
              style={{
                display: 'inline-block',
                backgroundColor: '#4caf50',
                color: 'white',
                padding: '15px 40px',
                borderRadius: 30,
                fontSize: 24,
                fontWeight: 'bold',
              }}
            >
              OpenClaw 2026.4.1
            </div>
          </div>
        </Sequence>
      </div>
    </AbsoluteFill>
  );
};