import React from 'react';
import {Composition} from 'remotion';
import OpsAutomationVideo from './OpsAutomationVideo';
import OpsAutomationVideoVertical from './OpsAutomationVideoVertical';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 横屏版本 */}
      <Composition
        id="OpsAutomationVideo"
        component={OpsAutomationVideo}
        durationInFrames={1020} // 34秒 @ 30fps
        fps={30}
        width={1920}
        height={1080}
      />
      
      {/* 竖屏版本 */}
      <Composition
        id="OpsAutomationVideoVertical"
        component={OpsAutomationVideoVertical}
        durationInFrames={1020} // 34秒 @ 30fps
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
