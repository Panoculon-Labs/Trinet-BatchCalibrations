# V6 batch calibration

Trinet Pro Stereo GS (global shutter). Same 3840x1080 side-by-side stream as V5: cam0 = left half, cam1 = right half. Generation code `v6`. Applies to the standard 1920x1080-per-eye mode. Not interchangeable with V5.

| File | fx cam0 / cam1 (px) | (cx, cy) cam0 / cam1 (px) | Baseline | Time offset | IMU rate (Hz) |
|---|---|---|---|---|---|
| [`trinet_pro_stereo_gs_V6_batch_calibration.json`](trinet_pro_stereo_gs_V6_batch_calibration.json) | 624.5 / 622.5 | (957, 526) / (986, 552) | 70.38 mm | +3.10 ms | 398.8 |

Image size 1920x1080 per camera. Format, conventions and tools: see the [top-level README](../../README.md). The principal point (cx, cy) and the relative rotation between the eyes vary from unit to unit; for full accuracy use the unit's own calibration.
