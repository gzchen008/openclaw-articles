import {Composition} from 'remotion';
import {OpenClawIntro} from './compositions/OpenClawIntro';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="OpenClawIntro"
        component={OpenClawIntro}
        durationInFrames={1800}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: 'OpenClaw',
          subtitle: 'AI驱动的自动化助手',
        }}
      />
    </>
  );
};
