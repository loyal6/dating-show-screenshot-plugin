# Fictional dating-show screenshot style

## Frame

- Canvas: preserve the source's native pixel dimensions when it is already 16:9. For other aspect ratios, expand to the smallest 16:9 canvas that contains the complete source without downscaling it. Use 1920×1080 only when the user explicitly requests it.
- Preserve the original photo pixels, ICC color profile, contrast, saturation, white balance, and exposure. Do not apply a broadcast grade to the photographic layer.
- For graphics-only edits, composite transparent overlays deterministically and save as lossless PNG. Do not regenerate, repaint, or JPEG-recompress the photograph.
- Keep faces, body shape, clothing, pose, background objects, and camera angle unchanged.
- If the source is not 16:9, keep the complete source centered and fill the remaining canvas with a darkened blurred copy of the photo. Do not crop people or stretch the source.

## Scene routing

Classify the photo before selecting graphics or copy:

| Scene cue | Dialogue bank | English flourish | Suggested station mood |
|---|---|---|---|
| Kitchen, table, food | 做饭吃饭 / 合住日常 | Taste of Today | 西湖、牡丹江 |
| Board game, sports, group task | 游戏互动 / 轻松吐槽 | Play Along | 敦煌 |
| Outdoor, travel, beach, landscape | 出游行动 / 轻松吐槽 | Wander Together | 漓江、阿勒泰、鼓浪屿、亚龙湾 |
| Sofa, bedroom, shared home | 合住日常 / 朋友闲聊 | Little Moments | 牡丹江、西湖 |
| Night, quiet one-to-one talk | 朋友闲聊 / 暧昧试探 | After Sunset | 洱海、漠河 |
| Portrait or interview | 采访回应 | Little Moments | 牡丹江 |
| Clear mutual attention | 暧昧试探 / 嘴硬逗趣 | Between Us | 双鸭山、亚龙湾 |

Do not force romance when the photo only suggests ordinary life, games, travel, food, or friendship.

## Top-left fictional station bug

- Position: 5% from left, 5–7% from top.
- Height: 54–72 px at 1920×1080.
- Structure:
  1. one illustrative city/prefecture map silhouette **or** one original station emblem;
  2. bold white station name;
  3. small rounded white `独播` pill.
- Never place an icon over a map. Each preset chooses exactly one of the two modes.
- Original emblems may use compact ribbons, waves, stars, bays, or mountain geometry in a restrained two-color palette. They should feel broadcast-ready but must not copy a real station trademark.
- Use local city or scenic names such as `双鸭山卫视`, `牡丹江卫视`, `漓江卫视`, `洱海卫视`, `阿勒泰卫视`, `敦煌卫视`, `漠河卫视`, `西湖卫视`, `亚龙湾卫视`, or `鼓浪屿卫视`.
- Do not default to a real province-level broadcaster. Do not recreate any real station trademark.
- Add a soft dark shadow only when the background is bright.
- Typography: use a compact semi-bold Chinese sans-serif for the station name and badge. This is the strongest type role in the frame.

## Lower third

- Position: low and wide across the lower 11–20% of the frame, following the first-generation result.
- Width: about 70% of the frame. Start near 12.5% from the left and stop before the bottom-right sponsor.
- Add one visually unified pink-gray airbrushed band that hugs the Chinese subtitle baseline. Measure the complete subtitle first, then make the band use exactly the same horizontal span as its underline. At 1920×1080 it should be roughly 105–115 px tall, with quiet cool-gray atmosphere and a soft muted-rose center. Keep the peak opacity restrained, feather the first and last 10% of that measured span, and leave the English flourish mostly outside the band. Never make it a translucent card or a stack of separately visible glow stripes.
- Center the complete `speaker + slash + dialogue` group as one measured unit inside the safe span from roughly 12.5% to 82% of the frame. Do not pin a short line to the left or center the dialogue independently from the speaker.
- Use one supplied transparent handwritten-English flourish as a recognizable background accent at the speaker label's upper-left. Keep it around 9–10% of frame width and 6–7% of frame height, retain roughly 70–75% opacity, rotate it only about 4° clockwise, and position it high enough that the full cursive silhouette remains legible while the speaker text covers only a small part of its lower-right edge. It must stay identifiable as lettering rather than dissolving into an anonymous decorative stroke.
- Speaker/role in white, then a thin white slash.
- Speaker/role and main dialogue: use the bundled LXGW WenKai Regular at 50–56 px. Render in white with only a restrained 1 px dark edge or soft shadow. Keep the literary Kai-style strokes readable and do not reuse the heavy station/comment treatment.
- Build the gray and rose as a bottom-up gradient: color is strongest immediately above the underline and fades continuously upward. Do not create a center glow or fade the color back out before it reaches the line. Crop the effect exactly at the underline so nothing extends below it.
- Underline: 2–3 px muted rose. Measure the complete `speaker + slash + dialogue` group and make the line follow that exact span with only about 1–1.5% frame-width padding on each side. Short copy must produce a visibly shorter line; never use a fixed full-width underline.
- Keep the subtitle above the very bottom edge; do not cover faces.

## Optional floating comments

