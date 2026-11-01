
"""praproses.py: rangkaian praproses SIMUTEH."""

import json
import os
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
    """Urutan: resize -> gamma -> CLAHE V -> filter -> sharpening."""

    p = {**PARAM_BAWAAN, **(p or {})}

    # TODO 1: Ubah ukuran dengan rasio aspek tetap
    tinggi, lebar = img_bgr.shape[:2]
    skala = p["lebar"] / lebar
    tinggi_baru = int(tinggi * skala)

    img = cv2.resize(
        img_bgr,
        (p["lebar"], tinggi_baru),
        interpolation=cv2.INTER_AREA
    )

    # TODO 2: Koreksi gamma
    if p["gamma"] != 1.0:
        gamma = p["gamma"]
        tabel = np.array([
            ((i / 255.0) ** (1.0 / gamma)) * 255
            for i in range(256)
        ]).astype("uint8")

        img = cv2.LUT(img, tabel)

    # TODO 3: CLAHE pada kanal V
    if p["clahe_clip"] > 0:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        clahe = cv2.createCLAHE(
            clipLimit=p["clahe_clip"],
            tileGridSize=(p["clahe_tile"], p["clahe_tile"])
        )

        v = clahe.apply(v)
        img = cv2.cvtColor(
            cv2.merge([h, s, v]),
            cv2.COLOR_HSV2BGR
        )

    # TODO 4: Redam derau
    jenis = p["penapis"]
    k = p["kernel"]

    if jenis == "rerata":
        img = cv2.blur(img, (k, k))

    elif jenis == "gaussian":
        img = cv2.GaussianBlur(
            img, (k, k), p["sigma"]
        )

    elif jenis == "median":
        img = cv2.medianBlur(img, k)

    elif jenis != "none":
        raise ValueError("Jenis penapis tidak dikenal")

    # TODO 5: Unsharp masking
    if p["tajam_k"] > 0:
        blur = cv2.GaussianBlur(img, (0, 0), 1.0)
        img = cv2.addWeighted(
            img, 1.0 + p["tajam_k"],
            blur, -p["tajam_k"], 0
        )

    return img


def simpan_param(p, path="../hasil/param_praproses.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(
            {**PARAM_BAWAAN, **p},
            f,
            indent=2
        )
