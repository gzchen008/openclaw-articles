import {useCurrentFrame, interpolate} from 'remotion';

export const PainPoint: React.FC = () => {
  const frame = useCurrentFrame();

  const slideIn = interpolate(frame, [0, 30], [-100, 0]);
  const fadeIn = interpolate(frame, [0, 20], [0, 1]);

  const painPoints = [
    '😫 每天重复操作让人崩溃',
    '📧 邮件、消息处理占用大量时间',
    '⏰ 定时任务总是忘记设置',
    '🤖 想自动化却不懂编程',
  ];

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        background: '#1a1a2e',
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
          color: '#ff6b6b',
          fontSize: 48,
          marginBottom: 40,
          opacity: fadeIn,
        }}
      >
        这些场景熟悉吗？
      </h2>
      <div style={{display: 'flex', flexDirection: 'column', gap: 24}}>
        {painPoints.map((point, index) => {
          const delay = index * 10;
          const itemOpacity = interpolate(frame, [delay, delay + 15], [0, 1]);
          const itemSlide = interpolate(frame, [delay, delay + 20], [50, 0]);

          return (
            <div
              key={index}
              style={{
                color: 'white',
                fontSize: 32,
                opacity: itemOpacity,
                transform: `translateX(${itemSlide}px)`,
                background: 'rgba(255,107,107,0.1)',
                padding: '16px 32px',
                borderRadius: 12,
                borderLeft: '4px solid #ff6b6b',
              }}
            >
              {point}
            </div>
          );
        })}
      </div>
    </div>
  );
};
