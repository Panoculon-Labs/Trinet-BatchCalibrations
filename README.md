# Trinet Batch Calibrations

Reference camera + IMU calibrations for every Trinet hardware version, one
**batch calibration** per version (and per lens variant where a version shipped
with two lenses). Use the file that matches your device's hardware version.

| Version | Product | Camera | Batch calibration file |
|---|---|---|---|
| **V1** | Trinet | mono, ~180° fisheye | [`mono/V1/trinet_V1_batch_calibration.json`](mono/V1/trinet_V1_batch_calibration.json) |
| **V2** | Trinet | mono, ~180° fisheye | [`mono/V2/trinet_V2_batch_calibration.json`](mono/V2/trinet_V2_batch_calibration.json) |
| **V3** | Trinet | mono, ~180° fisheye | [`mono/V3/trinet_V3_180deg_batch_calibration.json`](mono/V3/trinet_V3_180deg_batch_calibration.json) |
| **V3** | Trinet | mono, ~150° fisheye | [`mono/V3/trinet_V3_150deg_batch_calibration.json`](mono/V3/trinet_V3_150deg_batch_calibration.json) |
| **V4** | Trinet Pro Mono | mono, ~150° fisheye | [`mono/V4/trinet_pro_mono_V4_batch_calibration.json`](mono/V4/trinet_pro_mono_V4_batch_calibration.json) |
| **V5** | Trinet Pro Stereo | stereo, rolling shutter | [`stereo-rs/V5/trinet_pro_stereo_V5_batch_calibration.json`](stereo-rs/V5/trinet_pro_stereo_V5_batch_calibration.json) |
| **V6** | Trinet Pro Stereo GS | stereo, global shutter | [`stereo-gs/V6/trinet_pro_stereo_gs_V6_batch_calibration.json`](stereo-gs/V6/trinet_pro_stereo_gs_V6_batch_calibration.json) |

Calibrations of different versions are **not interchangeable**. In particular,
the camera-IMU time offset differs between versions (it depends on the
hardware and its firmware timestamping), and a V5 and a V6 calibration differ
even though both are 70 mm stereo cameras.

---

## Batch calibration vs. your unit's own calibration

Every Trinet unit also carries **its own factory calibration**, measured on
that unit. The batch calibration is a representative calibration for the
version, not a measurement of your particular unit.

| Use the batch calibration for | Use the unit's own calibration for |
|---|---|
| units without a factory calibration on file | metric stereo depth |
| quick starts, prototyping, simulation, dataset tooling | visual-inertial odometry / SLAM at full accuracy |
| initial values for online calibration refinement | anything needing sub-pixel accuracy |

What is shared across units and what varies:

- **Shared** (the batch value is a good estimate for every unit): focal length
  and lens distortion, the stereo baseline, the camera-IMU rotation and lever
  arm, the camera-IMU time offset, the rolling-shutter readout time.
- **Varies per unit**: the **principal point** (cx, cy), which is set by how
  each lens is centred on its sensor, and, for stereo, the small **relative
  rotation between the two eyes**. Typical unit-to-unit spread:

| Version | Focal length (1 SD) | Principal point (1 SD) | Stereo relative rotation (median / 95th pct) | Baseline (1 SD) |
|---|---|---|---|---|
| V3 (~180°) | ±3 px | ±10–17 px | n/a | n/a |
| V5 | ±2 px | ±30–40 px | 0.45° / 1.2° | ±0.4 mm |
| V6 | ±4 px | ±30–65 px | 0.7° / 1.6° | ±0.8 mm |

