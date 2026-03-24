import React from 'react';
import {Composition} from 'remotion';
import NotebookLMCompetitorsVideo from './NotebookLMCompetitorsVideo';
import NotebookLMCompetitorsVideoVerticalFixed from './NotebookLMCompetitorsVideoVertical-Fixed';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 横屏版本 */}
      <Composition
        id="NotebookLMCompetitorsVideo"
        component={NotebookLMCompetitorsVideo}
        durationInFrames={990} // 33秒 @ 30fps
        fps={30}
        width={1920}
        height={1080}
      />
      
      {/* 竖屏版本 - 完全居中 */}
      <Composition
        id="NotebookLMCompetitorsVideoVerticalFixed"
        component={NotebookLMCompetitorsVideoVerticalFixed}
        durationInFrames={990} // 33秒 @ 30fps
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
