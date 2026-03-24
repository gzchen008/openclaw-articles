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
      <div style={{fontSize: 100, marginBottom: 20}}>🤖</div>
      <h1
        style={{
          fontSize: 56,
          fontWeight: 'bold',
          color: '#fff',
          margin: 0,
          textAlign: 'center',
          lineHeight: 1.2,
        }}
      >
        运维自动化实战
      </h1>
      <p
        style={{
          fontSize: 28,
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
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#ff6b6b',
          marginBottom: 40,
          textAlign: 'center',
          width: '100%',
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
              marginBottom: 35,
              opacity,
              transform: `translateY(${translateY}px)`,
              width: '100%',
              justifyContent: 'center',
            }}
          >
            <div style={{fontSize: 40, marginRight: 20}}>{item.icon}</div>
            <div style={{fontSize: 26, color: '#fff'}}>{item.text}</div>
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
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 40,
          textAlign: 'center',
          width: '100%',
        }}
      >
        ✨ 4 大核心能力
      </h2>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 20,
          width: '100%',
          maxWidth: 900,
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
                padding: 25,
                borderRadius: 16,
                opacity,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
              }}
            >
              <div style={{fontSize: 44, marginBottom: 12}}>{feature.icon}</div>
              <div style={{fontSize: 26, fontWeight: 'bold', color: '#fff', marginBottom: 8}}>
                {feature.title}
              </div>
              <div style={{fontSize: 18, color: '#ccc'}}>{feature.desc}</div>
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
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 40,
          textAlign: 'center',
          width: '100%',
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
              marginBottom: 35,
              opacity,
              transform: `scale(${scale})`,
              width: '100%',
              maxWidth: 800,
              justifyContent: 'center',
            }}
          >
            <div
              style={{
                fontSize: 56,
                marginRight: 25,
                width: 80,
                textAlign: 'center',
              }}
            >
              {item.icon}
            </div>
            <div style={{flex: 1}}>
              <div style={{fontSize: 28, fontWeight: 'bold', color: '#fff', marginBottom: 8}}>
                {item.title}
              </div>
              <div style={{fontSize: 20, color: '#ccc'}}>{item.result}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// 场景 5: 效率对比
const EfficiencyScene: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const stats = [
    {label: '健康检查', before: '10分钟', after: '自动', save: '10分钟'},
    {label: '日志分析', before: '30分钟', after: '2分钟', save: '28分钟'},
    {label: '故障排查', before: '1小时', after: '5分钟', save: '55分钟'},
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
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 40,
          textAlign: 'center',
          width: '100%',
        }}
      >
        📈 效率提升
      </h2>
      <div style={{width: '100%', maxWidth: 800}}>
        {stats.map((stat, index) => {
          const progress = interpolate(
            frame,
            [index * 20, index * 20 + 30],
            [0, 1],
            {extrapolateRight: 'clamp'}
          );

          return (
            <div key={index} style={{marginBottom: 30, width: '100%'}}>
              <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 10}}>
                <span style={{fontSize: 22, color: '#fff', fontWeight: 'bold'}}>{stat.label}</span>
                <span style={{fontSize: 22, color: '#4CAF50'}}>节省 {stat.save}</span>
              </div>
              <div
                style={{
                  width: '100%',
                  height: 16,
                  backgroundColor: '#2a2a2a',
                  borderRadius: 8,
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    width: `${progress * 100}%`,
                    height: '100%',
                    backgroundColor: '#4CAF50',
                    borderRadius: 8,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
      <div
        style={{
          marginTop: 30,
          padding: 25,
          backgroundColor: '#2a2a2a',
          borderRadius: 16,
          textAlign: 'center',
          width: '100%',
          maxWidth: 800,
        }}
      >
        <div style={{fontSize: 36, fontWeight: 'bold', color: '#4CAF50'}}>
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
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: '#1a1a1a',
        padding: 60,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <h2
        style={{
          fontSize: 44,
          fontWeight: 'bold',
          color: '#4CAF50',
          marginBottom: 40,
          textAlign: 'center',
          width: '100%',
        }}
      >
        🚀 4 步快速上手
      </h2>
      <div style={{display: 'flex', flexDirection: 'column', gap: 20, width: '100%', maxWidth: 800}}>
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
                backgroundColor: '#2a2a2a',
                padding: 25,
                borderRadius: 16,
                textAlign: 'center',
                opacity,
                transform: `translateY(${translateY}px)`,
                width: '100%',
              }}
            >
              <div
                style={{
                  fontSize: 48,
                  fontWeight: 'bold',
                  color: '#4CAF50',
                  marginBottom: 10,
                }}
              >
                {item.step}
              </div>
              <div style={{fontSize: 20, color: '#fff'}}>{item.text}</div>
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
      <div style={{fontSize: 70, marginBottom: 30}}>💪</div>
      <h2
        style={{
          fontSize: 48,
          fontWeight: 'bold',
          color: '#fff',
          marginBottom: 20,
          textAlign: 'center',
          lineHeight: 1.3,
        }}
      >
        把重复性工作交给 AI
      </h2>
      <p
        style={{
          fontSize: 28,
          color: '#ccc',
          marginBottom: 40,
          textAlign: 'center',
        }}
      >
        你专注于更有价值的事情
      </p>
      <div
        style={{
          padding: '20px 40px',
          backgroundColor: '#4CAF50',
          borderRadius: 40,
          fontSize: 28,
          fontWeight: 'bold',
          color: '#fff',
        }}
      >
        现在开始使用 OpenClaw →
      </div>
    </div>
  );
};

// 主视频组件（竖屏版）
const OpsAutomationVideoVertical: React.FC = () => {
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

export default OpsAutomationVideoVertical;
