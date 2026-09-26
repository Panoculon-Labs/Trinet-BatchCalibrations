#!/usr/bin/env python3
"""Undistort a Trinet frame (mono) or rectify a side-by-side stereo frame with
OpenCV's fisheye (equidistant / Kannala-Brandt) model, using a Trinet
calibration JSON.

usage:
  # mono: undistort one image to a pinhole view
  python3 tools/undistort_example.py mono/V4/trinet_pro_mono_V4_batch_calibration.json frame.png out.png

  # stereo: rectify a 3840x1080 side-by-side frame (left half = cam0)
  python3 tools/undistort_example.py stereo-rs/V5/trinet_pro_stereo_V5_batch_calibration.json sbs.png out.png

Options: --balance 0..1 (0 = crop to valid pixels, 1 = keep the full field),
         --fov-scale >1 zooms out (keeps more of the fisheye periphery).

Requires: numpy, opencv-python.
"""
import argparse, json
import numpy as np
import cv2


def K_D(intr):
    K = np.array([[intr["fx"], 0, intr["cx"]], [0, intr["fy"], intr["cy"]], [0, 0, 1]], float)
    return K, np.array(intr["distortion"], float).reshape(4, 1), tuple(intr["image_size"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("calibration")
    ap.add_argument("image")
    ap.add_argument("out")
    ap.add_argument("--balance", type=float, default=0.0)
    ap.add_argument("--fov-scale", type=float, default=1.0)
    a = ap.parse_args()
    d = json.load(open(a.calibration))
    img = cv2.imread(a.image)

    if "cameras" not in d:                                          # mono
        K, D, size = K_D(d["intrinsics"])
        P = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, size, np.eye(3),
                                                                    balance=a.balance, fov_scale=a.fov_scale)
        m1, m2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), P, size, cv2.CV_16SC2)
        cv2.imwrite(a.out, cv2.remap(img, m1, m2, cv2.INTER_LINEAR))
        print("pinhole K after undistortion:\n", P)
        return

    K0, D0, size = K_D(d["cameras"][0]["intrinsics"])               # stereo
    K1, D1, _ = K_D(d["cameras"][1]["intrinsics"])
    T = np.array(d["T_cam1_cam0"], float)
    R, t = T[:3, :3], T[:3, 3]
    w = size[0]
    left, right = img[:, :w], img[:, w:2 * w]                       # cam0 = left half
    R0, R1, P0, P1, Q = cv2.fisheye.stereoRectify(K0, D0, K1, D1, size, R, t, cv2.CALIB_ZERO_DISPARITY,
                                                  size, balance=a.balance, fov_scale=a.fov_scale)
    maps = [cv2.fisheye.initUndistortRectifyMap(K, D, Rr, P, size, cv2.CV_16SC2)
            for K, D, Rr, P in ((K0, D0, R0, P0), (K1, D1, R1, P1))]
    out = np.hstack([cv2.remap(left, *maps[0], cv2.INTER_LINEAR), cv2.remap(right, *maps[1], cv2.INTER_LINEAR)])
    for y in range(0, out.shape[0], 60):                            # epipolar check lines
        cv2.line(out, (0, y), (out.shape[1] - 1, y), (0, 255, 0), 1)
    cv2.imwrite(a.out, out)
    print(f"baseline {np.linalg.norm(t) * 1000:.2f} mm; rectified focal {P0[0, 0]:.1f} px")
    print("Q (disparity -> depth reprojection):\n", Q)


if __name__ == "__main__":
    main()
