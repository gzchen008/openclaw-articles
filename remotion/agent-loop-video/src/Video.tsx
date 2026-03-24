import React from 'react';
import {AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

// 场景1: 封面
const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {clamp: true});
  
  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      justifyContent: 'center',
      alignItems: 'center',
      padding: 40,
    }}>
      <div style={{
        opacity,
        textAlign: 'center',
        color: 'white',
      }}>
        <h1 style={{
          fontSize: 60,
          fontWeight: 700,
          margin: 0,
          marginBottom: 20,
        }}>
          Agent Loop
        </h1>
        <p style={{
          fontSize: 32,
          margin: 0,
          opacity: 0.9,
        }}>
          从消息到回复的完整旅程
        </p>
        <p style={{
          fontSize: 24,
          marginTop: 30,
          opacity: 0.7,
        }}>
          OpenClaw 源码解读 第2篇
        </p>
      </div>
    </AbsoluteFill>
  );
};

// 场景2-9: 步骤卡片
interface StepProps {
  number: string;
  emoji: string;
  title: string;
  description: string;
  details: string[];
}

const StepScene: React.FC<StepProps> = ({number, emoji, title, description, details}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], {clamp: true});
  
  return (
    <AbsoluteFill style={{
      background: '#f6f8fa',
      justifyContent: 'center',
      alignItems: 'center',
      padding: 60,
    }}>
      <div style={{
        opacity,
        width: '100%',
        maxWidth: 900,
      }}>
        {/* 步骤编号 */}
        <div style={{
          background: '#0366d6',
          color: 'white',
          width: 80,
          height: 80,
          borderRadius: 40,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontSize: 36,
          fontWeight: 700,
          marginBottom: 30,
        }}>
          {number}
        </div>
        
        {/* 标题 */}
        <h2 style={{
          fontSize: 48,
          fontWeight: 700,
          color: '#24292e',
          margin: 0,
          marginBottom: 20,
        }}>
          {emoji} {title}
        </h2>
        
        {/* 描述 */}
        <p style={{
          fontSize: 32,
          color: '#586069',
          margin: 0,
          marginBottom: 30,
          lineHeight: 1.5,
        }}>
          {description}
        </p>
        
        {/* 详情列表 */}
        <div style={{
          background: 'white',
          padding: 30,
          borderRadius: 12,
          border: '2px solid #e1e4e8',
        }}>
          {details.map((detail, index) => (
            <p key={index} style={{
              fontSize: 26,
              color: '#24292e',
              margin: 0,
              marginBottom: index < details.length - 1 ? 15 : 0,
              paddingLeft: 20,
            }}>
              • {detail}
            </p>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 场景10: 总结
const SummaryScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], {clamp: true});
  
  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      justifyContent: 'center',
      alignItems: 'center',
      padding: 60,
    }}>
      <div style={{
        opacity,
        textAlign: 'center',
        color: 'white',
      }}>
        <h2 style={{
          fontSize: 48,
          fontWeight: 700,
          margin: 0,
          marginBottom: 40,
        }}>
          🎓 Agent Loop 设计哲学
        </h2>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 20,
          marginBottom: 40,
        }}>
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            padding: 20,
            borderRadius: 12,
          }}>
            <p style={{fontSize: 24, margin: 0, fontWeight: 600}}>串行化</p>
            <p style={{fontSize: 20, margin: 0, marginTop: 10, opacity: 0.9}}>保证一致性</p>
          </div>
          
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            padding: 20,
            borderRadius: 12,
          }}>
            <p style={{fontSize: 24, margin: 0, fontWeight: 600}}>流式输出</p>
            <p style={{fontSize: 20, margin: 0, marginTop: 10, opacity: 0.9}}>提升体验</p>
          </div>
          
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            padding: 20,
            borderRadius: 12,
          }}>
            <p style={{fontSize: 24, margin: 0, fontWeight: 600}}>Hook 系统</p>
            <p style={{fontSize: 20, margin: 0, marginTop: 10, opacity: 0.9}}>提供扩展性</p>
          </div>
          
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            padding: 20,
            borderRadius: 12,
          }}>
            <p style={{fontSize: 24, margin: 0, fontWeight: 600}}>多层容错</p>
            <p style={{fontSize: 20, margin: 0, marginTop: 10, opacity: 0.9}}>稳定可靠</p>
          </div>
        </div>
        
        <p style={{
          fontSize: 28,
          margin: 0,
          opacity: 0.8,
        }}>
          📖 查看完整文章：github.com/gzchen008/openclaw-articles
        </p>
      </div>
    </AbsoluteFill>
  );
};

