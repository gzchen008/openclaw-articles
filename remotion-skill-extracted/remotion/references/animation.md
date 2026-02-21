# Remotion 动画技巧

## 常用动画模式

### 1. 淡入淡出 (Fade)

```tsx
const opacity = interpolate(
  frame,
  [0, 30, durationInFrames - 30, durationInFrames],
  [0, 1, 1, 0]
);
```

### 2. 滑动 (Slide)

```tsx
const translateX = interpolate(frame, [0, 30], [-100, 0]);
const translateY = interpolate(frame, [0, 30], [50, 0]);
```

### 3. 缩放 (Scale)

```tsx
const scale = interpolate(frame, [0, 30], [0.5, 1]);
// 或弹簧动画
const scale = spring({frame, fps, config: {damping: 10}});
```

### 4. 旋转 (Rotate)

```tsx
const rotate = interpolate(frame, [0, 100], [0, 360]);
```

### 5. 打字机效果

```tsx
const charsToShow = Math.floor(frame / 3);
const displayText = fullText.slice(0, charsToShow);
```

## 时间控制

### Sequence 分镜

```tsx
<Sequence from={0} durationInFrames={150}>
  <Scene1 />
</Sequence>
<Sequence from={150} durationInFrames={150}>
  <Scene2 />
</Sequence>
```

### 延迟动画

```tsx
const delay = 30;
const animatedFrame = frame - delay;
const opacity = interpolate(animatedFrame, [0, 20], [0, 1]);
```

## 缓动函数

```tsx
import {Easing} from 'remotion';

interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.bezier(0.34, 1.56, 0.64, 1), // 弹性
});

interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.ease), // 平滑
});
```
