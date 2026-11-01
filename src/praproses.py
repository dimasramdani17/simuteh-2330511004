
"""praproses.py: rangkaian praproses SIMUTEH."""

import os
import json
import cv2
import numpy as np


PARAM_BAWAAN = {
    "lebar": 640,
    "gamma": 1.0,
    "clahe_clip": 2.0,
    "clahe_tile": 8,
    "penapis": "median",
    "kernel": 3,
    "sigma": 1.0,
    "tajam_k": 0.0,
}


def praproses(img_bgr, p=None):
    """
    Urutan:
    ubah ukuran -> gamma -> CLAHE kanal V
    -> redam derau -> penajaman.
    """

    p = {**PARAM_BAWAAN, **(p or {})}

    if img_bgr is None:
        raise ValueError("Citra tidak boleh kosong.")

    # TODO 1: Ubah ukuran citra
    tinggi, lebar = img_bgr.shape[:2]

    lebar_baru = int(p["lebar"])
    tinggi_baru = int(tinggi * lebar_baru / lebar)

    img = cv2.resize(
        img_bgr,
        (lebar_baru, tinggi_baru),
        interpolation=cv2.INTER_AREA
    )

    # TODO 2: Koreksi gamma
    gamma = float(p["gamma"])

    if gamma != 1.0:
        tabel = np.array([
            ((i / 255.0) ** gamma) * 255
            for i in range(256)
        ]).clip(0, 255).astype(np.uint8)

        img = cv2.LUT(img, tabel)

    # TODO 3: CLAHE pada kanal V
    if float(p["clahe_clip"]) > 0:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        clahe = cv2.createCLAHE(
            clipLimit=float(p["clahe_clip"]),
            tileGridSize=(
                int(p["clahe_tile"]),
                int(p["clahe_tile"])
            )
        )

        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])

        img = cv2.cvtColor(
            hsv,
            cv2.COLOR_HSV2BGR
        )

    # TODO 4: Redam derau
    penapis = str(p["penapis"]).lower()
    kernel = int(p["kernel"])

    if kernel < 1 or kernel % 2 == 0:
        raise ValueError("Kernel harus bilangan ganjil positif.")

    if penapis == "none":
        pass

    elif penapis == "rerata":
        img = cv2.blur(img, (kernel, kernel))

    elif penapis == "gaussian":
        img = cv2.GaussianBlur(
            img,
            (kernel, kernel),
            float(p["sigma"])
        )

    elif penapis == "median":
        img = cv2.medianBlur(img, kernel)

    else:
        raise ValueError("Jenis penapis tidak dikenal.")

    # TODO 5: Unsharp masking
    tajam_k = float(p["tajam_k"])

    if tajam_k > 0:
        blur = cv2.GaussianBlur(img, (0, 0), 1.0)

        img = cv2.addWeighted(
            img,
            1.0 + tajam_k,
            blur,
            -tajam_k,
            0
        )

    return img


def simpan_param(p, path="../hasil/param_praproses.json"):
    """Menyimpan parameter praproses ke JSON."""

    parameter = {**PARAM_BAWAAN, **p}

    folder = os.path.dirname(path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(parameter, f, indent=4)

    return parameter
