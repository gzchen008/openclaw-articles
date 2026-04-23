import React from "react";
import { Composition } from "remotion";
import { DokobotVideo } from "./Video";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="DokobotVideo"
      component={DokobotVideo}
      durationInFrames={2220}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
