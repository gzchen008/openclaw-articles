import {useCurrentFrame, interpolate} from 'remotion';

export const Solution: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 30], [0, 1]);
  const lineWidth = interpolate(frame, [30, 90], [0, 100]);

  const features = [
    {emoji: '💬', title: '一句话搞定', desc: '自然语言描述任务'},
    {emoji: '⚡', title: '即时执行', desc: '无需等待，立即完成'},
    {emoji: '🔌', title: '多平台集成', desc: 'Discord、邮件、日历...'},
    {emoji: '🤖', title: 'AI驱动', desc: '智能理解，自动规划'},
  ];

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        background: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        padding: 60,
      }}
    >
      <h2
        style={{
          color: 'white',
          fontSize: 56,
          marginBottom: 16,
          opacity: titleOpacity,
          textAlign: 'center',
        }}
      >
        OpenClaw 来了
      </h2>      <div
        style={{
          width: `${lineWidth}%`,
          maxWidth: 400,
          height: 4,
          background: 'white',
          marginBottom: 60,
          borderRadius: 2,
        }}
      />

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: 30,
          maxWidth: 900,
        }}
      >
        {features.map((feature, index) => {
          const delay = 60 + index * 20;
          const cardOpacity = interpolate(frame, [delay, delay + 20], [0, 1]);
          const cardScale = interpolate(frame, [delay, delay + 25], [0.8, 1]);

          return (
            <div
              key={index}
              style={{
                background: 'rgba(255,255,255,0.95)',
                borderRadius: 16,
                padding: 32,
                textAlign: 'center',
                opacity: cardOpacity,
                transform: `scale(${cardScale})`,
              }}
            >
              <div style={{fontSize: 48, marginBottom: 12}}>{feature.emoji}</div>
              <h3 style={{color: '#11998e', fontSize: 24, marginBottom: 8}}>
                {feature.title}
              </h3>
              <p style={{color: '#666', fontSize: 16, margin: 0}}>{feature.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
