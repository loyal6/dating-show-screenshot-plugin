<div align="center">

# 恋综截图生成器

**Dating Show Screenshot · Codex Plugin**

把普通照片一键处理成虚构的中文恋综或生活综艺截图。

[![Tests](https://github.com/loyal6/dating-show-screenshot-plugin/actions/workflows/test.yml/badge.svg)](https://github.com/loyal6/dating-show-screenshot-plugin/actions/workflows/test.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Codex Plugin](https://img.shields.io/badge/Codex-Plugin-E74866.svg)](.agents/plugins/marketplace.json)

</div>

插件会尽量保留人物、服装与原场景，按画面选择生活、游戏、出游、朋友或轻暧昧对白，再添加原创台标、英文花字、字幕、弹幕与虚构冠名包装。

![标准生成示例](examples/demo-output.png)

![照片卡生成示例](examples/demo-photo-card.png)

> 示例人物与场景均为 AI 生成；仓库不包含真实综艺截图、真实电视台标、真实节目名、艺人图或商业品牌素材。

## 快速使用

安装后上传一张照片，直接发送：

```text
用恋综截图生成器处理这张图，自动选一句生活化对白。
```

如果需要弹幕：

```text
用恋综截图生成器处理这张图，自动匹配台标、花字和地区食物冠名，
添加中等数量的顶部弹幕，避开人物脸部。
```

## 功能

- 场景识别与 13 类中文文案库，默认优先生活化内容，不强行恋爱导向。
- 10 个虚构台名预设，例如双鸭山卫视、牡丹江卫视、漓江卫视和西湖卫视。
- 两种台标模式严格二选一：
  - 地区轮廓：只显示抽象/示意地图轮廓；
  - 原创台标：只显示原创图形标识。
- 6 套透明英文花字：`Little Moments`、`Play Along`、`Taste of Today`、`Wander Together`、`After Sunset`、`Between Us`。
- 字幕会把“说话人＋斜杠＋对白”作为一个整体在安全区内居中，下划线随整组文字自动伸缩。
- 渐变雾带与字幕下划线共享同一段动态宽度；英文花字保留清晰笔画、轻微倾斜并上移到说话人左上角后方；冠名牌文字采用无描边清晰渲染。
- 分角色电视字幕字体：台名和弹幕用粗黑体；下方“嘉宾＋对白”默认使用内置霞鹜文楷常规体；人物姓名默认使用内置白路彤彤手写体；冠名使用宋体/衬线体。
- 5 类透明地区食物/产品实拍冠名组件，默认按台名匹配并显示在右下角。
- 可选少量（3）、中等（7）、满屏（14）三档顶部弹幕。
- 弹幕复刻真实视频样式：统一白色粗字、轻描边，少量加入由用户图形转制的透明白色点赞图标与数字。
- 支持人物保护框；提供人物蒙版时，弹幕可从人物背后穿过。
- 可复现首批参考图的四类版式：标准字幕、顶部弹幕、倾斜白框照片卡、人物旁手写姓名标；照片卡与姓名标可独立启用。
- 默认使用 Pillow 无损图层合成：不重新生成照片，保留原始像素、原生分辨率、ICC 色彩配置与曝光，只叠加透明包装。
- 仅在用户明确要求改变照片内容时使用 Codex/ChatGPT 图像编辑。
- 竖图自动居中，使用暗化模糊背景扩展成 16:9；不拉伸、不裁人，也不缩小原图。

## 安装

### 环境要求

- Codex CLI；
- Python 3.10 或更高版本；
- Git；
- macOS、Linux 或 Windows PowerShell。

### 一键脚本

macOS / Linux：

```bash
git clone https://github.com/loyal6/dating-show-screenshot-plugin.git
cd dating-show-screenshot-plugin
./install.sh
```

Windows PowerShell：

```powershell
git clone https://github.com/loyal6/dating-show-screenshot-plugin.git
cd dating-show-screenshot-plugin
.\install.ps1
```

### 手动安装

```bash
python3 -m pip install -r requirements.txt
codex plugin marketplace add "$PWD"
codex plugin add dating-show-screenshot@dating-show-screenshot
```

安装后，在 Codex 中上传照片并说：

```text
用恋综截图生成器处理这张图，自动选一句生活化对白。
```

安装脚本会安装 Python 运行依赖、注册仓库内的 Codex marketplace，并安装
`dating-show-screenshot` 插件；不会上传你的照片。

## 可以直接复制的使用示例

先上传需要处理的照片，再发送下面任意一段话。

### 1. 最简单：全部自动

```text
用恋综截图生成器处理这张图。自动判断场景，选择一句自然、生活化的对白；台标、英文花字和地区食物冠名也自动匹配。不要加弹幕。
```

只需要提供：**一张照片**。其余内容会自动选择。

### 2. 指定模板

```text
用恋综截图生成器处理这张图。
模板：顶部弹幕
台名预设：漓江卫视
对白类型：游戏互动
说话人：嘉宾
对白：自动选择
弹幕：中等
冠名：按台名自动匹配
```

模板可选：

- `标准`：台标、英文花字、渐变字幕、右下角冠名；
- `顶部弹幕`：标准模板加少量 / 中等 / 满屏三档弹幕；
- `照片卡`：倾斜白框照片叠在暗色模糊背景上；
- `嘉宾介绍`：在每个人物头部或肩部旁添加轻盈白色手写姓名和玫粉色上扬短笔触；不会生成身份卡片或“嘉宾：姓名”标签。

### 3. 完整 DIY

```text
用恋综截图生成器处理这张图。
模板：标准
台名：月牙湾卫视
台标：使用我同时上传的透明PNG，只使用图标，不叠加地图
英文花字：Weekend Mode，使用我同时上传的透明PNG
说话人：小满
对白：冰棍先别吃，给我留一口。
冠名：桂林米粉独家冠名
冠名素材：使用我同时上传的透明PNG
弹幕：不要
人物和原场景保持不变，输出16:9。
```

DIY 时按需要提供以下信息；没有写的项目会自动匹配：

| 项目 | 怎么提供 |
|---|---|
| 原照片 | 必需，直接上传 |
| 模板 | 标准 / 顶部弹幕 / 照片卡 / 嘉宾介绍 |
| 对白 | 写“自动选择”，或给出需要逐字显示的句子 |
| 说话人 | 嘉宾、主持人或自定义姓名 |
| 台名 | 选择内置预设，或填写自定义名称 |
| 台标 | 可上传透明 PNG；地图轮廓与图标必须二选一 |
| 英文花字 | 使用内置花字，或上传透明 PNG 并给出英文 |
| 冠名 | 自动匹配，或填写“食物名＋独家冠名” |
| 弹幕 | 不要 / 少量 / 中等 / 满屏，也可逐条填写 |
| 姓名标 | 填写人物姓名，并说明对应左边、中间或右边的人 |

## 命令行用法

脚本自带可再分发的 Noto Sans SC 与 Noto Serif SC 简体中文字体子集，无需另外指定字体：

```bash
python plugins/dating-show-screenshot/skills/make-dating-show-screenshot/scripts/render_dating_show.py \
  --input photo.jpg \
  --output photo-show.png \
  --category 做饭吃饭 \
  --station-preset xihu \
  --speaker 嘉宾 \
  --comments 3 \
  --seed 7
```

默认输出为无损 PNG。输入已经是 16:9 时保留原始尺寸；其他比例只扩展到能完整容纳原图的最小 16:9 画布。只有明确同时传入 `--width` 和 `--height` 时才会缩放。

常用自定义参数：

```bash
--line "先拍照，谁都不许动筷子。"
--station "自定义卫视"
--station-bug /absolute/path/logo-or-map.png
--flourish /absolute/path/wordmark.png
--sponsor "桂林米粉"
--sponsor-designation "独家冠名"
--sponsor-style noodle-bowl-lockup
--sponsor-asset /absolute/path/food-and-gold-plaque.png
--presentation photo-card
--name-tag "小满@0.35,0.30"
--name-font /absolute/path/handwritten-chinese.ttf
--name-curve /absolute/path/transparent-pink-curve.png
--danmaku-density medium
--comment "冰棍要化了"
--comment "她真的很会拍"
--protect-zone "0.36,0.02,0.64,0.34"
--subject-mask /absolute/path/person-mask.png
--station-font /absolute/path/station-font.ttf
--caption-font /absolute/path/dialogue-font.ttf
--sponsor-font /absolute/path/sponsor-font.ttf
--no-sponsor
```

`--station-bug` 接受透明 PNG；请自行保证它是“单独地图轮廓”或“单独原创图标”，不要把两者叠成一枚台标。

`--name-tag "文字@X,Y"` 使用 0–1 的归一化画布坐标，可重复传入。坐标应放在对应人物头部或上肩旁的留白处。默认使用白路彤彤手写体、轻微倾斜，以及用户提供的透明粉色弧线；弧线会按姓名实测宽度缩放，并从字形下部穿过。不会生成方框、身份说明或 `嘉宾：姓名`。`--name-font` 可单独替换姓名字体，`--name-curve` 可替换透明弧线，两者都不影响下方对白。`--presentation photo-card` 会生成暗化模糊背景、倾斜白框照片卡，并继续叠加台标、字幕和冠名；只有同时传入 `--name-tag` 时才会组合姓名标。

`--danmaku-density light|medium|full` 分别生成 3、7、14 条弹幕；需要逐字指定时，重复使用 `--comment "弹幕内容"`，最多 24 条。排版集中在顶部两至三条紧凑轨道，优先填满右上空间并避开台标；样式统一为白色粗字与轻描边，只在少数弹幕后加入点赞图标和数字。

`--protect-zone "X1,Y1,X2,Y2"` 使用 0–1 坐标保护人物或脸部区域，可重复提供。若准备了与原图同尺寸的黑白人物蒙版，使用 `--subject-mask person-mask.png`：白色人物会重新盖在弹幕上方，形成弹幕从人物背后穿过的效果。

字体也可以分角色 DIY：`--station-font` 控制台名、独播标和弹幕，`--caption-font` 控制对白，`--name-font` 控制人物姓名，`--name-curve` 控制姓名下方的透明粉色笔触，`--sponsor-font` 控制冠名牌。旧参数 `--font` 仍可一次覆盖全部文字。

默认冠名按台名匹配：

| 台名预设 | 默认冠名 |
|---|---|
| 双鸭山卫视 | 赫哲全鱼宴独家冠名 |
| 牡丹江卫视 | 镜泊湖鱼宴独家冠名 |
| 漓江卫视 | 桂林米粉独家冠名 |
| 洱海卫视 | 大理乳扇独家冠名 |
| 阿勒泰卫视 | 阿勒泰驼乳粉独家冠名 |
| 敦煌卫视 | 驴肉黄面独家冠名 |
| 漠河卫视 | 漠河冷水鱼独家冠名 |
| 西湖卫视 | 西湖藕粉独家冠名 |
| 亚龙湾卫视 | 海南清补凉独家冠名 |
| 鼓浪屿卫视 | 厦门沙茶面独家冠名 |

## DIY

| 想改什么 | 修改位置 |
|---|---|
| 中文对白 | `references/dialogues.json` |
| 台名与台标模式 | `references/station-presets.json` |
| 英文花字匹配 | `references/flourish-presets.json` |
| 台名与地区食物冠名映射 | `references/sponsor-presets.json` |
| 台标透明 PNG | `assets/station-icons/` 或 `assets/maps/` |
| 英文花字透明 PNG | `assets/flourishes/` |
| 白色点赞透明 PNG | `assets/ui/like-white.png` |
| 食物/产品抠图与金色冠名牌 | `assets/sponsors/` |
| 台名、对白与冠名字体 | `assets/fonts/` 或命令行字体参数 |
| 排版与图像编辑提示 | `references/style-spec.md` |

以上路径都位于：

```text
plugins/dating-show-screenshot/skills/make-dating-show-screenshot/
```

新增预设后运行测试，资源缺失、台标双模式混用、透明通道错误都会被自动检查。

## 开发与测试

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python scripts/validate_repo.py
```

GitHub Actions 会在 push 和 pull request 时执行相同检查，包括两种台标模式的冒烟渲染。

## 项目结构

```text
.
├── .agents/plugins/marketplace.json       # Codex marketplace 入口
├── .github/workflows/test.yml             # 自动测试
├── examples/                              # 纯生成示例图
├── plugins/dating-show-screenshot/
│   ├── .codex-plugin/plugin.json          # 插件清单
│   └── skills/make-dating-show-screenshot/
│       ├── SKILL.md                        # Codex 工作流
│       ├── assets/                         # 台标、花字、冠名、字体
│       ├── references/                     # 文案与视觉预设
│       └── scripts/                        # 确定性渲染器
├── install.sh / install.ps1                # 一键安装
├── tests/                                  # 自动测试
└── LICENSE
```

发现问题或希望增加模板，可在
[GitHub Issues](https://github.com/loyal6/dating-show-screenshot-plugin/issues) 提交。

## 版权、地图与品牌说明

- 代码采用 MIT License。
- 原创台标、花字与无品牌冠名组件随仓库按 MIT 授权；字体仍按 SIL OFL 1.1 授权。
- 地区轮廓来自公开 GeoJSON 的衍生示意图，不是官方标准地图，不能用于导航、测绘或行政边界判断。
- 若在中国大陆公开传播带行政边界的成品，请根据用途改用合规审图或官方标准地图来源；也可以只启用 `bug_mode: icon` 的原创台标模式。
- 不得用本项目冒充真实电视播出画面，也不要加入未经许可的真实台标、节目名、艺人肖像或商业品牌。

完整来源与许可证见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
地区食物名称的事实来源见技能内的 `references/regional-food-sources.md`。

## 许可证

[MIT](LICENSE)
