import {useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';

export const CTA: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: {damping: 12, stiffness: 80},
  });

  const opacity = interpolate(frame, [0, 30], [0, 1]);
  const buttonScale = spring({
    frame: frame - 60,
    fps,
    config: {damping: 10, stiffness: 100},
  });

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      <div style={{opacity, transform: `scale(${scale})`, textAlign: 'center'}}>
        <h2
          style={{
            color: 'white',
            fontSize: 56,
            marginBottom: 16,
          }}
        >
          准备好解放双手了吗？
        </h2>        <p
          style={{
            color: 'rgba(255,255,255,0.8)',
            fontSize: 24,
            marginBottom: 40,
          }}
        >
          开源免费 · 即刻开始 · 社区支持
        </p>

        {/* CTA 按钮 */}
        <div
          style={{
            transform: `scale(${buttonScale})`,
            background: 'white',
            color: '#667eea',
            padding: '20px 48px',
            borderRadius: 50,
            fontSize: 24,
            fontWeight: 700,
            boxShadow: '0 10px 40px rgba(0,0,0,0.3)',
          }}
        >
          🚀 访问 github.com/openclaw
        </div>
      </div>

      {/* 底部信息 */}
      <div
        style={{
          position: 'absolute',
          bottom: 40,
          opacity: interpolate(frame, [120, 150], [0, 1]),
          textAlign: 'center',
        }}
      >
        <p style={{color: 'rgba(255,255,255,0.6)', fontSize: 16}}>
          Made with ❤️ by the OpenClaw Community
        </p>      </div>
    </div>
  );
};
