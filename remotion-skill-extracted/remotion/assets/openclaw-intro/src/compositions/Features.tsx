import {useCurrentFrame, interpolate} from 'remotion';

export const Features: React.FC = () => {
  const frame = useCurrentFrame();

  const codeExample = `OpenClaw, 帮我：
• 每天早上9点发送工作日报
• 监控GitHub新Star项目
• 定时备份重要数据`;

  const demos = [
    {icon: '🤖', label: 'AI对话', cmd: '"帮我分析这份数据"'},
    {icon: '⏰', label: '定时任务', cmd: '每天10点查天气'},
    {icon: '🌐', label: '浏览器', cmd: '自动抓取网页'},
    {icon: '📧', label: '消息推送', cmd: 'Discord/邮件/Slack'},
  ];

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        background: '#0f0f23',
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
          color: '#00d4ff',
          fontSize: 48,
          marginBottom: 40,
          opacity: interpolate(frame, [0, 20], [0, 1]),
        }}
      >
        看看它能做什么
      </h2>

      <div style={{display: 'flex', gap: 40, maxWidth: 1200}}>
        {/* 代码示例 */}
        <div
          style={{
            flex: 1,
            background: '#1e1e2e',
            borderRadius: 16,
            padding: 32,
            opacity: interpolate(frame, [30, 50], [0, 1]),
            transform: `translateX(${interpolate(frame, [30, 50], [-50, 0])}px)`,
          }}
        >
          <div
            style={{
              color: '#00d4ff',
              fontSize: 14,
              marginBottom: 16,
              textTransform: 'uppercase',
              letterSpacing: 1,
            }}
          >
            自然语言指令
          </div>
          <pre
            style={{
              color: '#a6e3a1',
              fontSize: 18,
              fontFamily: 'monospace',
              margin: 0,
              lineHeight: 1.8,
            }}
          >
            {codeExample}
          </pre>
        </div>

        {/* 功能演示 */}
        <div
          style={{
            flex: 1,
            display: 'grid',
            gridTemplateColumns: 'repeat(2, 1fr)',
            gap: 20,
          }}
        >
          {demos.map((demo, index) => {
            const delay = 50 + index * 15;
            const opacity = interpolate(frame, [delay, delay + 15], [0, 1]);
            const scale = interpolate(frame, [delay, delay + 20], [0.9, 1]);

            return (
              <div
                key={index}
                style={{
                  background: 'rgba(0,212,255,0.1)',
                  border: '1px solid rgba(0,212,255,0.3)',
                  borderRadius: 12,
                  padding: 24,
                  opacity,
                  transform: `scale(${scale})`,
                }}
              >
                <div style={{fontSize: 32, marginBottom: 8}}>{demo.icon}</div>
                <div style={{color: 'white', fontSize: 16, fontWeight: 600}}>
                  {demo.label}
                </div>
                <div
                  style={{
                    color: '#888',
                    fontSize: 13,
                    marginTop: 4,
                    fontFamily: 'monospace',
                  }}
                >
                  {demo.cmd}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
