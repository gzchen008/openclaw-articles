import { Composition } from 'remotion';
import { ClawhubCodingVideo } from './ClawhubCodingVideo';
import { ClawhubCodingVideoVertical } from './ClawhubCodingVideoVertical';
import { ImageVideoToolsVertical } from './ImageVideoToolsVertical';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="ClawhubCodingVideo"
        component={ClawhubCodingVideo}
        durationInFrames={270}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ClawhubCodingVideoVertical"
        component={ClawhubCodingVideoVertical}
        durationInFrames={1020}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="ImageVideoToolsVertical"
        component={ImageVideoToolsVertical}
        durationInFrames={1020}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
