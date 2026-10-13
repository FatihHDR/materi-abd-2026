# ---
# Pertemuan 5: Exploratory Data Analysis (EDA) dan Visualisasi Interaktif
# Kuliah Analisis Big Data - Semester Ganjil 2026
# ---
#
# Notebook ini adalah panduan praktik untuk Pertemuan 5.
# Jalankan cell-cell di bawah ini secara berurutan.

# %% [markdown]
# # Pertemuan 5: Exploratory Data Analysis (EDA) dan Visualisasi Interaktif
#
# ## Tujuan Pembelajaran
# 1. Memahami prinsip EDA pada data berskala besar: agregasi dan sampling sebelum visualisasi
# 2. Membangun pipeline DuckDB (agregasi) -> Polars (transform) -> Plotly (visualisasi)
# 3. Memahami Grammar of Graphics melalui Altair
# 4. Memilih tipe grafik yang tepat: distribusi, korelasi, komposisi, tren, dan peta
# 5. Mengenali visualisasi yang menyesatkan dan cara memperbaikinya

# %% [markdown]
# ---
# ## Bagian 1: Setup dan Agregasi dengan DuckDB
#
# Kita memakai dataset e-commerce simulasi Indonesia (format serupa Pertemuan 2),
# lalu melakukan agregasi di DuckDB sebelum data dibawa ke Polars dan Plotly.
# Prinsip kunci EDA pada big data: **agregasi/sampling dulu, baru visualisasikan**.

# %%
import duckdb
import numpy as np
import polars as pl
import plotly.express as px
import altair as alt

np.random.seed(2026)
N = 1_000_000

# Koordinat perkiraan (lat, lon) untuk kota-kota yang dipakai sejak Pertemuan 2
kota_koordinat = {
    "Jakarta": (-6.2088, 106.8456),
    "Surabaya": (-7.2575, 112.7521),
    "Bandung": (-6.9175, 107.6191),
    "Medan": (3.5952, 98.6722),
    "Semarang": (-6.9667, 110.4167),
    "Makassar": (-5.1477, 119.4327),
    "Palembang": (-2.9761, 104.7754),
    "Tangerang": (-6.1783, 106.6319),
    "Depok": (-6.4025, 106.7942),
    "Bogor": (-6.5950, 106.8166),
    "Yogyakarta": (-7.7956, 110.3695),
    "Bekasi": (-6.2383, 106.9756),
    "Denpasar": (-8.6705, 115.2126),
    "Balikpapan": (-1.2379, 116.8529),
    "Manado": (1.4748, 124.8421),
}
kota_list = list(kota_koordinat.keys())
kategori_list = ["Elektronik", "Fashion", "Makanan", "Kesehatan", "Olahraga", "Kecantikan", "Otomotif"]
status_list = ["selesai", "dikirim", "proses", "dibatalkan", "dikembalikan"]

df = pl.DataFrame({
    "transaksi_id": [f"TRX{i:08d}" for i in range(N)],
    "tanggal": pl.datetime_range(
        pl.datetime(2024, 1, 1), pl.datetime(2024, 12, 31), interval="1m", eager=True
    ).sample(N, with_replacement=True, seed=2026),
    "kota": np.random.choice(kota_list, N),
    "kategori": np.random.choice(kategori_list, N),
    "harga": np.random.randint(5_000, 10_000_000, N),
    "kuantitas": np.random.randint(1, 20, N),
    "rating": np.round(np.random.uniform(1.0, 5.0, N), 1),
    "status": np.random.choice(status_list, N, p=[0.65, 0.15, 0.10, 0.06, 0.04]),
})
print(f"Dataset: {df.shape[0]:,} baris x {df.shape[1]} kolom")

# %%
# Agregasi di DuckDB: hanya hasil kecil yang dibawa ke tahap berikutnya
con = duckdb.connect()
con.register("transaksi", df)

ringkasan_kota = con.execute("""
    SELECT
        kota,
        COUNT(*) AS jumlah_transaksi,
        SUM(harga * kuantitas) AS total_pendapatan,
        AVG(rating) AS rata_rata_rating
    FROM transaksi
    WHERE status = 'selesai'
    GROUP BY kota
    ORDER BY total_pendapatan DESC
""").pl()
print(ringkasan_kota)

# %% [markdown]
# ---
# ## Bagian 2: Prinsip EDA pada Big Data
#
# Tiga prinsip utama sebelum membuat grafik pada dataset besar:
# 1. **Agregasi dulu** di database (DuckDB/SQL), baru bawa hasil kecil ke tahap visualisasi
# 2. **Sampling** jika perlu scatter plot per baris (jutaan titik akan membebani browser)
# 3. **Profiling ringkas** (describe, null check) untuk memastikan data yang divisualisasikan valid

