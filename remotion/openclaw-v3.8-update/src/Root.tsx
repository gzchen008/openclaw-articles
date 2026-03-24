import React from "react";
import { Composition } from "remotion";
import { OpenClawUpdate } from "./Video";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="OpenClawUpdate"
        component={OpenClawUpdate}
        durationInFrames={990}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
