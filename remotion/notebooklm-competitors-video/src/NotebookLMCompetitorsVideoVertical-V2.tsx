import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

// 场景 1: 品牌封面
const CoverScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const opacity = interpolate(frame, [0, 30], [0, 1]);
  const scale = spring({frame, fps, config: {damping: 100}, from: 0.8, to: 1});

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        opacity,
        transform: `scale(${scale})`,
        padding: 40,
      }}
    >
      <div style={{fontSize: 100, marginBottom: 30}}>📚</div>
      <h1
        style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: '#fff',
          margin: 0,
          textAlign: 'center',
          paddingHorizontal: 40,
        }}
      >
        NotebookLM 竞争品大盘点
      </h1>
      <p
        style={{
          fontSize: 32,
          color: '#4CAF50',
          marginTop: 20,
          textAlign: 'center',
          paddingHorizontal: 40,
        }}
      >
        哪个更适合你的知识管理？
      </p>
    </div>
  );
};

// 场景 2: 痛点场景
const PainPointScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const items = [
    {icon: '📄', text: 'PDF 堆积成山，找不到重点', delay: 0},
    {icon: '🔍', text: '搜索不到想要的信息', delay: 10},
    {icon: '🎧', text: '想听音频总结，但工具不支持', delay: 20},
    {icon: '💰', text: '多个工具来回切换，成本高', delay: 30},
  ];

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 60,
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#ff6b6b',
          marginBottom: 50,
          textAlign: 'center',
        }}
      >
        😫 知识管理的困惑
      </h2>
      {items.map((item, index) => {
        const opacity = interpolate(
          frame,
          [item.delay, item.delay + 15],
          [0, 1],
          {extrapolateRight: 'clamp'}
        );
        const translateY = interpolate(
          frame,
          [item.delay, item.delay + 15],
          [30, 0],
          {extrapolateRight: 'clamp'}
        );

        return (
          <div
            key={index}
            style={{
              display: 'flex',
              alignItems: 'center',
              marginBottom: 30,
                opacity,
              transform: `translateY(${translateY}px)`,
            }}
          >
            <div style={{fontSize: 40, marginRight: 20}}>{item.icon}</div>
            <div style={{fontSize: 28, color: '#fff', textAlign: 'center'}}>{item.text}</div>
          </div>
        );
      })}
    </div>
  );
};