# %%
# Statistik deskriptif ringkas sebagai langkah awal EDA
print("=== Statistik Deskriptif ===")
print(df.select(["harga", "kuantitas", "rating"]).describe())

# %%
# Sampling untuk scatter plot: jangan render jutaan titik sekaligus
print("\n=== Sampling untuk Visualisasi Titik ===")
sampel = df.sample(n=20_000, seed=2026)
print(f"Dataset asli: {len(df):,} baris -> Sampel untuk scatter plot: {len(sampel):,} baris")

fig_scatter = px.scatter(
    sampel.to_pandas(),
    x="kuantitas",
    y="harga",
    color="kategori",
    opacity=0.5,
    title="Harga vs Kuantitas (Sampel 20.000 baris)",
)
fig_scatter.show()

# %% [markdown]
# ---
# ## Bagian 3: Grammar of Graphics dengan Altair
#
# Altair menerapkan **Grammar of Graphics**: pemetaan deklaratif antara kolom data
# dan elemen visual (posisi, warna, ukuran) — bukan menggambar chart secara manual.

# %%
# Altair bekerja optimal pada data yang sudah diagregasi (ringkas)
chart = (
    alt.Chart(ringkasan_kota.to_pandas())
    .mark_bar()
    .encode(
        x=alt.X("kota:N", sort="-y", title="Kota"),
        y=alt.Y("total_pendapatan:Q", title="Total Pendapatan"),
        color=alt.Color("rata_rata_rating:Q", title="Rata-rata Rating"),
        tooltip=["kota", "jumlah_transaksi", "total_pendapatan", "rata_rata_rating"],
    )
    .properties(title="Total Pendapatan per Kota (Grammar of Graphics)", width=500)
)
chart

# %% [markdown]
# ---
# ## Bagian 4: Distribusi dan Deteksi Outlier
#
# Box plot dan histogram adalah pilihan terbaik untuk melihat sebaran data numerik
# dan mendeteksi pencilan — jauh lebih informatif dibanding pie chart untuk tujuan ini.

# %%
fig_box = px.box(
    sampel.to_pandas(),
    x="kategori",
    y="harga",
    color="kategori",
    title="Distribusi Harga per Kategori (Box Plot)",
    points="outliers",
)
fig_box.show()

fig_hist = px.histogram(
    sampel.to_pandas(),
    x="rating",
    nbins=20,
    title="Distribusi Rating Transaksi (Histogram)",
)
fig_hist.show()

# %% [markdown]
# ---
# ## Kuis Checkpoint 1
#
# 3 soal konseptual EDA dan visualisasi — buka Wayground sekarang.

# %% [markdown]
# ---
# ## Bagian 5: Korelasi Antar Variabel Numerik
#
# Heatmap korelasi membantu mengidentifikasi hubungan linier antarvariabel numerik
# sebelum masuk ke tahap feature engineering atau modeling.

# %%
korelasi = df.select(["harga", "kuantitas", "rating"]).corr()
fig_heatmap = px.imshow(
    korelasi.to_numpy(),
    x=korelasi.columns,
    y=korelasi.columns,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1,
    zmax=1,
    title="Heatmap Korelasi Variabel Numerik",
)
fig_heatmap.show()

# %% [markdown]
# ---
# ## Bagian 6: Komposisi Kategori — Bar Chart vs Pie Chart
#
# Untuk banyak kategori, bar chart lebih mudah dibaca dibanding pie chart
# karena manusia lebih akurat membandingkan panjang batang daripada sudut irisan.

# %%
komposisi_kategori = con.execute("""
    SELECT kategori, COUNT(*) AS jumlah
    FROM transaksi
    GROUP BY kategori
    ORDER BY jumlah DESC
""").pl()

fig_bar = px.bar(
    komposisi_kategori.to_pandas(),
    x="kategori",
    y="jumlah",
    title="Komposisi Transaksi per Kategori (Bar Chart)",
)
fig_bar.show()

# %% [markdown]
# ---
# ## Kuis Checkpoint 2
#
# 3 soal pemilihan chart dan interaktivitas — buka Wayground sekarang.

# %% [markdown]
# ---
# ## Bagian 7: Tren Waktu dengan Line Chart

