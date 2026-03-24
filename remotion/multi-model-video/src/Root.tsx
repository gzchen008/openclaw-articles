import { Composition } from "remotion";
import { MultiModelVideo } from "./Video";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MultiModelVideo"
        component={MultiModelVideo}
        durationInFrames={1440}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