// 主视频组件
export const AgentLoopVideo: React.FC = () => {
  const {fps} = useVideoConfig();
  
  return (
    <>
      {/* 场景1: 封面 (3秒) */}
      <Sequence from={0} durationInFrames={fps * 3}>
        <CoverScene />
      </Sequence>
      
      {/* 场景2: 步骤1 (5秒) */}
      <Sequence from={fps * 3} durationInFrames={fps * 5}>
        <StepScene
          number="1"
          emoji="📥"
          title="入口层"
          description="用户消息到达"
          details={[
            '来源：WhatsApp / Telegram / Discord',
            '方式：Gateway RPC（异步）或 CLI agent（同步）',
            '特点：立即返回 runId，不阻塞',
          ]}
        />
      </Sequence>
      
      {/* 场景3: 步骤2 (5秒) */}
      <Sequence from={fps * 8} durationInFrames={fps * 5}>
        <StepScene
          number="2"
          emoji="🔧"
          title="会话准备"
          description="准备运行环境"
          details={[
            '解析 sessionKey，找到对应会话',
            '加载当前激活的 Skills（技能快照）',
            '注入引导文件：AGENTS.md / SOUL.md / MEMORY.md',
            '获取会话写锁，防止并发冲突',
          ]}
        />
      </Sequence>
      
      {/* 场景4: 步骤3 (5秒) */}
      <Sequence from={fps * 13} durationInFrames={fps * 5}>
        <StepScene
          number="3"
          emoji="⏳"
          title="队列控制"
          description="请求排队等待"
          details={[
            'Session Lane：同一会话的请求串行执行',
            'Global Lane：控制整体并发数',
            '目的：避免工具冲突、会话历史错乱',
          ]}
        />
      </Sequence>
      
      {/* 场景5: 步骤4 (5秒) */}
      <Sequence from={fps * 18} durationInFrames={fps * 5}>
        <StepScene
          number="4"
          emoji="📝"
          title="Prompt 组装"
          description="构建系统提示"
          details={[
            '基础提示：你是 OpenClaw AI 助手',
            'Skills 提示：当前激活的技能列表',
            '引导上下文：AGENTS.md / SOUL.md / MEMORY.md',
            '对话历史：之前的所有对话（自动压缩）',
          ]}
        />
      </Sequence>
      
      {/* 场景6: 步骤5 (5秒) */}
      <Sequence from={fps * 23} durationInFrames={fps * 5}>
        <StepScene
          number="5"
          emoji="🤖"
          title="模型推理"
          description="AI 开始思考"
          details={[
            '运行时：pi-agent-core（嵌入式 Agent 运行时）',
            '模型支持：OpenAI / Claude / Gemini / GLM / Kimi（20+ 模型）',
            'Fallback：首选模型失败，自动降级到备选模型',
          ]}
        />
      </Sequence>
      
      {/* 场景7: 步骤6 (5秒) */}
      <Sequence from={fps * 28} durationInFrames={fps * 5}>
        <StepScene
          number="6"
          emoji="🛠️"
          title="工具执行"
          description="AI 调用工具完成任务"
          details={[
            '触发条件：AI 决定需要查天气、读文件、发消息等',
            '执行流程：工具 start → update → end',
            '结果处理：大小限制、图片压缩、消息去重',
          ]}
        />
      </Sequence>
      
      {/* 场景8: 步骤7 (5秒) */}
      <Sequence from={fps * 33} durationInFrames={fps * 5}>
        <StepScene
          number="7"
          emoji="🌊"
          title="流式输出"
          description="一字一字返回结果"
          details={[
            'assistant：助手文字增量（一字一字显示）',
            'tool：工具执行进度（透明展示）',
            'lifecycle：生命周期（start/end/error）',
          ]}
        />
      </Sequence>
      
      {/* 场景9: 步骤8 (5秒) */}
      <Sequence from={fps * 38} durationInFrames={fps * 5}>
        <StepScene
          number="8"
          emoji="💾"
          title="持久化"
          description="保存对话历史"
          details={[
            '组装最终回复：文本 + 工具结果 + 媒体',
            '过滤静默令牌：NO_REPLY 不发送',
            '写入会话记录：持久化到存储',
            '释放会话锁：允许下一个请求执行',
          ]}
        />
      </Sequence>
      
      {/* 场景10: 总结 (5秒) */}
      <Sequence from={fps * 43} durationInFrames={fps * 5}>
        <SummaryScene />
      </Sequence>
    </>
  );
};
