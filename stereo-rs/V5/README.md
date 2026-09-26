# V5 batch calibration

Trinet Pro Stereo (rolling shutter). One 3840x1080 side-by-side stream: cam0 = left half, cam1 = right half. Generation code `v5`. Frame timestamps refer to the centre image row at mid-exposure; see `rolling_shutter` in the file for the per-row timing.

| File | fx cam0 / cam1 (px) | (cx, cy) cam0 / cam1 (px) | Baseline | Time offset | IMU rate (Hz) |
|---|---|---|---|---|---|
| [`trinet_pro_stereo_V5_batch_calibration.json`](trinet_pro_stereo_V5_batch_calibration.json) | 591.2 / 591.1 | (913, 567) / (938, 574) | 70.05 mm | +3.50 ms | 400.2 |

Image size 1920x1080 per camera. Format, conventions and tools: see the [top-level README](../../README.md). The principal point (cx, cy) and the relative rotation between the eyes vary from unit to unit; for full accuracy use the unit's own calibration.
