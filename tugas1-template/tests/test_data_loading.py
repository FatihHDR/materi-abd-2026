"""Pengujian otomatis untuk script data loading.

Jalankan dengan ``pytest``. Uji ini dipakai oleh autograding GitHub Actions
dan sengaja tidak bergantung pada dataset asli (memakai data kecil di memori).
"""

import polars as pl

from src.data_loading import hitung_missing, ringkasan_dataframe


def test_ringkasan_dataframe():
    df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    assert ringkasan_dataframe(df) == {"jumlah_baris": 3, "jumlah_kolom": 2}


def test_ringkasan_dataframe_dari_lazyframe():
    lf = pl.DataFrame({"a": [1, 2]}).lazy()
    assert ringkasan_dataframe(lf) == {"jumlah_baris": 2, "jumlah_kolom": 1}


def test_hitung_missing_menghitung_null():
    df = pl.DataFrame({"a": [1, None, 3], "b": ["x", "y", "z"]})
    hasil = hitung_missing(df)
    kolom_a = hasil.filter(pl.col("kolom") == "a").row(0, named=True)
    kolom_b = hasil.filter(pl.col("kolom") == "b").row(0, named=True)
    assert kolom_a["jumlah_null"] == 1
    assert kolom_b["jumlah_null"] == 0
