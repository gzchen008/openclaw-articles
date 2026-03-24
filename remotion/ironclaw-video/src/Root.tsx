import { Composition } from "remotion";
import { IronClawVideo } from "./IronClawVideo";
import { IronClawVideoVertical } from "./IronClawVideoVertical";

export const Root: React.FC = () => {
  return (
    <>
      {/* 横屏版本 */}
      <Composition
        id="IronClawVideo"
        component={IronClawVideo}
        durationInFrames={1020}
        fps={30}
        width={1920}
        height={1080}
      />
      
      {/* 竖屏版本 */}
      <Composition
        id="IronClawVideoVertical"
        component={IronClawVideoVertical}
        durationInFrames={1020}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
