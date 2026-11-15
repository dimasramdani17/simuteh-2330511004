# 🍃 SIMUTEH
### Sistem Pemeriksaan Mutu Daun Teh Berbasis Citra

<p align="center">
  <strong>Computer Vision Project | SIMUTEH v0.3</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv" />
  <img src="https://img.shields.io/badge/Version-0.3-orange" />
  <img src="https://img.shields.io/badge/Dataset-60%20Images-purple" />
</p>

---

## 👨‍🎓 Identitas Pengembang

| Informasi | Keterangan |
|---|---|
| **Nama** | Dimas Ramdani |
| **NIM** | 2330511004 |
| **Kelas** | 7A |
| **Mata Kuliah** | Computer Vision |
| **SEED Dataset** | 1004 |
| **Program** | Teknik Informatika |

**Repository:** [github.com/dimasramdani17/simuteh-2330511004](https://github.com/dimasramdani17/simuteh-2330511004)

---

## 📌 1. Deskripsi Proyek

**SIMUTEH (Sistem Pemeriksaan Mutu Daun Teh)** merupakan sistem berbasis *Computer Vision* yang dirancang untuk membantu kelompok tani teh rakyat di Kabupaten Sukabumi dalam proses pemeriksaan dan pemilahan mutu daun teh.

Sistem ini berfokus pada deteksi penyakit cacar daun teh (*Blister Blight*), yang ditandai dengan bercak berwarna kuning pucat dengan bagian tepi kecokelatan.

SIMUTEH menggunakan citra daun teh yang diambil di atas nampan sebagai masukan (*input*). Selanjutnya, sistem melakukan pengolahan citra untuk menghasilkan informasi berupa:

- Persentase luas area bercak pada daun.
- Jumlah bercak yang terdeteksi.
- Klasifikasi mutu daun teh.

### 🎯 Kategori Klasifikasi

| Kategori | Keterangan |
|---|---|
| 🟢 **Sehat** | Daun tanpa bercak yang terdeteksi. |
| 🟡 **Bercak Ringan** | Daun dengan tingkat serangan bercak ringan. |
| 🔴 **Bercak Berat** | Daun dengan tingkat serangan bercak berat. |

> **Catatan:** SIMUTEH merupakan alat bantu pemeriksaan mutu daun teh. Keputusan akhir proses penyortiran tetap berada di tangan petugas sortir.

---

## 📂 2. Struktur Repository

Berikut merupakan struktur direktori proyek SIMUTEH:

```text
simuteh-2330511004/
│
├── data/
│   └── sintetis/               # Dataset citra sintetis
│       ├── citra/
│       ├── bersih/
│       ├── mask_daun/
│       ├── mask_bercak/
│       └── label.csv
│
├── hasil/                      # Hasil evaluasi dan pengolahan
│   ├── param_praproses.json
│   ├── param_bercak.json
│   └── p5_*.csv, p6_*.csv
│
├── notebook/                   # Notebook praktikum
│   ├── B1..B5_*.ipynb
│   ├── P5_tepi.ipynb
│   └── P6_morfologi.ipynb
│
├── src/                        # Modul program utama
│   ├── praproses.py
│   ├── utils_tepi.py
│   └── bercak.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ 3. Alur Pemrosesan (Processing Pipeline)

SIMUTEH menerapkan beberapa tahapan pengolahan citra untuk memperoleh hasil deteksi bercak yang optimal.

### 3.1 Akuisisi dan Praproses Citra (P1–P4)

Tahapan ini bertujuan meningkatkan kualitas citra sebelum dilakukan proses deteksi.

| Metode | Fungsi |
|---|---|
| Gamma Correction | Koreksi pencahayaan otomatis (0.6 untuk kondisi gelap dan 1.6 untuk kondisi terang). |
| CLAHE | Meningkatkan kontras lokal pada kanal V ketika pencahayaan tidak merata. |
| Median Filter 3×3 | Meredam derau pada citra tanpa melakukan penajaman. |
| Kanal R (Red) | Menjadi fokus analisis karena menghasilkan Kontras Bercak (KB) tertinggi. |

### 3.2 Deteksi Tepi (P5)

Tahapan deteksi tepi digunakan untuk mengidentifikasi batas area bercak pada daun teh.

Metode yang dievaluasi:
- Sobel
- Prewitt
- Laplacian of Gaussian (LoG)
- Canny

**Hasil utama:**

Operator Canny pada kanal R menunjukkan performa terbaik dengan nilai F1 > 0.97 dan mampu mengurangi *false positive*, termasuk deteksi pada tulang daun.

### 3.3 Morfologi dan Connected Components (P6)

Tahapan ini bertujuan memperbaiki hasil segmentasi dan mengidentifikasi komponen bercak.

| Metode | Fungsi |
|---|---|
| Opening | Menghilangkan derau dan potongan tulang daun menggunakan SE Elips 5×5. |
| Closing | Menutup lubang pada area bercak. |
| Connected Components | Mengidentifikasi komponen bercak menggunakan konektivitas 8. |

**Parameter penyaringan komponen:**

- Luas area ≥ 20 piksel.
- Kebulatan ≥ 0.5.
- Rasio aspek ≤ 1.8.

Hasil identifikasi komponen kemudian digunakan untuk menghitung persentase luas bercak dan menentukan kategori mutu daun teh.

---

## 🚀 4. Instalasi dan Penggunaan

### 4.1 Persiapan Lingkungan

Pastikan Python sudah terinstal. Selanjutnya, unduh repository:

```bash
git clone https://github.com/dimasramdani17/simuteh-2330511004.git
```

Masuk ke direktori proyek:

```bash
cd simuteh-2330511004
```

Instal seluruh dependensi:

```bash
pip install -r requirements.txt
```

Dependensi utama yang digunakan:

- OpenCV
- NumPy
- Pandas
- Matplotlib

### 4.2 Penggunaan Modul Praproses Citra

Modul `praproses.py` digunakan untuk melakukan koreksi dan peningkatan kualitas citra berdasarkan parameter hasil evaluasi P1–P4.

```python
import cv2
import json
import sys

sys.path.append("src")

from praproses import praproses

# Memuat parameter hasil P1-P4
with open("hasil/param_praproses.json") as f:
    PARAM = json.load(f)

# Membaca citra mentah
img_mentah = cv2.imread(
    "data/sintetis/citra/teh_041.png"
)

# Melakukan praproses
img_praproses = praproses(img_mentah, PARAM)
```

### 4.3 Analisis Mutu Daun Teh

Modul `bercak.py` digunakan untuk melakukan analisis bercak dan menentukan kategori mutu daun.

```python
import sys

sys.path.append("src")

import bercak

# Parameter analisis
PB = {}

# Menjalankan analisis daun
hasil = bercak.analisis_daun(img_praproses, PB)

# Menampilkan hasil
print(f"Jumlah Bercak : {hasil['jumlah_bercak']}")
print(f"Persen Bercak : {hasil['persen_bercak']}%")
print(f"Kelas Mutu    : {hasil['kelas']}")
```

---

## 📊 5. Hasil Evaluasi

Berdasarkan pengujian terhadap **60 citra dataset sintetis**, modul `bercak.py` pada SIMUTEH v0.3 memperoleh hasil evaluasi sebagai berikut.

### Ringkasan Performa

| Parameter Evaluasi | Hasil |
|---|---:|
| Jumlah Dataset | 60 citra |
| Galat Absolut Rerata Persen Bercak | **0.396%** |
| Korelasi | **0.944** |
| Akurasi Klasifikasi | **93.3%** |
| Jumlah Klasifikasi Benar | **56 dari 60 citra** |

### 🔍 Temuan Utama

1. **Kanal R (Red)** terbukti efektif dalam memisahkan karakteristik bercak dari area daun berdasarkan hasil analisis kontras.
2. **Opening Morfologi** berhasil mengurangi komponen derau dari ratusan menjadi hanya 3 komponen riil pada pengujian citra `teh_021`.
3. Kombinasi deteksi tepi, operasi morfologi, dan Connected Components membantu proses identifikasi area bercak.

---

## ⚠️ 6. Keterbatasan Sistem

Meskipun memperoleh hasil evaluasi yang baik pada dataset sintetis, SIMUTEH masih memiliki beberapa keterbatasan.

### 6.1 Bentuk Bercak Sintetis

Dataset sintetis saat ini memiliki karakteristik bercak berbentuk lingkaran sempurna. Kondisi tersebut belum sepenuhnya merepresentasikan bentuk bercak pada daun teh nyata yang dapat memiliki bentuk tidak beraturan atau memanjang.

### 6.2 Parameter Rasio Aspek

Penggunaan aturan `rasio_maks = 1.8` berpotensi terlalu ketat untuk menyaring bercak nyata yang memiliki bentuk memanjang.

### 6.3 Evaluasi Batas Klasifikasi

Batas kelas persentase bercak masih dievaluasi menggunakan seluruh dataset. Kondisi ini berpotensi menimbulkan *data leakage* sehingga perlu diperbaiki pada pengembangan berikutnya.

---

## 🔬 7. Rencana Pengembangan (P7)

Pengembangan selanjutnya difokuskan pada peningkatan kemampuan segmentasi bercak, khususnya untuk menangani citra dengan kontras rendah dan bercak yang saling menyatu.

Metode yang direncanakan:

| Metode | Tujuan |
|---|---|
| Otsu Thresholding | Menentukan ambang segmentasi secara otomatis. |
| Watershed | Memisahkan area bercak yang saling menyatu. |
| K-Means Clustering | Mengelompokkan piksel berdasarkan karakteristik warnanya. |
| Distance Transform | Membantu memisahkan komponen bercak yang saling berdekatan atau menyatu. |

Pengujian juga akan difokuskan pada citra dengan kondisi kontras rendah, khususnya `teh_044`.

---

## 📌 8. Kesimpulan

SIMUTEH merupakan implementasi sistem *Computer Vision* untuk membantu pemeriksaan mutu daun teh melalui analisis citra digital.

Berdasarkan hasil pengujian pada 60 citra sintetis, sistem memperoleh akurasi klasifikasi sebesar **93.3%** dengan galat absolut rerata persentase bercak sebesar **0.396%**.

Hasil tersebut menunjukkan bahwa pendekatan pengolahan citra menggunakan koreksi pencahayaan, peningkatan kontras, deteksi tepi, operasi morfologi, dan Connected Components memiliki potensi untuk diterapkan dalam proses identifikasi bercak daun teh.

Pengembangan berikutnya akan diarahkan pada peningkatan kemampuan segmentasi agar sistem lebih adaptif terhadap variasi bentuk bercak dan kondisi pencahayaan pada citra daun teh.

---

<p align="center">
  <strong>🍃 SIMUTEH — Sistem Pemeriksaan Mutu Daun Teh Berbasis Citra</strong>
  <br/>
  <sub>Computer Vision | Teknik Informatika | 2026</sub>
  <br/>
  <sub>Developed by Dimas Ramdani</sub>
</p>
