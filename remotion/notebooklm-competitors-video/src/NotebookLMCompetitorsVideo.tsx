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
        flex: 1,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      <div style={{fontSize: 120, marginBottom: 30}}>📚</div>
      <h1
        style={{
          fontSize: 70,
          fontWeight: 'bold',
          color: '#fff',
          margin: 0,
          textAlign: 'center',
        }}
      >
        NotebookLM 竞争品大盘点
      </h1>
      <p
        style={{
          fontSize: 40,
          color: '#4CAF50',
          marginTop: 20,
          textAlign: 'center',
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
        flex: 1,
        backgroundColor: '#1a1a1a',
        padding: 80,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
      }}
    >
      <h2
        style={{
          fontSize: 60,
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
              marginBottom: 35,
              opacity,
              transform: `translateY(${translateY}px)`,
            }}
          >
            <div style={{fontSize: 50, marginRight: 30}}>{item.icon}</div>
            <div style={{fontSize: 36, color: '#fff'}}>{item.text}</div>
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
        flex: 1,
        backgroundColor: '#1a1a1a',
        padding: 80,
      }}
    >
      <h2
        style={{
          fontSize: 60,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 50,
          textAlign: 'center',
        }}
      >
        ✨ NotebookLM 是什么？
      </h2>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 40,
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
                padding: 40,
                borderRadius: 20,
                opacity,
              }}
            >
              <div style={{fontSize: 60, marginBottom: 20}}>{feature.icon}</div>
              <div style={{fontSize: 36, fontWeight: 'bold', color: '#fff', marginBottom: 10}}>
                {feature.title}
              </div>
              <div style={{fontSize: 24, color: '#ccc'}}>{feature.desc}</div>
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
        flex: 1,
        backgroundColor: '#1a1a1a',
        padding: 80,
      }}
    >
      <h2
        style={{
          fontSize: 60,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 50,
          textAlign: 'center',
        }}
      >
        🥊 6 大竞争品
      </h2>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr 1fr',
          gap: 30,
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
                padding: 30,
                borderRadius: 20,
                textAlign: 'center',
                opacity,
                transform: `scale(${scale})`,
              }}
            >
              <div style={{fontSize: 50, marginBottom: 15}}>{item.icon}</div>
              <div style={{fontSize: 28, fontWeight: 'bold', color: '#fff', marginBottom: 8}}>
                {item.name}
              </div>
              <div style={{fontSize: 20, color: '#4CAF50'}}>{item.highlight}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// 场景 5: 功能对比
const ComparisonScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const features = [
    {feature: '音频总结', notebooklm: '✅', perplexity: '❌', claude: '❌', obsidian: '❌'},
    {feature: '联网搜索', notebooklm: '❌', perplexity: '✅', claude: '❌', obsidian: '❌'},
    {feature: '长文档', notebooklm: '中', perplexity: '强', claude: '超强', obsidian: '中'},
    {feature: '本地化', notebooklm: '❌', perplexity: '❌', claude: '❌', obsidian: '✅'},
  ];

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#1a1a1a',
        padding: 60,
      }}
    >
      <h2
        style={{
          fontSize: 50,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 40,
          textAlign: 'center',
        }}
      >
        📊 核心功能对比
      </h2>
      <div style={{overflow: 'hidden'}}>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1.5fr 1fr 1fr 1fr 1fr',
            gap: 10,
            marginBottom: 20,
          }}
        >
          <div style={{fontSize: 24, color: '#fff', fontWeight: 'bold'}}>功能</div>
          <div style={{fontSize: 20, color: '#4CAF50', textAlign: 'center'}}>NotebookLM</div>
          <div style={{fontSize: 20, color: '#fff', textAlign: 'center'}}>Perplexity</div>
          <div style={{fontSize: 20, color: '#fff', textAlign: 'center'}}>Claude</div>
          <div style={{fontSize: 20, color: '#fff', textAlign: 'center'}}>Obsidian</div>
        </div>
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
                display: 'grid',
                gridTemplateColumns: '1.5fr 1fr 1fr 1fr 1fr',
                gap: 10,
                padding: '15px 0',
                borderTop: '1px solid #2a2a2a',
                opacity,
              }}
            >
              <div style={{fontSize: 24, color: '#ccc'}}>{row.feature}</div>
              <div style={{fontSize: 24, textAlign: 'center', color: '#4CAF50'}}>{row.notebooklm}</div>
              <div style={{fontSize: 24, textAlign: 'center', color: '#fff'}}>{row.perplexity}</div>
              <div style={{fontSize: 24, textAlign: 'center', color: '#fff'}}>{row.claude}</div>
              <div style={{fontSize: 24, textAlign: 'center', color: '#fff'}}>{row.obsidian}</div>
            </div>
          );
        })}
      </div>
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
        flex: 1,
        backgroundColor: '#1a1a1a',
        padding: 80,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
      }}
    >
      <h2
        style={{
          fontSize: 60,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 60,
          textAlign: 'center',
        }}
      >
        🎯 怎么选？
      </h2>
      {recommendations.map((item, index) => {
        const opacity = interpolate(
          frame,
          [index * 15, index * 15 + 15],
          [0, 1],
          {extrapolateRight: 'clamp'}
        );
        const translateX = interpolate(
          frame,
          [index * 15, index * 15 + 15],
          [-50, 0],
          {extrapolateRight: 'clamp'}
        );

        return (
          <div
            key={index}
            style={{
              display: 'flex',
              alignItems: 'center',
              marginBottom: 40,
              padding: 30,
              backgroundColor: '#2a2a2a',
              borderRadius: 20,
              opacity,
              transform: `translateX(${translateX}px)`,
            }}
          >
            <div style={{fontSize: 50, marginRight: 30, width: 60}}>{item.icon}</div>
            <div style={{flex: 1}}>
              <div style={{fontSize: 28, color: '#ccc', marginBottom: 8}}>需要 {item.need}</div>
              <div style={{fontSize: 36, fontWeight: 'bold', color: '#fff'}}>
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
        flex: 1,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      <div style={{fontSize: 80, marginBottom: 40}}>💡</div>
      <h2
        style={{
          fontSize: 70,
          fontWeight: 'bold',
          color: '#fff',
          marginBottom: 30,
          textAlign: 'center',
        }}
      >
        组合才是王道
      </h2>
      <p
        style={{
          fontSize: 36,
          color: '#ccc',
          marginBottom: 30,
          textAlign: 'center',
        }}
      >
        没有最好的工具，只有最适合你的工具
      </p>
      <div
        style={{
          marginTop: 30,
          padding: '20px 40px',
          backgroundColor: '#4CAF50',
          borderRadius: 50,
          fontSize: 32,
          fontWeight: 'bold',
          color: '#fff',
        }}
      >
        选择适合你的知识管理工具 →
      </div>
    </div>
  );
};

// 主视频组件
const NotebookLMCompetitorsVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <div
      style={{
        flex: 1,
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

export default NotebookLMCompetitorsVideo;
