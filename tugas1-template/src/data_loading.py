"""Helper pemuatan dan profiling data untuk Tugas 1.

Modul ini dipakai ulang oleh notebook maupun pengujian otomatis (autograding).
Gunakan Polars Lazy API (``scan_*``) agar efisien untuk dataset besar.
"""

from __future__ import annotations

from pathlib import Path

import polars as pl

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def resolve_data_path(*parts: str) -> Path:
    """Bangun path absolut di dalam folder ``data/``."""
    return DATA_DIR.joinpath(*parts)


def scan_dataset(path: str | Path) -> pl.LazyFrame:
    """Pindai dataset (Parquet/CSV) secara lazy tanpa memuatnya ke memori."""
    path = Path(path)
    if path.suffix == ".parquet":
        return pl.scan_parquet(path)
    if path.suffix == ".csv":
        return pl.scan_csv(path)
    raise ValueError(f"Format tidak didukung: {path.suffix}")


def ringkasan_dataframe(df: pl.DataFrame | pl.LazyFrame) -> dict[str, int]:
    """Kembalikan jumlah baris dan kolom (LazyFrame akan di-collect)."""
    if isinstance(df, pl.LazyFrame):
        df = df.collect()
    return {"jumlah_baris": df.height, "jumlah_kolom": df.width}


def hitung_missing(df: pl.DataFrame) -> pl.DataFrame:
    """Ringkasan missing value per kolom (jumlah dan persen)."""
    total = df.height
    return (
        pl.DataFrame(
            {
                "kolom": df.columns,
                "jumlah_null": [df[kolom].null_count() for kolom in df.columns],
            }
        )
        .with_columns((pl.col("jumlah_null") / total * 100).round(2).alias("persen_null"))
        .sort("jumlah_null", descending=True)
    )
