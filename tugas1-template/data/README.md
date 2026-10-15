# Petunjuk Pengunduhan Data

Letakkan **data mentah** hasil unduhan di `data/raw/`. Folder ini tidak
di-commit ke Git — cukup dokumentasikan sumber dan cara mengunduhnya di sini.

## Syarat Dataset

- Ukuran minimal **500 MB** **atau** lebih dari **1 juta baris**.
- Sumber yang diizinkan: **BPS Web API**, **Satu Data Indonesia**,
  **BMKG Data Online**, **HuggingFace Datasets**, atau **Kaggle Indonesia**.
- Format disarankan: **Parquet** (lebih cepat & lebih kecil dari CSV).

## Opsi 1 — Kaggle

```bash
pip install kaggle
# Taruh kredensial di ~/.kaggle/kaggle.json
kaggle datasets download -d <owner>/<slug-dataset> -p data/raw --unzip
```

## Opsi 2 — HuggingFace Datasets

```bash
python -c "from datasets import load_dataset; \
ds = load_dataset('<owner>/<dataset>', split='train'); \
ds.to_parquet('data/raw/dataset.parquet')"
```

## Opsi 3 — BPS Web API

```bash
# Ganti <VAR_ID> dan <TH> sesuai tabel BPS yang dipilih
curl -s "https://webapi.bps.go.id/v1/api/list/model/data/var/<VAR_ID>/th/<TH>/key/<API_KEY>/" \
    -o data/raw/bps.json
```

## Opsi 4 — BMKG Data Online

Unduh data cuaca per stasiun melalui <https://dataonline.bmkg.go.id>, lalu
simpan hasil ekspor ke `data/raw/`.

## Verifikasi Cepat

```bash
python -c "import polars as pl; \
lf = pl.scan_parquet('data/raw/dataset.parquet'); \
print(lf.select(pl.len()).collect())"
```

Setelah data tersedia, lanjutkan ke `notebooks/01_data_profiling.ipynb` dan
catat meta data (nama, sumber, ukuran, periode) di `README.md`.
