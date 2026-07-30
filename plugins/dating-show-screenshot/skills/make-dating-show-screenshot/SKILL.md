---
name: make-dating-show-screenshot
description: Turn an uploaded photo into a polished fictional Chinese dating- or lifestyle-reality-show screenshot while preserving the people and scene. Use for requests such as 恋综截图、生活综艺字幕、游戏互动、合住日常、卫视独播角标、暧昧对白、朋友闲聊、观察室弹幕、嘉宾采访画面、综艺感P图, or when the user wants to import a photo and generate a similar 16:9 TV-show frame in one step.
---

# Make Dating Show Screenshot

Create a fictional entertainment screenshot from one user-supplied image. Preserve identities, faces, bodies, poses, clothing, objects, and camera framing unless the user asks for other edits.

## Workflow

1. Inspect the edit target with `view_image`.
2. Classify the visible moment before choosing text:
   - kitchen/table/food → `做饭吃饭` or `合住日常`
   - games/sports/group task → `游戏互动` or `轻松吐槽`
   - outdoor/travel/beach → `出游行动`
   - shared home/sofa/bedroom → `合住日常` or `朋友闲聊`
   - quiet night conversation → `朋友闲聊` or `暧昧试探`
   - portrait/interview → `采访回应`
   - only use romance categories when expressions or user intent support them
3. Read `references/dialogues.json` when the user has not supplied exact copy. Pick one natural line that matches the scene; do not ask unless speaker identity or tone is genuinely ambiguous.
4. Read `references/station-presets.json` and select a fictional local station that matches the scene. Use city or scenic names, not a real province-level broadcaster.
5. Read `references/style-spec.md` for layout and prompting. Use exactly one selected station-bug asset:
   - `bug_mode: map` → a single illustrative regional silhouette from `assets/maps/`;
   - `bug_mode: icon` → a single original broadcast emblem from `assets/station-icons/`.
   Never combine the map and emblem in the same bug.
6. Read `references/flourish-presets.json` and include its transparent handwritten-English wordmark in the lower third.
7. Read `references/sponsor-presets.json` and add the selected station's regional-food sponsor lockup at bottom right unless the user asks to remove it. Keep the food cutout, champagne-gold plaque, and exact one-line copy together.
8. Use `scripts/render_dating_show.py` by default when the request only adds broadcast graphics. This path must preserve the source photo pixels, native resolution, ICC color profile, framing, and color; add transparent layers only and save as lossless PNG. Do not send an overlay-only edit through image generation.
9. Use built-in `image_gen` only when the user explicitly requests generative changes to the photograph itself:
   - load the edit target, the selected station asset, the selected English flourish, and the selected sponsor plate;
   - treat the uploaded photo as the edit target and bundled assets only as graphic/layout references;
   - preserve all photographic content that the user did not ask to change.
10. Inspect the result. Check exact Chinese copy, source resolution and color preservation, one-mode-only station bug, a recognizable slightly tilted flourish sitting high behind the speaker label, a centered lower-third group, a measured underline and bottom-up gradient sharing the same horizontal span, crisp sponsor copy, and absence of unintended people or objects.
    For cast introductions, also check that every name sits beside its matching person's head or upper shoulder in Bai Lu Tongtong-style airy white handwriting, with the supplied pink curve passing behind the lower part of the glyphs. Never render a boxed identity chip, `嘉宾：姓名`, or an app-style label.
11. If only the text or graphic placement is wrong, rerender deterministically instead of regenerating the photograph.
12. Save non-destructively and return the image.

## Default Creative Choices

- Default content is scene-aware and life-oriented, not automatically romantic.
- Default role: `嘉宾`.
- Default graphics: station bug + English flourish + pink-gray gradient lower third + station-linked regional-food sponsor lockup. Keep bullet comments off unless requested or clearly useful.
- Default output: lossless PNG at the source photo's native resolution. Keep native 16:9 images pixel-for-pixel beneath the overlays; for other aspect ratios, expand to the smallest 16:9 canvas that contains the full source without downscaling. Only resize when the user explicitly supplies output dimensions.
- Recreate all layout variants shown in the initial references when requested:
  - standard station bug + gradient lower third + sponsor;
  - light (3), medium (7), or full (14) mixed-format floating comments;
  - tilted white-border photo card over a dark blurred background;
  - multiple white cast-name labels with short pink underline strokes.
- Station presets:
  - `shuangyashan` → 双鸭山卫视 / 赫哲全鱼宴独家冠名
  - `mudanjiang` → 牡丹江卫视 / 镜泊湖鱼宴独家冠名
  - `lijiang` → 漓江卫视 / 桂林米粉独家冠名
  - `erhai` → 洱海卫视 / 大理乳扇独家冠名
  - `aletai` → 阿勒泰卫视 / 阿勒泰驼乳粉独家冠名
  - `dunhuang` → 敦煌卫视 / 驴肉黄面独家冠名
  - `mohe` → 漠河卫视 / 漠河冷水鱼独家冠名
  - `xihu` → 西湖卫视 / 西湖藕粉独家冠名
  - `yalongwan` → 亚龙湾卫视 / 海南清补凉独家冠名
  - `gulangyu` → 鼓浪屿卫视 / 厦门沙茶面独家冠名

