import React from 'react';
import { Composition } from 'remotion';
import { ContextEngineVideo } from './ContextEngineVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ContextEngineVideo"
        component={ContextEngineVideo}
        durationInFrames={990}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
