import React from 'react';
import {Composition} from 'remotion';
import {AgentLoopVideo} from './Video';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="AgentLoopVideo"
        component={AgentLoopVideo}
        durationInFrames={1440}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
