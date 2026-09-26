# Changelog

## 2026-09-26 — initial release

Batch calibrations for all Trinet hardware versions, one file per version
(two for V3, one per lens):

| Version | File | fx (px) | Baseline | Camera-IMU time offset |
|---|---|---|---|---|
| V1 | `mono/V1/trinet_V1_batch_calibration.json` | 591.5 | n/a | -6.34 ms |
| V2 | `mono/V2/trinet_V2_batch_calibration.json` | 588.3 | n/a | -4.39 ms |
| V3 ~180° | `mono/V3/trinet_V3_180deg_batch_calibration.json` | 589.4 | n/a | -15.82 ms |
| V3 ~150° | `mono/V3/trinet_V3_150deg_batch_calibration.json` | 871.4 | n/a | -14.67 ms |
| V4 | `mono/V4/trinet_pro_mono_V4_batch_calibration.json` | 871.0 | n/a | +6.47 ms |
| V5 | `stereo-rs/V5/trinet_pro_stereo_V5_batch_calibration.json` | 591.2 / 591.1 | 70.05 mm | +3.50 ms |
| V6 | `stereo-gs/V6/trinet_pro_stereo_gs_V6_batch_calibration.json` | 624.5 / 622.5 | 70.38 mm | +3.10 ms |

- V4: same calibration values as the Trinet Pro Mono batch calibration
  delivered on 2026-09-16 (IMU biases, which are per unit, are not part of a
  batch file).
- V5: camera-IMU time offset and lever arm as in the 2026-09-23 rolling-shutter
  calibration revision (3.5 ms, timestamps at the centre image row,
  mid-exposure).
- Tools: `tools/to_kalibr_yaml.py` (Kalibr / OpenVINS YAML export),
  `tools/undistort_example.py` (OpenCV fisheye undistort / stereo rectify).
