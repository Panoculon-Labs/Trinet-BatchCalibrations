#!/usr/bin/env python3
"""Convert a Trinet calibration JSON (mono or stereo) into the Kalibr YAML pair
used by Kalibr, OpenVINS, VINS-Fusion and Basalt importers:

  <out>/camchain-imucam.yaml   cameras, intrinsics, distortion, T_cam_imu, timeshift
  <out>/imu.yaml               IMU noise model and rate

usage:
  python3 tools/to_kalibr_yaml.py stereo-rs/V5/trinet_pro_stereo_V5_batch_calibration.json out/
  python3 tools/to_kalibr_yaml.py calibration.json out/ --cam-topics /cam0/image_raw /cam1/image_raw --imu-topic /imu0

No dependencies beyond the Python standard library.
"""
import argparse, json, os


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def mat(m, indent):
    pad = " " * indent
    return "\n".join(f"{pad}- [{', '.join(repr(float(x)) for x in row)}]" for row in m)


def cam_block(name, intr, T_cam_imu, ts, topic, T_cn_cnm1=None):
    s = [f"{name}:",
         "  T_cam_imu:", mat(T_cam_imu, 2)]
    if T_cn_cnm1 is not None:
        s += ["  T_cn_cnm1:", mat(T_cn_cnm1, 2)]
    s += ["  camera_model: pinhole",
          "  distortion_model: equidistant",
          f"  distortion_coeffs: [{', '.join(repr(float(x)) for x in intr['distortion'])}]",
          f"  intrinsics: [{intr['fx']!r}, {intr['fy']!r}, {intr['cx']!r}, {intr['cy']!r}]",
          f"  resolution: [{intr['image_size'][0]}, {intr['image_size'][1]}]",
          f"  timeshift_cam_imu: {float(ts)!r}",
          f"  rostopic: {topic}"]
    return "\n".join(s)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("calibration")
    ap.add_argument("out_dir")
    ap.add_argument("--cam-topics", nargs="+", default=["/cam0/image_raw", "/cam1/image_raw"])
    ap.add_argument("--imu-topic", default="/imu0")
    a = ap.parse_args()
    d = json.load(open(a.calibration))
    os.makedirs(a.out_dir, exist_ok=True)

    if "cameras" in d:                                   # stereo
        c0, c1 = d["cameras"]
        T0 = d["T_cam0_imu"]
        T10 = d["T_cam1_cam0"]
        T1 = matmul(T10, T0)
        chain = [cam_block("cam0", c0["intrinsics"], T0, c0["timeshift_cam_imu_s"], a.cam_topics[0]),
                 cam_block("cam1", c1["intrinsics"], T1, c1["timeshift_cam_imu_s"], a.cam_topics[1], T10)]
    else:                                                # mono
        chain = [cam_block("cam0", d["intrinsics"], d["T_cam_imu"], d["timeshift_cam_imu_s"], a.cam_topics[0])]
    open(os.path.join(a.out_dir, "camchain-imucam.yaml"), "w").write("\n".join(chain) + "\n")

    imu = d.get("imu", {})
    lines = ["imu0:",
             f"  accelerometer_noise_density: {imu.get('accel_noise_density')!r}",
             f"  accelerometer_random_walk: {imu.get('accel_random_walk')!r}",
             f"  gyroscope_noise_density: {imu.get('gyro_noise_density')!r}",
             f"  gyroscope_random_walk: {imu.get('gyro_random_walk')!r}",
             f"  update_rate: {float(imu.get('rate_hz', 400.0))!r}",
             f"  rostopic: {a.imu_topic}"]
    open(os.path.join(a.out_dir, "imu.yaml"), "w").write("\n".join(lines) + "\n")
    print(f"wrote {a.out_dir}/camchain-imucam.yaml and {a.out_dir}/imu.yaml")


if __name__ == "__main__":
    main()