# %%
tren_bulanan = con.execute("""
    SELECT
        EXTRACT(MONTH FROM tanggal) AS bulan,
        SUM(harga * kuantitas) AS total_pendapatan
    FROM transaksi
    WHERE status = 'selesai'
    GROUP BY 1
    ORDER BY 1
""").pl()

fig_line = px.line(
    tren_bulanan.to_pandas(),
    x="bulan",
    y="total_pendapatan",
    markers=True,
    title="Tren Pendapatan Bulanan",
)
fig_line.show()

# %% [markdown]
# ---
# ## Bagian 8: Peta Interaktif Persebaran Transaksi di Indonesia
#
# `scatter_geo` menampilkan titik lokasi (lat/lon) dengan ukuran/warna
# merepresentasikan nilai agregat — cocok untuk data dengan koordinat kota.

# %%
ringkasan_peta = ringkasan_kota.with_columns([
    pl.col("kota").replace_strict({k: v[0] for k, v in kota_koordinat.items()}).alias("lat"),
    pl.col("kota").replace_strict({k: v[1] for k, v in kota_koordinat.items()}).alias("lon"),
])

fig_map = px.scatter_geo(
    ringkasan_peta.to_pandas(),
    lat="lat",
    lon="lon",
    size="total_pendapatan",
    color="rata_rata_rating",
    hover_name="kota",
    scope="asia",
    title="Persebaran Pendapatan Transaksi per Kota di Indonesia",
)
fig_map.update_geos(center={"lat": -2.5, "lon": 118}, projection_scale=4)
fig_map.show()

# %% [markdown]
# ---
# ## Bagian 9: Visualisasi yang Menyesatkan (Misleading Visualization)
#
# Memotong sumbu Y (truncated axis) dapat membesar-besarkan perbedaan kecil
# sehingga menyesatkan interpretasi pembaca.

# %%
data_demo = komposisi_kategori.to_pandas()

fig_benar = px.bar(data_demo, x="kategori", y="jumlah", title="Benar: Sumbu Y mulai dari 0")
fig_benar.update_yaxes(range=[0, data_demo["jumlah"].max() * 1.1])
fig_benar.show()

fig_menyesatkan = px.bar(data_demo, x="kategori", y="jumlah", title="Menyesatkan: Sumbu Y dipotong")
fig_menyesatkan.update_yaxes(range=[data_demo["jumlah"].min() * 0.95, data_demo["jumlah"].max() * 1.01])
fig_menyesatkan.show()

# %% [markdown]
# ---
# ## Bagian 10: Transformasi untuk Pola Non-linier
#
# Jika scatter plot menunjukkan pola melengkung, transformasi logaritma
# dapat membantu melinearkan hubungan antarvariabel.

# %%
fig_sebelum = px.scatter(
    sampel.to_pandas(), x="harga", y="kuantitas", opacity=0.4,
    title="Sebelum Transformasi: Harga vs Kuantitas",
)
fig_sebelum.show()

sampel_log = sampel.with_columns(pl.col("harga").log10().alias("log_harga"))
fig_sesudah = px.scatter(
    sampel_log.to_pandas(), x="log_harga", y="kuantitas", opacity=0.4,
    title="Sesudah Transformasi Log: Log(Harga) vs Kuantitas",
)
fig_sesudah.show()

# %% [markdown]
# ---
# ## Kuis Checkpoint 3
#
# 4 soal interpretasi visualisasi — buka Wayground sekarang.

# %% [markdown]
# ---
# ## Ringkasan Pertemuan 5
#
# Hari ini kita telah mempelajari:
# 1. Prinsip EDA pada big data: agregasi/sampling dulu, baru visualisasikan
# 2. Pipeline DuckDB (agregasi) -> Polars (transform) -> Plotly/Altair (visualisasi)
# 3. Grammar of Graphics: pemetaan deklaratif data ke elemen visual (Altair)
# 4. Pemilihan chart yang tepat: box plot/histogram (distribusi), heatmap (korelasi),
#    bar chart (komposisi), line chart (tren), scatter geo (peta)
# 5. Mengenali visualisasi menyesatkan (truncated axis) dan transformasi data (log)
#
# ### Milestone 2 Tugas 1 — Check-in Hari Ini
# Implementasi DuckDB SUMMARIZE dan transformasi Polars untuk data cleaning,
# penanganan missing values dan outliers, validasi data dasar.
#
# ### Pertemuan Berikutnya
# Pemrosesan Data Time Series Besar — Resampling, Rolling Windows, dan
# Partitioning data temporal dengan Polars `group_by_dynamic()`