- Offer three densities: light = 3 comments / 2 lanes, medium = 7 / 3 lanes, full = 14 / 3 dense lanes.
- Keep lanes compact across roughly the top 2–26% of the complete frame. Fill the upper-right area and keep the station bug clear.
- Match real video comments with consistent bold white text and a restrained dark edge. Add only occasional aligned white like icons plus counts; do not use colored emphasis, heart counters, or `热议` pills.
- Avoid important face/subject rectangles. When a subject mask is available, composite the person above the comments so danmaku may pass behind the person.
- Pack each lane from left to right with only a small text-width-aware gap. Comments may cross from background or side fill into the central image and may overlap hair or non-critical body areas; do not scatter them into distant corners or place one directly across the eyes and central facial features.
- Use bold white text with a soft black shadow.
- Comments should react to the action rather than repeat the main line.
- Everyday examples: `规则又白讲了`, `谁去救一下锅`, `今天也是全员迷路`.
- Avoid covering eyes and faces.

## Initial-reference layout variants

| Variant | Required composition |
|---|---|
| Standard | Station bug at top left, pink-gray gradient lower third, English flourish, one-line food sponsor at bottom right |
| Floating comments | Standard layout plus light, medium, or full mixed-format top-lane danmaku |
| Photo card | Dark blurred full-canvas background plus one slightly clockwise-tilted photo with a thick white border; keep station bug, lower third, and sponsor above it |
| Cast introduction | Standard layout plus one airy white handwritten name beside each visible person's head or upper shoulder and the supplied transparent pink brush curve |

Treat these as composable broadcast layers. Preserve the user's image and do not add real program titles, real broadcaster logos, celebrity cutouts, or real commercial brands.

### Cast-name treatment

- Place each name in nearby negative space beside its matching head or upper shoulder. Keep it close enough to read as identification, but never cover eyes or sit directly across a face.
- Use the bundled Bai Lu Tongtong font by default: elongated, naturally uneven white Chinese handwriting with a subtle counter-clockwise slant and restrained dark shadow. Do not substitute a brush-calligraphy font, heavy station font, or lower-third serif.
- Use `assets/ui/cast-name-curve.png` exactly as the default pink stroke. Scale it proportionally to about 113% of the measured name width, place it behind the lower quarter of the glyphs, and rotate it together with the name. Do not redraw it as a straight or synthetic two-line underline.
- Do not use a box, pill, identity card, `嘉宾：姓名`, profile description, occupation, age, location, or English transliteration unless the user explicitly requests those fields.
- Treat cast introduction and photo card as independent options. Combine them only when the user asks for both.

## Sponsor corner

- Bottom right, compact regional-food product lockup: one realistic food/product cutout above a blank champagne-gold nameplate.
- Show by default. Select by station preset, not by dialogue category.
- Render one exact line on the plaque with no space between the food name and designation, for example `桂林米粉独家冠名`.
- Use a compact Chinese Song/serif semi-bold for the sponsor plaque so it reads like a television title card rather than app UI.
- Keep the sponsor copy crisp at native resolution: use about 88–92% of the plaque's inner width, avoid translucent outlines or glow, and render the dark text without a stroke on light champagne-gold plates.
- Keep the lockup around 16–21% of frame width and 12–17% of frame height. Do not turn it into an app-style rounded card.
- Use only bundled original/generated cutouts or user-supplied assets. Do not insert a real commercial brand or celebrity cutout by default.

## Image edit prompt

```text
Use case: precise-object-edit
Asset type: fictional Chinese reality-show screenshot
Primary request: Add polished TV-broadcast graphics as transparent overlays to the uploaded photo.
Input images: Image 1 is the edit target. The other PNGs are the selected one-mode-only station bug, English flourish, and fictional sponsor plate.
Scene: <scene>. Tone: <tone>.
Composition: preserve the photo pixels, native resolution, ICC color, exposure, saturation, and white balance exactly; add a top-left fictional station bug, a centered lower-third subtitle group, and a bottom-right sponsor plate. Center speaker, slash, and dialogue together as one measured group. If the requested reference variant is photo-card, place the photo inside a slightly tilted thick white frame over a dark blurred copy. If it is cast-introduction, add the requested names above the corresponding people with short pink underline strokes.
Station bug: use the provided transparent regional silhouette OR original emblem exactly once, never both; then add station text "<station>" and badge "独播".
Lower-third flourish: shrink the provided handwritten-English transparent wordmark to a subtle semi-transparent background accent at the speaker label's upper-left; do not let it become a large separate headline.
Sponsor: place the supplied regional-food cutout and champagne-gold plaque at bottom right and render "<food name>独家冠名" exactly on one line.
Text (verbatim): speaker "<speaker>"; dialogue "<line>".
Style: clean Chinese reality-show broadcast package, white typography, scene-matched underline, subtle translucent lower-third haze.
Constraints: keep every person’s face, identity, expression, pose, body, clothing, skin tone, scene, objects, resolution, color, and lighting unchanged; add graphics only; exact Chinese text; lossless PNG at native resolution. If the source is not 16:9, preserve it uncropped and unscaled over the smallest suitable 16:9 blurred background fill.
Avoid: real broadcaster logos, map-plus-icon composites, province-level station branding, new people, altered faces, beautification, extra limbs, illegible characters, random English, real sponsor brands.
```
