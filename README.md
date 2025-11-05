# Single-Cell RNA-seq Analysis Pipeline

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A reproducible single-cell RNA-seq analysis pipeline for PBMC data using **Scanpy**.  
The workflow performs quality control, normalization, clustering, marker gene detection, and automated cell type annotation.  
It is fully containerized with **Docker** and generates an **interactive HTML report** deployable via GitHub Pages.

---

## Live Demo

[View Interactive Report](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)

---

## Features

- Complete end-to-end single-cell RNA-seq workflow  
- Automated quality control and filtering  
- PCA and UMAP for dimensionality reduction  
- Leiden clustering at multiple resolutions  
- Marker gene detection using Wilcoxon rank-sum test  
- Automated PBMC cell type annotation  
- Interactive HTML report generation  
- Fully containerized with Docker for reproducibility  

---

## Dataset

| Attribute | Description |
|------------|-------------|
| Source | [10X Genomics PBMC 3k](https://support.10xgenomics.com/single-cell-gene-expression/datasets) |
| Cells | ~2,700 PBMCs |
| Genes | ~13,700 |
| Technology | Chromium Single Cell 3′ Expression |
| Cell Types | T cells, B cells, Monocytes, NK cells |

---

## Quick Start

### Prerequisites
Docker Desktop or Python 3.11+  
At least 4 GB RAM and 2 GB disk space

### Run with Docker
```bash
docker-compose up sc-analysis
open results/single_cell_analysis/interactive_report.html


