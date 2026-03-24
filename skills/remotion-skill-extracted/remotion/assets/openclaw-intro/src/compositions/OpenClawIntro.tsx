import {Sequence} from 'remotion';
import {Intro} from './Intro';
import {PainPoint} from './PainPoint';
import {Solution} from './Solution';
import {Features} from './Features';
import {CTA} from './CTA';

export const OpenClawIntro: React.FC<{
  title: string;
  subtitle: string;
}> = ({title, subtitle}) => {
  return (
    <>
      {/* 开场: 0-5s (150 frames) */}
      <Sequence from={0} durationInFrames={150}>
        <Intro title={title} subtitle={subtitle} />
      </Sequence>

      {/* 痛点: 5-15s (150-450 frames) */}
      <Sequence from={150} durationInFrames={300}>
        <PainPoint />
      </Sequence>

      {/* 解决方案: 15-35s (450-1050 frames) */}
      <Sequence from={450} durationInFrames={600}>
        <Solution />
      </Sequence>

      {/* 功能展示: 35-60s (1050-1800 frames) */}
      <Sequence from={1050} durationInFrames={750}>
        <Features />
      </Sequence>

      {/* 行动号召: 60-75s (1800-2250 frames) */}
      <Sequence from={1800} durationInFrames={450}>
        <CTA />
      </Sequence>
    </>
  );
};
