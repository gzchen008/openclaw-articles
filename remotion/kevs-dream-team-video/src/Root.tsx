import { Composition } from "remotion";
import { KevsDreamTeamVideo, KevsDreamTeamVideoVertical } from "./KevsDreamTeamVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* 横屏版本：1920x1080 */}
      <Composition
        id="KevsDreamTeam"
        component={KevsDreamTeamVideo}
        durationInFrames={1000} // 约 33 秒
        fps={30}
        width={1920}
        height={1080}
      />
      
      {/* 竖屏版本：1080x1920（无封面） */}
      <Composition
        id="KevsDreamTeamVertical"
        component={KevsDreamTeamVideoVertical}
        durationInFrames={910} // 约 30 秒（减去封面）
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
