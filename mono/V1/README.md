# V1 batch calibration

Original Trinet, mono, ~180° fisheye. Reports generation code `v2` (legacy); IMU at ~570 Hz.

| File | Lens | fx (px) | (cx, cy) (px) | Time offset | IMU rate (Hz) |
|---|---|---|---|---|---|
| [`trinet_V1_batch_calibration.json`](trinet_V1_batch_calibration.json) | ~180° fisheye | 591.5 | (931, 525) | -6.34 ms | 571.6 |

Image size 1920x1080 per camera. Format, conventions and tools: see the [top-level README](../../README.md). The principal point (cx, cy) varies from unit to unit; for full accuracy use the unit's own calibration.
