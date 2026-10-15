FROM quay.io/jupyter/datascience-notebook:latest

LABEL maintainer="Kuliah Analisis Big Data"
LABEL description="Template Tugas 1 - Analisis Big Data (Semester Ganjil 2026)"

USER root

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Kembali ke user notebook
USER ${NB_UID}

WORKDIR /home/jovyan/work

# Salin seluruh isi repositori
COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan/work/

EXPOSE 8888
