import React from 'react';
import { Composition } from 'remotion';
import { PaperclipVideo } from './PaperclipVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="PaperclipVideo"
        component={PaperclipVideo}
        durationInFrames={990}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
