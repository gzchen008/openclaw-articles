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
      <div style={{fontSize: 120, marginBottom: 30}}>🤖</div>
      <h1
        style={{
          fontSize: 80,
          fontWeight: 'bold',
          color: '#fff',
          margin: 0,
          textAlign: 'center',
        }}
      >
        运维自动化实战
      </h1>
      <p
        style={{
          fontSize: 40,
          color: '#4CAF50',
          marginTop: 20,
          textAlign: 'center',
        }}
      >
        OpenClaw - 你的 24 小时运维助手
      </p>
    </div>
  );
};

// 场景 2: 痛点场景
const PainPointScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const items = [
    {icon: '🌙', text: '凌晨 3 点服务器告警', delay: 0},
    {icon: '💾', text: '手动备份 10 个数据库', delay: 10},
    {icon: '📊', text: '老板问宕机次数答不上', delay: 20},
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
        😫 运维人的崩溃时刻
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
              marginBottom: 40,
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

// 场景 3: 功能介绍
const FeatureScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const features = [
    {icon: '📊', title: '服务器监控', desc: 'CPU/内存/磁盘实时监控'},
    {icon: '📝', title: '日志分析', desc: 'AI 智能分析异常模式'},
    {icon: '💾', title: '自动备份', desc: '定时备份失败立即通知'},
    {icon: '🐳', title: 'Docker 管理', desc: '自然语言操作容器'},
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
        ✨ 4 大核心能力
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

// 场景 4: 实战案例
const CaseStudyScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const cases = [
    {icon: '🏥', title: '健康检查', result: '每天早上 9 点自动报告'},
    {icon: '🔍', title: '异常检测', result: '自动识别 DDoS 攻击'},
    {icon: '💾', title: '自动备份', result: '凌晨 3 点自动执行'},
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
        🎯 实战案例
      </h2>
      {cases.map((item, index) => {
        const opacity = interpolate(
          frame,
          [index * 20, index * 20 + 15],
          [0, 1],
          {extrapolateRight: 'clamp'}
        );
        const scale = spring({
          frame: frame - index * 20,
          fps,
          config: {damping: 100},
          from: 0.8,
          to: 1,
        });

        return (
          <div
            key={index}
            style={{
              display: 'flex',
              alignItems: 'center',
              marginBottom: 50,
              opacity,
              transform: `scale(${scale})`,
            }}
          >
            <div
              style={{
                fontSize: 70,
                marginRight: 40,
                width: 100,
                textAlign: 'center',
              }}
            >
              {item.icon}
            </div>
            <div style={{flex: 1}}>
              <div style={{fontSize: 36, fontWeight: 'bold', color: '#fff', marginBottom: 10}}>
                {item.title}
              </div>
              <div style={{fontSize: 28, color: '#ccc'}}>{item.result}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// 场景 5: 效率对比
const EfficiencyScene: React.FC = () => {
  const frame = useVideoConfig();
  const {fps} = useVideoConfig();

  const stats = [
    {label: '健康检查', before: '10分钟', after: '自动', save: '10分钟'},
    {label: '日志分析', before: '30分钟', after: '2分钟', save: '28分钟'},
    {label: '故障排查', before: '1小时', after: '5分钟', save: '55分钟'},
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
        📈 效率提升
      </h2>
      {stats.map((stat, index) => {
        const progress = interpolate(
          useCurrentFrame(),
          [index * 20, index * 20 + 30],
          [0, 1],
          {extrapolateRight: 'clamp'}
        );

        return (
          <div key={index} style={{marginBottom: 50}}>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 15}}>
              <span style={{fontSize: 32, color: '#fff', fontWeight: 'bold'}}>{stat.label}</span>
              <span style={{fontSize: 32, color: '#4CAF50'}}>节省 {stat.save}</span>
            </div>
            <div
              style={{
                width: '100%',
                height: 20,
                backgroundColor: '#2a2a2a',
                borderRadius: 10,
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  width: `${progress * 100}%`,
                  height: '100%',
                  backgroundColor: '#4CAF50',
                  borderRadius: 10,
                }}
              />
            </div>
          </div>
        );
      })}
      <div
        style={{
          marginTop: 40,
          padding: 30,
          backgroundColor: '#2a2a2a',
          borderRadius: 20,
          textAlign: 'center',
        }}
      >
        <div style={{fontSize: 48, fontWeight: 'bold', color: '#4CAF50'}}>
          💰 一个月省下 20 小时
        </div>
      </div>
    </div>
  );
};

// 场景 6: 快速上手
const QuickStartScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const steps = [
    {step: '1', text: '安装 OpenClaw'},
    {step: '2', text: '配置通知渠道'},
    {step: '3', text: '创建定时任务'},
    {step: '4', text: '查看运行状态'},
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
        🚀 4 步快速上手
      </h2>
      <div style={{display: 'flex', justifyContent: 'space-between', gap: 30}}>
        {steps.map((item, index) => {
          const opacity = interpolate(
            frame,
            [index * 15, index * 15 + 15],
            [0, 1],
            {extrapolateRight: 'clamp'}
          );
          const translateY = interpolate(
            frame,
            [index * 15, index * 15 + 15],
            [30, 0],
            {extrapolateRight: 'clamp'}
          );

          return (
            <div
              key={index}
              style={{
                flex: 1,
                backgroundColor: '#2a2a2a',
                padding: 40,
                borderRadius: 20,
                textAlign: 'center',
                opacity,
                transform: `translateY(${translateY}px)`,
              }}
            >
              <div
                style={{
                  fontSize: 60,
                  fontWeight: 'bold',
                  color: '#4CAF50',
                  marginBottom: 20,
                }}
              >
                {item.step}
              </div>
              <div style={{fontSize: 24, color: '#fff'}}>{item.text}</div>
            </div>
          );
        })}
      </div>
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
      <div style={{fontSize: 80, marginBottom: 40}}>💪</div>
      <h2
        style={{
          fontSize: 70,
          fontWeight: 'bold',
          color: '#fff',
          marginBottom: 30,
          textAlign: 'center',
        }}
      >
        把重复性工作交给 AI
      </h2>
      <p
        style={{
          fontSize: 40,
          color: '#ccc',
          marginBottom: 50,
          textAlign: 'center',
        }}
      >
        你专注于更有价值的事情
      </p>
      <div
        style={{
          padding: '25px 50px',
          backgroundColor: '#4CAF50',
          borderRadius: 50,
          fontSize: 36,
          fontWeight: 'bold',
          color: '#fff',
        }}
      >
        现在开始使用 OpenClaw →
      </div>
    </div>
  );
};

// 主视频组件
const OpsAutomationVideo: React.FC = () => {
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
      
      {/* 场景 3: 功能介绍 (6秒) */}
      {frame >= 240 && frame < 420 && <FeatureScene />}
      
      {/* 场景 4: 实战案例 (6秒) */}
      {frame >= 420 && frame < 600 && <CaseStudyScene />}
      
      {/* 场景 5: 效率对比 (5秒) */}
      {frame >= 600 && frame < 750 && <EfficiencyScene />}
      
      {/* 场景 6: 快速上手 (5秒) */}
      {frame >= 750 && frame < 900 && <QuickStartScene />}
      
      {/* 场景 7: 行动号召 (4秒) */}
      {frame >= 900 && <CallToActionScene />}
    </div>
  );
};

export default OpsAutomationVideo;
