# V3 batch calibration

Trinet V3, mono. Shipped with two lenses; pick the file for your lens: the ~150° lens has fx ≈ 870 px, the ~180° lens fx ≈ 590 px. Generation code `v3`.

| File | Lens | fx (px) | (cx, cy) (px) | Time offset | IMU rate (Hz) |
|---|---|---|---|---|---|
| [`trinet_V3_150deg_batch_calibration.json`](trinet_V3_150deg_batch_calibration.json) | ~150° fisheye | 871.4 | (931, 533) | -14.67 ms | n/a |
| [`trinet_V3_180deg_batch_calibration.json`](trinet_V3_180deg_batch_calibration.json) | ~180° fisheye | 589.4 | (966, 540) | -15.82 ms | n/a |

Image size 1920x1080 per camera. Format, conventions and tools: see the [top-level README](../../README.md). The principal point (cx, cy) varies from unit to unit; for full accuracy use the unit's own calibration.
