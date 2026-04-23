import React from 'react';
import { Composition } from 'remotion';
import { OpenClawUpdateVideo } from './OpenClawUpdateVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="OpenClawUpdate"
        component={OpenClawUpdateVideo}
        durationInFrames={900}
        fps={30}
        width={1920}  // 横屏
        height={1080} // 横屏
      />
    </>
  );
};