For stereo, a relative rotation of 0.1° shifts the image by about 1 px, so the
batch calibration is **not** a substitute for the unit's own calibration when
you compute metric depth; rectify with the unit's calibration, or refine the
relative rotation online (see [Refining online](#refining-online)).

### Getting your unit's own calibration

- **Trinet SDK:** read it from a connected device (`getCalibration`), or from
  any recording: SDK recordings embed the unit's stored calibration in the MP4
  (`moov/udta`), so a clip is usable for undistortion even when separated from
  its folder.
- **Per-unit files:** where we hold your units' calibrations as files, they
  use the same JSON format as this repository, keyed by device ID.

---

## Which version do I have?

| Version | How to recognise it |
|---|---|
| V1, V2 | Mono. The device reports generation code `v2` (legacy). IMU at ~560-570 Hz. V2 is the second housing of the original Trinet; its optical centre sits lower in the image (cy ≈ 630 px vs ≈ 525 px). |
| V3 | Mono. Generation code `v3`. Live magnetometer, 400 Hz IMU. Shipped with a ~180° or a ~150° lens: the ~150° lens has a much longer focal length (fx ≈ 870 px vs ≈ 590 px). |
| V4 | Trinet Pro Mono. Generation code `v4`. Embedded audio, 400 Hz IMU, ~150° lens. |
| V5 | Trinet Pro Stereo. Generation code `v5`. One 3840x1080 side-by-side stream (two 1920x1080 eyes), rolling shutter. |
| V6 | Trinet Pro Stereo GS. Generation code `v6`. Same 3840x1080 side-by-side stream as V5, but global shutter: the per-frame timing metadata reports a readout time of zero. |

The generation code is available from the Trinet SDK (`getGeneration()`;
`null` means `v2`). The stream shape is the most robust signal for stereo: a
unit that streams 3840x1080 side-by-side is a V5 or V6 even if it reports an
older code, and the per-frame timing metadata tells V5 (rolling) from V6
(global).

---

## File format

All files are JSON. Units: **pixels** for intrinsics, **metres** for
translations, **seconds** for time offsets. Every file repeats its conventions
in a `conventions` block.

### Mono (`format: trinet-mono-calibration/1`)

```jsonc
{
  "format": "trinet-mono-calibration/1",
  "hardware": "Trinet Pro Mono",
  "hardware_version": "V4",
  "calibration_type": "batch",
  "lens": "~150° fisheye",
  "shutter": "rolling",
  "calibration_date": "2026-09-26",
  "conventions": { ... },
  "intrinsics": {
    "image_size": [1920, 1080],
    "model": "equidistant",
    "fx": 871.03, "fy": 872.44, "cx": 965.76, "cy": 551.46,
    "distortion": [k1, k2, k3, k4]
  },
  "T_cam_imu": [[...4x4...]],
  "timeshift_cam_imu_s": 0.00647,
  "imu": { "rate_hz": 400.25, "gyro_noise_density": ..., "gyro_random_walk": ...,
           "accel_noise_density": ..., "accel_random_walk": ... }
}
```

### Stereo (`format: trinet-stereo-calibration/1`)

```jsonc
{
  "format": "trinet-stereo-calibration/1",
  "hardware": "Trinet Pro Stereo",
  "hardware_version": "V5",
  "calibration_type": "batch",
  "shutter": "rolling",
  "cameras": [
    { "intrinsics": { ...cam0, as mono... }, "timeshift_cam_imu_s": 0.0035 },
    { "intrinsics": { ...cam1... },          "timeshift_cam_imu_s": 0.0035 }
  ],
  "T_cam1_cam0": [[...4x4...]],
  "T_cam0_imu":  [[...4x4...]],
  "imu": { ... },
  "rolling_shutter": {                      // V5 only
    "readout_time_s": 0.0318,
    "line_delay_s": 2.94e-05,
    "timestamp_reference": "centre image row, mid-exposure"
  }
}
```

V6 (global shutter) has no `rolling_shutter` block; its `timestamp_reference`
is `mid-exposure`.

### Conventions

- **Camera model:** pinhole projection + **equidistant (Kannala-Brandt) fisheye
  distortion**, `distortion = [k1, k2, k3, k4]`. This is OpenCV's `cv2.fisheye`
  model and Kalibr's `pinhole-equi`.
- **Camera frame:** x right, y down, z forward (along the optical axis).
- **`T_cam_imu` / `T_cam0_imu`:** 4x4 homogeneous transform that maps a point
  from the IMU frame into the camera frame: `p_cam = T_cam_imu · p_imu`. The
  translation column is the IMU origin expressed in the camera frame.
- **`T_cam1_cam0`:** maps a point from the cam0 frame into the cam1 frame:
  `p_cam1 = T_cam1_cam0 · p_cam0`. Its translation is ≈ (-0.070, 0, 0) m: cam1
  sits 70 mm to the right of cam0.
- **Stereo eyes:** **cam0 = scene-left eye = left half** of the side-by-side
  frame (x = 0...1919); **cam1 = scene-right eye = right half** (x = 1920...3839).
- **Time offset:** `t_imu = t_cam + timeshift_cam_imu_s`. To express a camera
  timestamp on the IMU clock, add the timeshift. This is the same sign
  convention as Kalibr's `timeshift_cam_imu`.
- **Frame timestamps:** V5 frame timestamps refer to the **centre image row at
  mid-exposure**; row `r` of a V5 frame was exposed at
  `t_frame + (r - 540) · line_delay_s`. V6 frames (global shutter) expose all
  rows together; timestamps refer to mid-exposure.
- **IMU noise model:** continuous-time noise densities and random walks
  (Kalibr / OpenVINS convention): gyro in rad/s/√Hz and rad/s²/√Hz, accel in
  m/s²/√Hz and m/s³/√Hz. These are conservative defaults suited to VIO.

### Resolution

All calibrations are for **1920x1080 per camera** (for stereo: per eye of the
3840x1080 side-by-side stream). If you scale images, scale `fx, fy, cx, cy`
by the same factor (distortion coefficients are unchanged). V6 units also
support an optional 1920x1200 per-eye mode; these calibrations apply to the
standard 1920x1080 mode only.

---

## Tools

Python 3; `undistort_example.py` needs `numpy` and `opencv-python`.

**Export to Kalibr / OpenVINS / VINS-Fusion / Basalt YAML**

```bash
python3 tools/to_kalibr_yaml.py stereo-rs/V5/trinet_pro_stereo_V5_batch_calibration.json out/
# -> out/camchain-imucam.yaml  out/imu.yaml
python3 tools/to_kalibr_yaml.py mono/V4/trinet_pro_mono_V4_batch_calibration.json out/ \
    --cam-topics /cam0/image_raw --imu-topic /imu0
```

**Undistort (mono) or rectify (stereo) with OpenCV**

```bash
python3 tools/undistort_example.py mono/V4/trinet_pro_mono_V4_batch_calibration.json frame.png undistorted.png
python3 tools/undistort_example.py stereo-gs/V6/trinet_pro_stereo_gs_V6_batch_calibration.json sbs.png rectified.png
```

The stereo example splits the side-by-side frame, rectifies both eyes with
`cv2.fisheye.stereoRectify`, draws horizontal epipolar check lines and prints
the `Q` matrix for disparity-to-depth reprojection.

---

## Refining online

The quantities that vary per unit are cheap to refine at run time:

- **Stereo relative rotation:** pitch and roll between the eyes are observable
  from the vertical disparity of matched features in any scene; yaw from
  distant features, or from a VIO with online camera-IMU extrinsic refinement
  (e.g. OpenVINS, Basalt). Keep intrinsics and baseline fixed.
- **Principal point:** refine together with the camera-IMU extrinsics in your
  VIO, or use the unit's own calibration.

---

## Versioning

Files are updated in place when a version's calibration is revised; every
revision is recorded in [`CHANGELOG.md`](CHANGELOG.md) and tagged in git.
The `calibration_date` field of each file gives the date of its current
revision. To pin a revision, use the git tag.
