# 用 AI 剪视频？browser-use 团队开源 video-use，让 Claude Code 帮你剪辑

> 把原始素材丢进文件夹，跟 Claude 聊几句，拿回一个 `final.mp4`。

## 🤖 这是什么项目？

**video-use** 是 browser-use 团队的最新开源项目。你没看错——就是那个做 AI 浏览器代理的 browser-use。这次他们把目光从网页转向了视频。

核心思路极其简洁：**用 LLM 代替剪辑师，但不是让 AI "看"视频，而是让 AI "读"视频。**

把原始素材扔进一个文件夹，启动 Claude Code，说一句"帮我剪个发布视频"，它就会自动完成从转录、剪辑、调色、字幕到动画叠加的全流程。

不需要预设模板，不需要拖拽时间线，不需要学习 Premiere。就是聊天。

## 🔧 它能做什么？

具体来说，video-use 覆盖了一个完整视频剪辑工作流的几乎所有环节：

<p style="margin: 4px 0; padding-left: 20px;">• <strong>智能去 filler</strong>：自动识别并剪掉"嗯""啊"、口误、重复和拍摄间隙的空白</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>自动调色</strong>：每段素材独立调色，支持暖色调电影感、中性风格或自定义 ffmpeg 滤镜链</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>音频平滑过渡</strong>：每个剪切点自动加 30ms 淡入淡出，杜绝爆音</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>字幕烧录</strong>：默认 2 词一组的大写字幕，完全可自定义样式</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>动画生成</strong>：通过 Manim、Remotion 或 PIL 生成动画叠加层，每个动画由独立的子 Agent 并行执行</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>自评估机制</strong>：渲染完成后自动在每个剪切点检查画面跳变、音频爆音、字幕遮挡</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>会话记忆</strong>：通过 project.md 持久化，下次对话无缝接续上次进度</p>

## 🧠 技术架构：不"看"视频，而是"读"视频

这是整个项目最巧妙的设计。

传统 AI 视频处理的思路是把视频拆成帧，逐帧喂给视觉模型。问题很明显：一段 30 秒的视频大约 900 帧，每帧 1500 tokens，总共 135 万 tokens——绝大部分是冗余信息。

video-use 采用了完全不同的策略：**两层信息架构**。

**第一层——音频转录（始终加载）。** 通过 ElevenLabs Scribe API，对每段素材做一次转录，拿到词级时间戳、说话人分离和音频事件（笑声、掌声、叹息等）。所有片段打包成一个约 12KB 的 `takes_packed.md` 文件——这就是 LLM 的"阅读视图"。

第二层——视觉合成（按需加载）。`timeline_view` 工具可以在任意时间范围生成胶片条 + 波形 + 词标注的 PNG 图片。只在需要决策的时候调用——比如判断一个停顿是否应该保留、对比两次拍摄的差异。

效果对比：朴素的逐帧方案需要 <strong>4500 万 tokens 的噪音</strong>；video-use 只需要 <strong>12KB 文本 + 几张 PNG</strong>。

这和 browser-use 的核心理念一脉相承——不是给 LLM 看截图，而是给它结构化的 DOM。只不过这次，DOM 换成了转录文本。

## 📋 处理流水线

整个剪辑流程是一条清晰的流水线：

<p style="margin: 8px 0; padding-left: 20px; font-family: monospace; font-size: 14px; color: #24292e;">转录 → 打包 → LLM 推理 → 生成 EDL → 渲染 → 自评估</p>

其中自评估环节会检查渲染后的输出，在每个剪切点运行 `timeline_view`，捕捉画面跳变、音频爆音和字幕遮挡。发现问题会自动修复并重新渲染（最多 3 轮）。只有通过检查的结果才会展示给用户。

## 🚀 如何使用？

安装非常简单：

<p style="margin: 8px 0; padding-left: 20px; font-family: monospace; font-size: 14px; color: #24292e;">git clone https://github.com/browser-use/video-use<br>cd video-use<br>ln -s "$(pwd)" ~/.claude/skills/video-use<br>pip install -e .<br>brew install ffmpeg</p>