Never imply that the result is a genuine broadcast still. Do not recreate real broadcaster trademarks or add real program titles, sponsor brands, or celebrity cutouts unless the user supplies them and asks to retain them. All bundled station emblems, English flourishes, sponsor plates, and sponsor names are fictional.

## Exact-Text Rendering

Scene-matched local station:

```bash
python scripts/render_dating_show.py \
  --input /absolute/path/photo.jpg \
  --output /absolute/path/photo-show.png \
  --speaker "嘉宾" \
  --category "游戏互动" \
  --station-preset "dunhuang" \
  --seed 7 \
  --comments 4 \
  --sponsor "驴肉黄面"
```

Exact custom line and station text:

```bash
python scripts/render_dating_show.py \
  --input /absolute/path/photo.jpg \
  --output /absolute/path/photo-show.png \
  --speaker "嘉宾" \
  --line "先拍照，谁都不许动筷子。" \
  --category "做饭吃饭" \
  --station-preset "xihu" \
  --station "西湖卫视"
```

Use `--station-bug /absolute/path/logo-or-map.png` to DIY the top-left asset, `--flourish /absolute/path/wordmark.png` to replace the English flourish, `--sponsor "自定义食物名"` to change the sponsor name, `--sponsor-asset /absolute/path/food-lockup.png` to replace the transparent food-and-plaque lockup, or `--no-sponsor` to remove it.

Recreate the tilted-photo reference variant:

```bash
python scripts/render_dating_show.py \
  --input /absolute/path/photo.jpg \
  --output /absolute/path/photo-card-show.png \
  --presentation photo-card \
  --station-preset lijiang \
  --category 朋友闲聊
```

Recreate the cast-introduction reference variant:

```bash
python scripts/render_dating_show.py \
  --input /absolute/path/group-photo.jpg \
  --output /absolute/path/cast-introduction.png \
  --station-preset lijiang \
  --category 朋友闲聊 \
  --name-tag "小满@0.34,0.31" \
  --name-tag "阿禾@0.61,0.27"
```

Use `--danmaku-density light|medium|full` for 3, 7, or 14 automatically selected comments. Match the reference with consistent bold white text, a restrained dark edge, and only occasional aligned like icons plus counts. Use two or three compact top lanes, fill the upper-right area, and keep the station bug clear. Repeat `--comment "准确弹幕"` up to 24 times for exact copy.

Protect important people in either of two ways:

- repeat `--protect-zone X1,Y1,X2,Y2` with normalized coordinates to reserve face/subject rectangles;
- pass `--subject-mask person-mask.png` with white subject pixels and black background to restore the person above the comments, making the comments visually pass behind them. The mask must match the input dimensions and currently supports the standard presentation.

`--name-tag "文字@X,Y"` accepts normalized coordinates from 0 to 1 and can be repeated for group shots. Inspect the photo and place each anchor in nearby negative space beside the corresponding head or upper shoulder; do not center names on faces or arrange them as a detached legend. The renderer uses the bundled Bai Lu Tongtong handwriting font and the bundled transparent pink curve supplied by the user. Use `--name-font` to supply another handwritten Chinese font, or `--name-curve` to replace the curve, without changing the lower-third.

Typography is independently DIY-able. By default, the lower-third speaker label and dialogue use the bundled `LXGWWenKai-Regular.ttf`. Use `--station-font` for the station name, badge, and comments; `--caption-font` to explicitly override the lower-third; `--name-font` for cast names; and `--sponsor-font` for the sponsor plaque. The legacy `--font` option still overrides every role at once.

## Resources

- `references/dialogues.json`: scene-oriented line, commentary, and floating-comment bank.
- `references/station-presets.json`: local/scenic station names and one-mode-only map or emblem choices.
- `references/flourish-presets.json`: scene-to-English-wordmark mapping.
- `references/sponsor-presets.json`: station-to-regional-food sponsor mapping.
- `references/regional-food-sources.md`: factual sources for the regional-food pairings.
- `references/style-spec.md`: scene routing, layout, and image-edit prompt.
- `references/icon-sources.md`: open-source provenance and non-infringement guardrails.
- `assets/maps/`: transparent illustrative city/prefecture silhouettes.
- `assets/station-icons/`: five transparent original station emblems.
- `assets/flourishes/`: six transparent handwritten-English wordmarks.
- `assets/sponsors/`: transparent fictional food/product cutouts with blank champagne-gold plaques.
- `assets/ui/like-white.png`: transparent white like icon derived from the user-supplied silhouette.
- `assets/ui/cast-name-curve.png`: cropped transparent pink curve supplied by the user.
- `assets/fonts/`: bundled Noto Sans SC and Noto Serif SC under SIL OFL, plus the author-declared Bai Lu Tongtong handwriting font and its source notice.
