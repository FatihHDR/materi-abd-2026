# Tugas 1 — Eksplorasi dan Analisis Dataset Besar Indonesia

Template repositori **Tugas 1 (Individual)** untuk mata kuliah *Analisis Big Data*.
Repositori ini adalah *starter* untuk GitHub Classroom — ganti semua penanda
HTML comment (`<!-- ... -->`) dengan pekerjaanmu.

> **Bobot:** 25% dari nilai akhir · **Tipe:** Individual · **Diumumkan:** Pertemuan 2

## Identitas

| Item            | Isi                        |
| --------------- | -------------------------- |
| Nama            | <!-- Nama Lengkap -->      |
| NIM             | <!-- NIM -->               |
| GitHub Username | <!-- username-github -->   |
| Judul Analisis  | <!-- judul analisis -->    |

## Ringkasan Dataset

| Item         | Isi                                                    |
| ------------ | ------------------------------------------------------ |
| Nama Dataset | <!-- contoh: Transaksi E-Commerce Indonesia -->        |
| Sumber       | <!-- BPS / Satu Data Indonesia / BMKG / HuggingFace / Kaggle --> |
| Ukuran       | <!-- contoh: 1.2 juta baris / 640 MB -->               |
| Periode      | <!-- contoh: Januari–Desember 2024 -->                 |

Petunjuk pengunduhan lengkap ada di [`data/README.md`](data/README.md).
Data mentah **tidak** di-commit ke Git (lihat `.gitignore`).

## Cara Menjalankan

### 1. Docker (disarankan — environment identik dengan kuliah)

```bash
# Build image
docker build -t tugas1 .

# Jalankan JupyterLab
docker run --rm -p 8888:8888 -v "$PWD":/home/jovyan/work tugas1
```

Buka <http://localhost:8888/lab> lalu jalankan notebook secara berurutan.

### 2. Lokal (virtualenv)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

## Struktur Repositori

```text
tugas1-[username_github]/
├── .github/
│   └── workflows/
│       └── lint_check.yml      # Autograding: format, lint, uji data loading
├── README.md                   # Laporan utama + AI Disclosure
├── Dockerfile                  # Reproduktivitas environment
├── requirements.txt            # Dependensi Python
├── pyproject.toml              # Konfigurasi ruff + pytest
├── notebooks/
│   ├── 01_data_profiling.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_eda_and_insights.ipynb
├── src/                        # Helper script / modul Polars
├── tests/                      # Pengujian otomatis (autograding)
├── data/
│   └── README.md               # Petunjuk pengunduhan data
└── output/
    └── figures/                # Visualisasi ter-export
```

## Alur Milestone

| Milestone           | Diberikan | Deadline       | Deliverable                                                                 |
| ------------------- | --------- | -------------- | --------------------------------------------------------------------------- |
| Milestone 1         | P2        | P3             | Setup repo + `data/README.md` + notebook profiling awal (>500 MB / >1 juta) |
| Milestone 2         | P4        | P5             | `DuckDB SUMMARIZE` + cleaning Polars (missing, outlier, validasi dasar)      |
| Milestone 3         | P6        | P8             | Analisis temporal + minimal 6 visualisasi interaktif Plotly/Altair          |
| Final Submission    | P8        | P10            | 5+ insight, `Dockerfile`, README final, AI Disclosure                      |

## Tools Wajib

- **Polars** untuk manipulasi data (bukan Pandas).
- **DuckDB** untuk SQL analytics.
- **Plotly** atau **Altair** untuk visualisasi interaktif.
- **JupyterLab** sebagai environment kerja.

## Checklist Sebelum Submit

- [ ] Dataset >500 MB atau >1 juta baris, sumber terdokumentasi di `data/README.md`.
- [ ] Semua pemrosesan utama memakai Polars (Lazy API) dan/atau DuckDB.
- [ ] Minimal 6 visualisasi interaktif tersimpan di `output/figures/`.
- [ ] 5+ insight analitik ditulis di `README.md` / notebook akhir.
- [ ] `docker build` berhasil tanpa error.
- [ ] Autograding (format, lint, test) lulus — cek tab **Actions**.
- [ ] AI Disclosure diisi jujur.

## AI Disclosure

Wajib diisi. Tuliskan penggunaan AI asisten secara transparan.

| Tool AI        | Bagian yang dibantu       | Ringkasan prompt | Sudah diverifikasi? |
| -------------- | ------------------------- | ---------------- | ------------------- |
| <!-- mis. ChatGPT --> | <!-- mis. cleaning --> | <!-- ... --> | <!-- Ya/Tidak --> |

> Menyalin pekerjaan orang lain atau menyembunyikan penggunaan AI adalah
> pelanggaran integritas akademik.

## Insight Utama

<!-- Tuliskan 5+ insight analitik di sini setelah analisis selesai. -->
