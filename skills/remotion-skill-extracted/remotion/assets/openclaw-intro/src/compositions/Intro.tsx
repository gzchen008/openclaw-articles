import {useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';

export const Intro: React.FC<{title: string; subtitle: string}> = ({title, subtitle}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: {damping: 15, stiffness: 100},
  });

  const opacity = interpolate(frame, [0, 30], [0, 1]);

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
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
          textAlign: 'center',
        }}
      >
        <h1
          style={{
            color: 'white',
            fontSize: 120,
            fontWeight: 800,
            margin: 0,
            textShadow: '0 4px 20px rgba(0,0,0,0.3)',
          }}
        >
          {title}
        </h1>        <p
          style={{
            color: 'rgba(255,255,255,0.9)',
            fontSize: 36,
            marginTop: 20,
            fontWeight: 400,
          }}
        >
          {subtitle}
        </p>
      </div>
    </div>
  );
};
