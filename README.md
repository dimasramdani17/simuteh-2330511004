# Proyek Praktikum Computer Vision – SIMUTEH

## 1. Deskripsi Proyek

Proyek ini merupakan implementasi praktikum Computer Vision menggunakan dataset sintetis daun teh SIMUTEH. Praktikum berfokus pada pengolahan citra digital, mulai dari pembacaan citra, analisis warna, histogram, peningkatan kualitas citra, hingga konvolusi dan penapisan spasial.

Dataset terdiri dari tiga kategori kondisi daun, yaitu:
- Sehat
- Bercak ringan
- Bercak berat

## 2. Struktur Folder

```text
simuteh-1004/
│
├── data/
│   └── sintetis/
│       ├── citra/
│       ├── bersih/
│       ├── mask_daun/
│       ├── mask_bercak/
│       └── label.csv
│
├── src/
│   ├── buat_dataset_sintetis.py
│   └── utils_cv.py
│
├── notebook/
│   ├── B1_lingkungan.ipynb
│   ├── B2_citra_warna.ipynb
│   ├── B3_histogram.ipynb
│   ├── B4_penapisan.ipynb
│   └── B5_praproses.ipynb
│
├── hasil/
│
├── laporan/
│
├── requirements.txt
└── README.md
```

## 3. Kebutuhan Sistem

Perangkat dan perangkat lunak yang digunakan:
- Python 3
- Google Colab atau Jupyter Notebook
- Google Drive
- OpenCV
- NumPy
- Pandas
- Matplotlib

## 4. Instalasi Library

Jalankan perintah berikut pada Google Colab atau terminal Python:

```bash
pip install numpy pandas matplotlib opencv-python
```

## 5. Persiapan Dataset

Dataset sintetis dibuat menggunakan file `buat_dataset_sintetis.py`.

Nilai seed yang digunakan adalah:

```python
SEED = 1004
```

Seed digunakan agar proses pembentukan dataset dapat menghasilkan data yang konsisten ketika dijalankan kembali dengan konfigurasi yang sama.

Dataset disimpan pada folder:

```text
data/sintetis/
```

Folder tersebut berisi citra, citra bersih, mask daun, mask bercak, dan file label.

## 6. Cara Menjalankan Program

1. Buka Google Colab.
2. Upload notebook ke Google Colab atau buka notebook melalui Google Drive.
3. Hubungkan Google Drive ke Google Colab.
4. Pastikan folder proyek berada di lokasi yang sesuai.
5. Sesuaikan path direktori apabila diperlukan.
6. Jalankan setiap notebook secara berurutan.

Urutan pengerjaan praktikum:

| Notebook | Materi |
|---|---|
| B1 | Lingkungan dan pengenalan citra |
| B2 | Citra warna dan sampling |
| B3 | Histogram dan peningkatan kualitas citra |
| B4 | Konvolusi dan penapisan spasial |
| B5 | Pipeline praproses citra |

## 7. Pengujian B4 – Konvolusi dan Penapisan Spasial

Pengujian B4 dilakukan untuk membandingkan beberapa metode penapisan citra dalam mengurangi derau.

Jenis penapis yang digunakan:
- Mean Filter 3×3
- Mean Filter 5×5
- Gaussian Filter 5×5
- Median Filter 3×3
- Median Filter 5×5
- Median Filter 9×9

Jenis derau yang diuji:
- Gaussian dengan standar deviasi 10
- Gaussian dengan standar deviasi 20
- Gaussian dengan standar deviasi 40
- Salt and Pepper 4%
- Salt and Pepper 10%

Parameter evaluasi:
- **PSNR:** mengukur kualitas citra hasil penapisan dibandingkan citra bersih.
- **Waktu pemrosesan:** mengukur waktu yang dibutuhkan setiap penapis.
- **KB (Kontras Bercak):** mengukur perbedaan intensitas bercak terhadap area daun yang tidak bercak.

Selain itu, dilakukan pengujian ukuran median filter serta pengamatan bercak terkecil pada citra `teh_021` dengan ukuran filter 3×3, 5×5, 9×9, dan 15×15.

## 8. Hasil Pengujian

Hasil pengujian disimpan pada folder `hasil/`.

Beberapa keluaran B4 meliputi:
- `b4_tabel_penapis.csv`
- `b4_diagram_psnr.png`
- `b4_diagram_waktu.png`
- `b4_diagram_kb.png`
- `b4_pengujian_ukuran_median.csv`
- `b4_pengujian_multi_citra.csv`
- Folder `bercak_terkecil_teh_021/`

File tersebut berisi tabel, diagram batang, dan citra hasil pengujian.

## 9. Catatan

- Pastikan dataset tersedia sebelum menjalankan notebook.
- Jalankan notebook sesuai urutan praktikum.
- Periksa kembali path penyimpanan apabila menggunakan direktori yang berbeda.
- Dataset tidak disertakan dalam ZIP kode apabila pengumpulan tugas meminta kode saja.
- Hasil pengujian dapat disimpan pada folder `hasil/` sebagai bahan penyusunan laporan.

---

**Proyek Praktikum Computer Vision – SIMUTEH**  
**Seed Dataset: 1004**