配置 ElevenLabs API Key 后，把素材放到一个文件夹里：

<p style="margin: 8px 0; padding-left: 20px; font-family: monospace; font-size: 14px; color: #24292e;">cd /path/to/your/videos<br>claude</p>

然后在 Claude Code 里说：

<p style="margin: 8px 0; padding-left: 20px; font-family: monospace; font-size: 14px; color: #24292e;">edit these into a launch video</p>

它会自动扫描素材、提出剪辑策略、等你确认后执行，最终输出到 `edit/final.mp4`。

## 🎯 适用场景

video-use 的设计原则是"不做内容假设"，理论上适用于任何类型的视频：

<p style="margin: 4px 0; padding-left: 20px;">• <strong>口播视频</strong>：去 filler、去空白、加字幕，效果最直接</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>教程/课程</strong>：自动剪辑多段拍摄，保留核心讲解</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>访谈/播客</strong>：说话人分离 + 自动剪掉无效片段</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>Vlog/旅行</strong>：多段素材智能拼接，自动调色统一风格</p>
<p style="margin: 4px 0; padding-left: 20px;">• <strong>产品发布</strong>：配合 Manim/Remotion 生成动画叠加层</p>

## 💡 设计哲学

项目有 5 条核心设计原则，值得每个 AI 工具开发者参考：

<p style="margin: 4px 0; padding-left: 20px;">1. <strong>文本优先，视觉按需</strong>：不暴力灌帧，转录文本是主视图</p>
<p style="margin: 4px 0; padding-left: 20px;">2. <strong>音频主导，画面跟随</strong>：剪切点来自语音边界和静音间隙</p>
<p style="margin: 4px 0; padding-left: 20px;">3. <strong>先问后做</strong>：永远不碰时间线，直到用户确认策略</p>
<p style="margin: 4px 0; padding-left: 20px;">4. <strong>零内容假设</strong>：不预设视频类型，看了再说</p>
<p style="margin: 4px 0; padding-left: 20px;">5. <strong>硬规则 + 艺术自由</strong>：生产正确性不可妥协，审美风格自由发挥</p>

最后一条特别有意思——SKILL.md 里定义了 12 条"硬规则"（比如字幕必须最后叠加、每个剪切点必须有音频淡入淡出、绝不能在单词中间剪切），其余全部是"参考示例而非强制规范"。这种" correctness 不可谈判，taste 随你发挥"的设计哲学，在 AI 工具里相当少见。

## ⚠️ 局限性

<p style="margin: 4px 0; padding-left: 20px;">• 依赖 Claude Code，不是通用的 LLM 方案</p>
<p style="margin: 4px 0; padding-left: 20px;">• 需要 ElevenLabs API（付费服务）做转录</p>
<p style="margin: 4px 0; padding-left: 20px;">• 主要针对说话类视频，纯画面类视频（如风景延时）支持有限</p>
<p style="margin: 4px 0; padding-left: 20px;">• 动画生成需要额外依赖（Manim/Remotion）</p>

## 📌 总结

video-use 代表了一种 AI 与创意工具结合的新范式：**不是用 AI 替代剪辑软件，而是用对话替代 GUI**。

它的核心洞察——"让 LLM 读转录文本而不是看视频帧"——大幅降低了 token 消耗，同时保留了足够的编辑精度。自评估机制和 12 条硬规则则确保了输出质量不会因为"AI 的自由发挥"而翻车。

对于经常需要剪辑口播、教程、访谈类视频的创作者来说，这个工具值得试用。对于开发者来说，它的"文本优先 + 按需视觉"架构思路，同样值得借鉴。

<p style="margin: 8px 0;">项目地址：<strong>https://github.com/browser-use/video-use</strong></p>

<p style="margin: 8px 0;">如果觉得有用，点个"在看"吧 👇</p>