// 场景 3: NotebookLM 介绍
const NotebookLMScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const features = [
    {icon: '📤', title: '上传知识源', desc: 'PDF、Docs、网页'},
    {icon: '🤖', title: 'AI 问答', desc: '基于内容回答问题'},
    {icon: '🎧', title: 'Audio Overview', desc: '播客式音频总结'},
    {icon: '🆓', title: '完全免费', desc: 'Google 出品'},
  ];

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 60,
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 40,
          textAlign: 'center',
        }}
      >
        ✨ NotebookLM 是什么？
      </h2>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 25,
          width: '100%',
          maxWidth: 600,
        }}
      >
        {features.map((feature, index) => {
          const opacity = interpolate(
            frame,
            [index * 15, index * 15 + 15],
            [0, 1],
            {extrapolateRight: 'clamp'}
          );

          return (
            <div
              key={index}
              style={{
                backgroundColor: '#2a2a2a',
                padding: 30,
                borderRadius: 20,
                opacity,
                textAlign: 'center',
              }}
            >
              <div style={{fontSize: 50, marginBottom: 15}}>{feature.icon}</div>
              <div style={{fontSize: 28, fontWeight: 'bold', color: '#fff', marginBottom: 8}}>
                {feature.title}
              </div>
              <div style={{fontSize: 20, color: '#ccc'}}>{feature.desc}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// 场景 4: 6 大竞争品
const CompetitorsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const competitors = [
    {icon: '🔍', name: 'Perplexity AI', highlight: '搜索能力最强'},
    {icon: '📝', name: 'Claude Projects', highlight: '200K 上下文'},
    {icon: '🎨', name: 'ChatGPT Canvas', highlight: '生态最完整'},
    {icon: '📋', name: 'Notion AI', highlight: '笔记原生集成'},
    {icon: '🧠', name: 'Mem.ai', highlight: '自动组织'},
    {icon: '🔒', name: 'Obsidian', highlight: '本地优先'},
  ];

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 60,
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 40,
          textAlign: 'center',
        }}
      >
        🥊 6 大竞争品
      </h2>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 20,
          width: '100%',
          maxWidth: 600,
        }}
      >
        {competitors.map((item, index) => {
          const opacity = interpolate(
            frame,
            [index * 10, index * 10 + 15],
            [0, 1],
            {extrapolateRight: 'clamp'}
          );
          const scale = spring({
            frame: frame - index * 10,
            fps,
            config: {damping: 100},
            from: 0.8,
            to: 1,
          });

          return (
            <div
              key={index}
              style={{
                backgroundColor: '#2a2a2a',
                padding: 25,
                borderRadius: 20,
                textAlign: 'center',
                opacity,
                transform: `scale(${scale})`,
              }}
            >
              <div style={{fontSize: 40, marginBottom: 10}}>{item.icon}</div>
              <div style={{fontSize: 22, fontWeight: 'bold', color: '#fff', marginBottom: 6}}>
                {item.name}
              </div>
              <div style={{fontSize: 16, color: '#4CAF50'}}>{item.highlight}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// 场景 5: 功能对比（简化版）
const ComparisonScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const features = [
    {feature: '音频总结', notebooklm: '✅', others: '❌'},
    {feature: '联网搜索', notebooklm: '❌', others: '✅ Perplexity'},
    {feature: '长文档', notebooklm: '中', others: '超强 Claude'},
    {feature: '本地化', notebooklm: '❌', others: '✅ Obsidian'},
  ];

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 50,
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 40,
          textAlign: 'center',
        }}
      >
        📊 核心功能对比
      </h2>
      {features.map((row, index) => {
        const opacity = interpolate(
          frame,
          [index * 15, index * 15 + 15],
          [0, 1],
          {extrapolateRight: 'clamp'}
        );

        return (
          <div
            key={index}
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              width: '100%',
              maxWidth: 600,
              padding: '20px 30px',
              marginBottom: 15,
              backgroundColor: '#2a2a2a',
              borderRadius: 15,
              opacity,
            }}
          >
            <div style={{fontSize: 22, color: '#ccc'}}>{row.feature}</div>
            <div style={{fontSize: 20, textAlign: 'right'}}>
              <span style={{color: '#4CAF50', marginRight: 15}}>{row.notebooklm}</span>
              <span style={{color: '#fff'}}>{row.others}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// 场景 6: 选择建议
const RecommendationScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const recommendations = [
    {need: '音频总结', tool: 'NotebookLM', icon: '🎧'},
    {need: '搜索 + 知识', tool: 'Perplexity AI', icon: '🔍'},
    {need: '超长文档', tool: 'Claude Projects', icon: '📝'},
    {need: '隐私保护', tool: 'Obsidian', icon: '🔒'},
  ];

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 60,
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 50,
          textAlign: 'center',
        }}
      >
        🎯 怎么选?
      </h2>
      {recommendations.map((item, index) => {
        const opacity = interpolate(
          frame,
          [index * 15, index * 15 + 15],
          [0, 1],
          {extrapolateRight: 'clamp'}
        );
        const scale = spring({
          frame: frame - index * 15,
          fps,
          config: {damping: 100},
          from: 0.9,
          to: 1,
        });

        return (
          <div
            key={index}
            style={{
              display: 'flex',
              alignItems: 'center',
              marginBottom: 25,
              padding: 25,
              backgroundColor: '#2a2a2a',
              borderRadius: 20,
              width: '100%',
              maxWidth: 600,
              opacity,
              transform: `scale(${scale})`,
            }}
          >
            <div style={{fontSize: 40, marginRight: 20, width: 50}}>{item.icon}</div>
            <div style={{flex: 1, textAlign: 'center'}}>
              <div style={{fontSize: 22, color: '#ccc', marginBottom: 6}}>需要 {item.need}</div>
              <div style={{fontSize: 28, fontWeight: 'bold', color: '#fff'}}>
                → {item.tool}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// 场景 7: 行动号召
const CallToActionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const opacity = interpolate(frame, [0, 20], [0, 1]);
  const scale = spring({frame, fps, config: {damping: 100}, from: 0.9, to: 1});

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        opacity,
        transform: `scale(${scale})`,
        padding: 40,
      }}
    >
      <div style={{fontSize: 70, marginBottom: 30}}>💡</div>
      <h2
        style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: '#fff',
          marginBottom: 25,
          textAlign: 'center',
          paddingHorizontal: 40,
        }}
      >
        组合才是王道
      </h2>
      <p
        style={{
          fontSize: 28,
          color: '#ccc',
          marginBottom: 40,
          textAlign: 'center',
          paddingHorizontal: 40,
        }}
      >
        没有最好的工具，只有最适合你的工具
      </p>
      <div
        style={{
          marginTop: 20,
          padding: '20px 40px',
          backgroundColor: '#4CAF50',
          borderRadius: 50,
          fontSize: 26,
          fontWeight: 'bold',
          color: '#fff',
          textAlign: 'center',
        }}
      >
        选择适合你的知识管理工具 →
      </div>
    </div>
  );
};

// 主视频组件
const NotebookLMCompetitorsVideoVerticalV2: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
      }}
    >
      {/* 场景 1: 封面 (3秒) */}
      {frame < 90 && <CoverScene />}
      
      {/* 场景 2: 痛点 (5秒) */}
      {frame >= 90 && frame < 240 && <PainPointScene />}
      
      {/* 场景 3: NotebookLM 介绍 (5秒) */}
      {frame >= 240 && frame < 390 && <NotebookLMScene />}
      
      {/* 场景 4: 6 大竞争品 (6秒) */}
      {frame >= 390 && frame < 570 && <CompetitorsScene />}
      
      {/* 场景 5: 功能对比 (5秒) */}
      {frame >= 570 && frame < 720 && <ComparisonScene />}
      
      {/* 场景 6: 选择建议 (5秒) */}
      {frame >= 720 && frame < 870 && <RecommendationScene />}
      
      {/* 场景 7: 行动号召 (4秒) */}
      {frame >= 870 && <CallToActionScene />}
    </div>
  );
};

export default NotebookLMCompetitorsVideoVerticalV2;
