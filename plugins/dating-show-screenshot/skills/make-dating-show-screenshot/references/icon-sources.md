# Graphic source notes

- Emblems in `assets/station-icons/` and wordmarks in `assets/flourishes/` are original image-generation outputs. Open icon libraries and uploaded screenshots were used only to study general broadcast-layout conventions; no real broadcaster logo or screenshot crop is bundled.
- Material Symbols reference: <https://developers.google.com/fonts/docs/material_symbols>. Google publishes the family under Apache License 2.0.
- Material Design Icons repository: <https://github.com/google/material-design-icons>. The repository is Apache-2.0 licensed.
- Map geometry source: `china-map-geojson@1.0.4`, ISC license, <https://www.npmjs.com/package/china-map-geojson>. The generated PNG silhouettes are derived from the selected city/prefecture features.
- The bundled Simplified Chinese font subsets come from `@fontsource/noto-sans-sc@5.3.0` and `@fontsource/noto-serif-sc@5.3.0`. Both are distributed under SIL Open Font License 1.1; the license is in `assets/fonts/OFL.txt`.
- Sponsor product lockups in `assets/sponsors/` are original image-generation outputs or programmatically drawn fictional products. They contain no real brand, real packaging text, or copied television artwork.
- Never pass a real broadcaster logo into image generation unless the user supplied it and explicitly asked to retain it. Default presets must remain fictional and must use one regional silhouette or one original emblem, never both.
