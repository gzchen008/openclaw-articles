import React from 'react';
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig, Img, staticFile } from 'remotion';

// 封面场景
const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [60, 90], [1, 0], { extrapolateRight: 'clamp' });
  const subtitleOpacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', backgroundColor: '#0a0a0a' }}>
      <div style={{ opacity: opacity * fadeOut, textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ fontSize: 72, fontWeight: 'bold', color: '#4CAF50', marginBottom: 40, textAlign: 'center', lineHeight: 1.3 }}>
          OpenClaw<br/>Context Engine
        </div>
        <div style={{ fontSize: 36, color: '#fff', opacity: subtitleOpacity, textAlign: 'center', lineHeight: 1.6 }}>
          让你的 AI 拥有无损记忆
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 痛点场景
const PainPointScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const text1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const text2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const text3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 48, fontWeight: 'bold', color: '#ff6b6b', opacity: titleOpacity, marginBottom: 60, textAlign: 'center' }}>
          😰 你遇到过这种情况吗？
        </div>
        <div style={{ fontSize: 28, color: '#fff', opacity: text1Opacity, marginBottom: 32, textAlign: 'center', lineHeight: 1.6 }}>
          和 AI 聊了 100 轮，做了很多决策
        </div>
        <div style={{ fontSize: 28, color: '#fff', opacity: text2Opacity, marginBottom: 32, textAlign: 'center', lineHeight: 1.6 }}>
          突然想回到第 5 轮讨论的话题...
        </div>
        <div style={{ fontSize: 32, color: '#ff6b6b', opacity: text3Opacity, textAlign: 'center', fontWeight: 'bold', lineHeight: 1.6 }}>
          AI：「抱歉，我不记得了」
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 概念场景
const ConceptScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const box1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const box2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const box3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 60, textAlign: 'center' }}>
          📦 Context Engine 是什么？
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', opacity: box1Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 12 }}>独占插件插槽</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>同一时间只能激活一个引擎</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', opacity: box2Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 12 }}>上下文管理</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>组装发送给模型的所有内容</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, width: '100%', opacity: box3Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 12 }}>压缩与摄入</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>当接近 token 限制时压缩旧对话</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 方案对比场景
const SolutionsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const box1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const box2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const box3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          🚀 无损记忆三种方案
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', borderLeft: '4px solid #4CAF50', opacity: box1Opacity }}>
          <div style={{ fontSize: 26, color: '#4CAF50', marginBottom: 8 }}>1️⃣ 分层上下文</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>活跃层 + 索引层 + 存储层</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', borderLeft: '4px solid #2196F3', opacity: box2Opacity }}>
          <div style={{ fontSize: 26, color: '#2196F3', marginBottom: 8 }}>2️⃣ 图结构上下文</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>保留因果关系，追溯决策链</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, width: '100%', borderLeft: '4px solid #9C27B0', opacity: box3Opacity }}>
          <div style={{ fontSize: 26, color: '#9C27B0', marginBottom: 8 }}>3️⃣ 向量化上下文</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>语义搜索，跨会话检索</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 性能对比场景
const ComparisonScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const row1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const row2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const row3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          📊 Legacy vs 无损记忆
        </div>
        <div style={{ display: 'flex', width: '100%', marginBottom: 24, opacity: row1Opacity }}>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, marginRight: 12 }}>
            <div style={{ fontSize: 20, color: '#ff6b6b', marginBottom: 8 }}>❌ Legacy</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>压缩后丢失细节</div>
          </div>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, borderLeft: '3px solid #4CAF50' }}>
            <div style={{ fontSize: 20, color: '#4CAF50', marginBottom: 8 }}>✅ 无损记忆</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>完整保留所有信息</div>
          </div>
        </div>
        <div style={{ display: 'flex', width: '100%', marginBottom: 24, opacity: row2Opacity }}>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, marginRight: 12 }}>
            <div style={{ fontSize: 20, color: '#ff6b6b', marginBottom: 8 }}>❌ Legacy</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>无检索能力</div>
          </div>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, borderLeft: '3px solid #4CAF50' }}>
            <div style={{ fontSize: 20, color: '#4CAF50', marginBottom: 8 }}>✅ 无损记忆</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>向量搜索，语义检索</div>
          </div>
        </div>
        <div style={{ display: 'flex', width: '100%', opacity: row3Opacity }}>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, marginRight: 12 }}>
            <div style={{ fontSize: 20, color: '#ff6b6b', marginBottom: 8 }}>❌ Legacy</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>简单任务场景</div>
          </div>
          <div style={{ flex: 1, backgroundColor: '#2a2a2a', padding: 20, borderRadius: 12, borderLeft: '3px solid #4CAF50' }}>
            <div style={{ fontSize: 20, color: '#4CAF50', marginBottom: 8 }}>✅ 无损记忆</div>
            <div style={{ fontSize: 18, color: '#ccc' }}>长期项目 + 复杂任务</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 代码示例场景
const CodeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const code1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const code2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          🛠️ 核心接口
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 28, borderRadius: 16, width: '100%', opacity: code1Opacity, marginBottom: 24 }}>
          <div style={{ fontFamily: 'monospace', fontSize: 18, color: '#9CDCFE', lineHeight: 1.8 }}>
            <div><span style={{ color: '#569CD6' }}>interface</span> ContextEngine {'{'}</div>
            <div style={{ paddingLeft: 20 }}>assembleContext()</div>
            <div style={{ paddingLeft: 20 }}>compact()</div>
            <div style={{ paddingLeft: 20 }}>ingest()</div>
            <div>{'}'}</div>
          </div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 28, borderRadius: 16, width: '100%', opacity: code2Opacity }}>
          <div style={{ fontFamily: 'monospace', fontSize: 18, color: '#9CDCFE', lineHeight: 1.8 }}>
            <div><span style={{ color: '#569CD6' }}>async</span> assembleContext(session, params) {'{'}</div>
            <div style={{ paddingLeft: 20 }}><span style={{ color: '#6A9955' }}>// 1. 活跃层</span></div>
            <div style={{ paddingLeft: 20 }}><span style={{ color: '#6A9955' }}>// 2. 向量检索</span></div>
            <div style={{ paddingLeft: 20 }}><span style={{ color: '#6A9955' }}>// 3. 合并返回</span></div>
            <div>{'}'}</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 行动号召场景
const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const step1Opacity = interpolate(frame, [20, 40], [0, 1], { extrapolateRight: 'clamp' });
  const step2Opacity = interpolate(frame, [40, 60], [0, 1], { extrapolateRight: 'clamp' });
  const step3Opacity = interpolate(frame, [60, 80], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center', padding: 48 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '90%', maxWidth: 960 }}>
        <div style={{ fontSize: 44, fontWeight: 'bold', color: '#4CAF50', opacity: titleOpacity, marginBottom: 50, textAlign: 'center' }}>
          🎯 如何使用？
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', opacity: step1Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 8 }}>1️⃣ 适用场景</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>长期项目、复杂任务、多文件协作</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, marginBottom: 24, width: '100%', opacity: step2Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 8 }}>2️⃣ 配置方式</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>plugins.slots.contextEngine = "lossless"</div>
        </div>
        <div style={{ backgroundColor: '#1a1a1a', padding: 24, borderRadius: 16, width: '100%', opacity: step3Opacity }}>
          <div style={{ fontSize: 24, color: '#4CAF50', marginBottom: 8 }}>3️⃣ 推荐技术栈</div>
          <div style={{ fontSize: 20, color: '#ccc' }}>LanceDB + OpenAI Embeddings</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 主视频组件
export const ContextEngineVideo: React.FC = () => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {/* 封面场景：0-90帧（3秒） */}
      <Sequence from={0} durationInFrames={90}>
        <CoverScene />
      </Sequence>

      {/* 痛点场景：90-240帧（5秒） */}
      <Sequence from={90} durationInFrames={150}>
        <PainPointScene />
      </Sequence>

      {/* 概念场景：240-390帧（5秒） */}
      <Sequence from={240} durationInFrames={150}>
        <ConceptScene />
      </Sequence>

      {/* 方案对比场景：390-540帧（5秒） */}
      <Sequence from={390} durationInFrames={150}>
        <SolutionsScene />
      </Sequence>

      {/* 性能对比场景：540-690帧（5秒） */}
      <Sequence from={540} durationInFrames={150}>
        <ComparisonScene />
      </Sequence>

      {/* 代码示例场景：690-840帧（5秒） */}
      <Sequence from={690} durationInFrames={150}>
        <CodeScene />
      </Sequence>

      {/* 行动号召场景：840-990帧（5秒） */}
      <Sequence from={840} durationInFrames={150}>
        <CTAScene />
      </Sequence>
    </AbsoluteFill>
  );
};
