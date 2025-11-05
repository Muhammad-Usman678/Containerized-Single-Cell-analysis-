# 🧬 Single-Cell RNA-seq Analysis Pipeline

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A comprehensive, reproducible single-cell RNA-sequencing analysis pipeline for PBMC data using Scanpy. Performs quality control, normalization, clustering, marker gene discovery, and cell type annotation with complete Docker support and interactive HTML reporting.

## 🌟 Live Demo

**[📊 View Interactive Report](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)**

---

## ✨ Features

- **Complete Analysis Pipeline**: End-to-end scRNA-seq workflow from raw data to publication-ready results
- **Quality Control**: Automated cell and gene filtering with comprehensive QC metrics
- **Dimensionality Reduction**: PCA and UMAP for visualization
- **Multi-Resolution Clustering**: Leiden clustering at resolutions 0.4, 0.8, and 1.2
- **Marker Gene Discovery**: Wilcoxon rank-sum test for differential expression
- **Cell Type Annotation**: Automated annotation using known PBMC markers
- **Interactive HTML Report**: Beautiful web-based report with all visualizations
- **Docker Support**: Fully containerized for reproducibility
- **GitHub Pages**: Live deployment of results

---

## 📊 Dataset

- **Source**: [10X Genomics PBMC 3k Dataset](https://support.10xgenomics.com/single-cell-gene-expression/datasets)
- **Cells**: 2,700 peripheral blood mononuclear cells (PBMCs)
- **Genes**: ~13,700 genes detected
- **Technology**: Chromium Single Cell 3' Gene Expression
- **Cell Types**: T cells, B cells, Monocytes, NK cells

---

## 🚀 Quick Start

### Prerequisites

- **Docker**: Docker Desktop for containerized execution
- **Python 3.11+**: For local execution
- **4GB+ RAM**: For data processing
- **2GB+ disk space**: For data and results

### Option 1: Docker (Recommended)

#### Windows

```powershell
# 1. Start Docker Desktop (from Windows Start menu)

# 2. Navigate to project
cd cancer-mlops

# 3. Run the automated script
.\run_docker.bat

# Results will open automatically in your browser
```

#### Linux/macOS

```bash
# Build and run
docker-compose up sc-analysis

# View results
open results/single_cell_analysis/interactive_report.html  # macOS
xdg-open results/single_cell_analysis/interactive_report.html  # Linux
```

### Option 2: Local Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Download data and run analysis
python download_data.py
python single_cell_analysis.py

# View results
# Windows
start results\single_cell_analysis\interactive_report.html
# macOS
open results/single_cell_analysis/interactive_report.html
# Linux
xdg-open results/single_cell_analysis/interactive_report.html
```

---

## 📁 Project Structure

```
cancer-mlops/
├── data/
│   ├── raw/                          # Downloaded 10X Genomics data
│   │   └── cancer_expression.h5ad    # PBMC 3k dataset (gitignored)
│   └── processed/                    # Preprocessed data (gitignored)
│
├── results/
│   └── single_cell_analysis/
│       ├── figures/                  # 11 analysis plots (PNG)
│       ├── interactive_report.html   # Main HTML report
│       ├── analysis_report.json      # Summary metrics
│       ├── marker_genes.csv          # Top markers per cluster
│       └── processed_data.h5ad       # Final processed data (gitignored)
│
├── docs/                             # GitHub Pages deployment
│   ├── index.html                    # Published interactive report
│   └── landing.html                  # Landing page
│
├── .github/
│   └── workflows/
│       └── pages.yml                 # GitHub Pages deployment workflow
│
├── single_cell_analysis.py           # Main analysis pipeline
├── download_data.py                  # Data download script
├── convert_to_pdf.py                 # HTML to PDF converter (optional)
│
├── Dockerfile                        # Container definition
├── docker-compose.yml                # Docker Compose configuration
├── run_docker.bat                    # Windows automation script
│
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
└── README.md                         # This file
```

---
```

---

## 🔬 Analysis Pipeline

The pipeline performs the following steps:

### 1️⃣ Data Loading
- Downloads PBMC 3k dataset from 10X Genomics (via Scanpy)
- Loads into AnnData format

### 2️⃣ Quality Control
- Calculate QC metrics (genes/cell, counts/cell, mitochondrial %)
- Visualize distributions
- Filter low-quality cells and genes

**QC Thresholds:**
- Min genes per cell: 200
- Max genes per cell: 5,000
- Max mitochondrial %: 20%

### 3️⃣ Normalization & Feature Selection
- Normalize to 10,000 counts per cell
- Log transformation: log(x + 1)
- Identify 2,000 highly variable genes (HVGs)
- Scale data (max value: 10)

### 4️⃣ Dimensionality Reduction
- **PCA**: 50 principal components
- **UMAP**: 2D embedding for visualization
- Compute k-nearest neighbors (k=15)

### 5️⃣ Multi-Resolution Clustering
- Leiden algorithm at resolutions: 0.4, 0.8, 1.2
- Default resolution: 0.8
- Identifies 8-9 distinct cell populations

### 6️⃣ Marker Gene Discovery
- Wilcoxon rank-sum test for differential expression
- Identify top markers per cluster
- Export to CSV

### 7️⃣ Cell Type Annotation
Automated annotation using known PBMC markers:
- **T cells**: CD3D, CD3E, CD8A, CD4
- **B cells**: CD19, MS4A1 (CD20)
- **Monocytes**: CD14, LYZ, FCGR3A (CD16)
- **NK cells**: NKG7, GNLY

### 8️⃣ Report Generation
- Interactive HTML report with all visualizations
- JSON summary with key metrics
- Export processed AnnData object

---

## 📈 Output Files

| File | Description | Size |
|------|-------------|------|
| **Visualizations** (11 plots) | | |
| `01_qc_metrics.png` | QC distributions (counts, genes, MT%) | ~200 KB |
| `02_highly_variable_genes.png` | Top 2,000 HVGs | ~150 KB |
| `03_pca_variance_ratio.png` | PCA variance explained | ~100 KB |
| `04_clustering_resolutions.png` | Multi-resolution clustering | ~500 KB |
| `05_marker_genes_ranking.png` | Top markers per cluster | ~600 KB |
| `06_marker_genes_dotplot.png` | Marker expression dotplot | ~400 KB |
| `07_marker_genes_heatmap.png` | Marker expression heatmap | ~800 KB |
| `08_marker_gene_expression.png` | Known markers on UMAP | ~1 MB |
| `09_umap_clusters.png` | UMAP with cluster labels | ~300 KB |
| `10_umap_qc_metrics.png` | UMAP colored by QC | ~800 KB |
| `11_cluster_composition.png` | Cell count per cluster | ~100 KB |
| **Reports** | | |
| `interactive_report.html` | Complete HTML report | ~10 MB |
| `analysis_report.json` | Metrics summary | ~1 KB |
| `marker_genes.csv` | Top markers per cluster | ~4 MB |

---

## 🐳 Docker Usage

### Simple Analysis (Recommended)

```bash
# Build the image
docker-compose build

# Run analysis
docker-compose up

# Results will be in: results/single_cell_analysis/
```

### Manual Docker Commands

```bash
# Build
docker build -t single-cell-analysis:latest .

# Run with volume mounts
docker run -v $(pwd)/results:/app/results \
           -v $(pwd)/data:/app/data \
           single-cell-analysis:latest

# Windows PowerShell
docker run -v ${PWD}/results:/app/results -v ${PWD}/data:/app/data single-cell-analysis:latest
```

### Docker Features

- **Python 3.11** slim base image
- **System dependencies**: HDF5, build tools
- **Automated execution**: Downloads data → Runs analysis → Generates report
- **Volume mounts**: Results exported to host system
- **No manual intervention**: Complete pipeline in one command

---

## 📊 Example Results

Based on PBMC 3k dataset analysis:

```
=============================================================
SINGLE-CELL ANALYSIS SUMMARY
=============================================================
Total cells analyzed: 2,700
Total genes: ~13,700
Highly variable genes: 2,000
Clusters identified: 8-9 (resolution 0.8)

Mean genes per cell: ~847
Mean counts per cell: ~1,713
Mitochondrial content: ~1.48% (mean)

Cell Type Distribution (approximate):
  T cells: ~60%
  Monocytes: ~20%
  B cells: ~15%
  NK cells: ~5%
=============================================================
```

---

## 🛠️ Requirements

### Python Dependencies

```
scanpy>=1.9.0           # Single-cell analysis
numpy>=1.24.0           # Numerical computing
pandas>=2.0.0           # Data manipulation
matplotlib>=3.7.0       # Plotting
seaborn>=0.12.0         # Statistical visualization
scipy>=1.11.0           # Scientific computing
igraph>=0.11.0          # Graph algorithms
leidenalg>=0.10.0       # Leiden clustering
scikit-misc>=0.3.0      # Statistical methods
loguru>=0.7.0           # Logging
pyyaml>=6.0             # Configuration
h5py>=3.0.0             # HDF5 file handling
```

### System Requirements

- **Python**: 3.11+
- **RAM**: 4GB+ recommended
- **Disk**: 2GB+ for data and results
- **OS**: Windows, macOS, Linux

---

## 📦 What's Included in This Repository

### ✅ Pushed to GitHub
- **Source Code**: All Python scripts
- **Docker Files**: Dockerfile, docker-compose.yml
- **Documentation**: This README
- **HTML Reports**: Interactive reports in `docs/` folder (for GitHub Pages)
- **Configuration**: requirements.txt, .gitignore

### ❌ Not Pushed (Auto-generated/Too Large)
- **Data Files**: `data/` folder (empty directories tracked only)
- **Results**: `results/` folder (generated when you run the pipeline)
- **Models**: `models/` folder (generated during analysis)
- **Python Cache**: `__pycache__`, `.pytest_cache`

**Note**: When you clone and run this project, data will be automatically downloaded and results will be generated locally.

---

## 🌐 GitHub Pages Deployment

The project automatically deploys the interactive HTML report to GitHub Pages.

### How It Works
1. HTML reports are stored in `docs/` folder
2. Push to GitHub triggers automatic deployment
3. Your analysis report becomes a live website

### Enable GitHub Pages
1. Go to your repository **Settings → Pages**
2. Source: Select **Deploy from a branch**
3. Branch: Select **main** (or your branch) and **/docs** folder
4. Save and wait 2-3 minutes
5. Visit: `https://[username].github.io/[repo-name]/`

**Live Example**: [View Demo Report](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)

---

## 🔧 Configuration

Modify analysis parameters in `single_cell_analysis.py`:

```python
# Quality control thresholds
min_genes = 200          # Minimum genes per cell
max_genes = 5000         # Maximum genes per cell
max_mt_pct = 20          # Maximum mitochondrial percentage

# Feature selection
n_top_genes = 2000       # Highly variable genes

# Dimensionality reduction
n_pcs = 50               # PCA components
n_neighbors = 15         # UMAP neighbors

# Clustering
resolutions = [0.4, 0.8, 1.2]  # Leiden resolutions
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Scanpy](https://scanpy.readthedocs.io/) - Single-cell analysis in Python
- [10X Genomics](https://www.10xgenomics.com/) - PBMC datasets
- [Leiden Algorithm](https://www.nature.com/articles/s41598-019-41695-z) - Community detection
- [GitHub Pages](https://pages.github.com/) - Static site hosting

---

## 📞 Contact

- **Repository**: [https://github.com/Muhammad-Usman678/Containerized-Single-Cell-analysis-](https://github.com/Muhammad-Usman678/Containerized-Single-Cell-analysis-)
- **Live Demo**: [https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)

---

## 📚 Additional Resources

- [Scanpy Tutorial](https://scanpy-tutorials.readthedocs.io/)
- [Single-Cell Best Practices](https://www.sc-best-practices.org/)
- [10X Genomics Support](https://support.10xgenomics.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**Built with ❤️ for Bioinformatics Research**

*Last Updated: November 2025*



[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success)](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)

[![Docker](https://img.shields.io/badge/Docker-Supported-blue)](https://www.docker.com/)

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)A comprehensive, reproducible single-cell RNA-seq analysis pipeline for PBMC data using Scanpy.## 🧬 Project Overview

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)



A comprehensive, reproducible single-cell RNA-sequencing analysis pipeline for PBMC data using Scanpy. Performs quality control, normalization, clustering, marker gene discovery, and cell type annotation with complete Docker support and interactive HTML reporting.

## FeaturesProduction-ready MLOps pipeline for cancer single-cell RNA-seq analysis. Classifies immune cell types (B-cells, T-cells, Monocytes, NK-cells) from single-cell gene expression data with 97.76% accuracy.

## 🌟 Live Demo



**[📊 View Interactive Report](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)**

- **Quality Control**: Cell and gene filtering with QC visualizations### Key Features

**[📄 Download PDF Report](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/analysis_report.pdf)**

- **Normalization**: Standard Scanpy preprocessing pipeline- ✅ **Real Data**: 10X Genomics PBMC dataset (1,176 cells, 15,246 genes)

---

- **Dimensionality Reduction**: PCA and UMAP- ✅ **High Accuracy**: 97.76% test accuracy with Random Forest

## ✨ Features

- **Clustering**: Multi-resolution Leiden clustering- ✅ **Production Ready**: FastAPI REST API with MLflow tracking

- **Complete Analysis Pipeline**: End-to-end scRNA-seq workflow from raw data to publication-ready results

- **Quality Control**: Automated cell and gene filtering with comprehensive QC metrics- **Marker Gene Discovery**: Wilcoxon rank-sum test- ✅ **Complete Pipeline**: Data preprocessing → Training → Evaluation → Deployment

- **Dimensionality Reduction**: PCA and UMAP for visualization

- **Multi-Resolution Clustering**: Leiden clustering at resolutions 0.4, 0.8, and 1.2- **Cell Type Annotation**: Automated annotation using known PBMC markers- ✅ **Visualizations**: Confusion matrix, ROC curves, feature importance

- **Marker Gene Discovery**: Wilcoxon rank-sum test for differential expression

- **Cell Type Annotation**: Automated annotation using known PBMC markers- **Interactive HTML Report**: Complete analysis with all plots- ✅ **Monitoring**: Prometheus metrics and drift detection

- **Interactive HTML Report**: Beautiful web-based report with all visualizations

- **PDF Export**: Downloadable PDF version of complete analysis- **Docker Support**: Fully reproducible containerized pipeline

- **Docker Support**: Fully containerized for reproducibility

- **GitHub Pages**: Live deployment of results**Model Performance:**



---## Dataset- Overall Accuracy: 97.76%



## 📊 Dataset- Precision: 97.80% (weighted avg)



- **Source**: [10X Genomics PBMC 3k Dataset](https://support.10xgenomics.com/single-cell-gene-expression/datasets)- **Source**: 10X Genomics PBMC 3k- Recall: 97.76% (weighted avg)

- **Cells**: 2,700 peripheral blood mononuclear cells (PBMCs)

- **Genes**: ~13,700 genes detected- **Cells**: 2,700 peripheral blood mononuclear cells- F1-Score: 97.73% (weighted avg)

- **Technology**: Chromium Single Cell 3' Gene Expression

- **Cell Types**: T cells, B cells, Monocytes, NK cells- **Genes**: ~13,700 genes- ROC-AUC: 99.96%



---



## 🚀 Quick Start## Quick Start---



### Option 1: Docker (Recommended)



```bash### Using Docker (Recommended)## 📁 Project Structure

# Clone repository

git clone https://github.com/Muhammad-Usman678/Containerized-Single-Cell-analysis-.git

cd Containerized-Single-Cell-analysis-

```bash```

# Run with Docker Compose

docker-compose up# Build and runcancer-mlops/



# Results will be in results/single_cell_analysis/docker-compose up├── data/

```

│   ├── raw/                          # Downloaded 10X Genomics data

### Option 2: Local Installation

# Results will be in results/single_cell_analysis/│   └── processed/                    # Preprocessed train/test splits

```bash

# Install dependencies# Open results/single_cell_analysis/interactive_report.html├── src/

pip install -r requirements.txt

```│   ├── preprocess.py                 # Scanpy preprocessing pipeline

# Download data and run analysis

python download_data.py│   ├── train.py                      # Model training with MLflow

python single_cell_analysis.py

### Local Installation│   ├── evaluate.py                   # Evaluation with visualizations

# View results

start results/single_cell_analysis/interactive_report.html  # Windows│   ├── serve.py                      # FastAPI inference server

open results/single_cell_analysis/interactive_report.html   # macOS

xdg-open results/single_cell_analysis/interactive_report.html  # Linux```bash│   └── utils/

```

# Install dependencies│       ├── config.py                 # Configuration management

### Option 3: Generate PDF

pip install -r requirements.txt│       └── data_loader.py            # Data loading utilities

```bash

# Install Playwright├── monitoring/

pip install playwright

python -m playwright install chromium# Download data and run analysis│   ├── drift_detection.py            # EvidentlyAI drift detection



# Convert HTML to PDFpython download_data.py│   └── reports/                      # Drift reports

python convert_to_pdf.py

python single_cell_analysis.py├── models/                           # Trained model artifacts

# PDF saved to: results/single_cell_analysis/analysis_report.pdf

```│   ├── best_model.pkl



---# View interactive report│   ├── label_encoder.pkl



## 📁 Project Structurestart results/single_cell_analysis/interactive_report.html│   └── classification_report.json



``````├── evaluation_results/               # Evaluation outputs

.

├── single_cell_analysis.py          # Main analysis pipeline│   ├── confusion_matrix.png

├── download_data.py                  # Data download script

├── convert_to_pdf.py                 # HTML to PDF converter## Project Structure│   ├── roc_curves_multiclass.png

├── Dockerfile                        # Docker configuration

├── docker-compose.yml                # Multi-container setup│   ├── feature_importance.png

├── requirements.txt                  # Python dependencies

│```│   ├── probability_distribution.png

├── .github/

│   └── workflows/.│   └── evaluation_report.json

│       └── pages.yml                 # GitHub Pages deployment

│├── single_cell_analysis.py    # Main pipeline├── mlruns/                          # MLflow experiment tracking

├── docs/                             # GitHub Pages files

│   ├── index.html                    # Full interactive report├── download_data.py            # Data download├── Dockerfile                        # Container definition

│   ├── landing.html                  # Landing page

│   └── analysis_report.pdf           # PDF version├── Dockerfile                  # Docker config├── docker-compose.yml               # Multi-service orchestration

│

├── data/├── docker-compose.yml          # Docker Compose├── requirements.txt                 # Python dependencies

│   └── raw/                          # Downloaded data (gitignored)

│├── requirements.txt            # Dependencies├── config.yml                       # Pipeline configuration

└── results/

    └── single_cell_analysis/├── data/raw/                   # Raw data├── metrics_dashboard.html           # Interactive metrics dashboard

        ├── figures/                  # 11 analysis plots

        ├── interactive_report.html   # HTML report└── results/single_cell_analysis/└── README.md

        ├── analysis_report.pdf       # PDF report

        ├── analysis_report.json      # Metrics summary    ├── figures/                # 11 plots```

        ├── marker_genes.csv          # Cluster markers

        └── processed_data.h5ad       # Processed data    ├── interactive_report.html # HTML report

```

    ├── analysis_report.json    # Summary---

---

    ├── marker_genes.csv        # Markers

## 🔬 Analysis Pipeline

    └── processed_data.h5ad     # Processed data## 🚀 Quick Start

The pipeline performs the following steps:

```

### 1️⃣ Data Loading

- Downloads PBMC 3k dataset from 10X Genomics### Prerequisites

- Loads into AnnData format for Scanpy

## Analysis Pipeline- Python 3.10 or 3.11

### 2️⃣ Quality Control

- Calculate QC metrics (genes/cell, counts/cell, mitochondrial %)- 4GB+ RAM (for data processing)

- Visualize distributions

- Filter low-quality cells and genes1. **Data Loading** → Load PBMC 3k dataset



### 3️⃣ Normalization & Feature Selection2. **Quality Control** → Calculate and visualize QC metrics### 1. Install Dependencies

- Normalize to 10,000 counts per cell

- Log transformation3. **Filtering** → Filter low-quality cells and genes

- Identify 2,000 highly variable genes (HVGs)

- Scale data for downstream analysis4. **Normalization** → Normalize counts, log transform, find HVGs```bash



### 4️⃣ Dimensionality Reduction5. **Dimensionality Reduction** → PCA + UMAPcd cancer-mlops

- PCA: 50 principal components

- UMAP: 2D embedding for visualization6. **Clustering** → Leiden at resolutions 0.4, 0.8, 1.2pip install -r requirements.txt



### 5️⃣ Clustering7. **Marker Genes** → Identify cluster markers```

- Leiden clustering at multiple resolutions (0.4, 0.8, 1.2)

- Identify distinct cell populations8. **Cell Type Annotation** → Annotate using known markers



### 6️⃣ Marker Gene Discovery9. **Report Generation** → Create interactive HTML report### 2. Download Data & Preprocess

- Wilcoxon rank-sum test for differential expression

- Identify top markers per cluster

- Export to CSV for further analysis

## Output Files```python

### 7️⃣ Cell Type Annotation

- Annotate using known PBMC markers:# Download GSE72056 melanoma data

  - **T cells**: CD3D, CD3E, CD8A, CD4

  - **B cells**: CD19, MS4A1 (CD20)| File | Description |python -c "

  - **Monocytes**: CD14, LYZ, FCGR3A (CD16)

  - **NK cells**: NKG7, GNLY|------|-------------|from src.utils.data_loader import download_sample_data



### 8️⃣ Report Generation| `01_qc_metrics.png` | QC distributions |download_sample_data()

- Create interactive HTML report with all visualizations

- Generate PDF version for sharing| `02_highly_variable_genes.png` | HVG identification |"

- Export metrics to JSON

| `03_pca_variance_ratio.png` | PCA variance |```

---

| `04_clustering_resolutions.png` | Multi-resolution clustering |

## 📈 Output Files

| `05_marker_genes_ranking.png` | Top markers |Or place your own `cancer_expression.csv` in the `data/` directory.

| File | Description | Size |

|------|-------------|------|| `06_marker_genes_dotplot.png` | Marker dotplot |

| **Visualizations** (11 plots) | | |

| `01_qc_metrics.png` | QC distributions (counts, genes, MT%) | ~200 KB || `07_marker_genes_heatmap.png` | Marker heatmap |### 3. Run the Pipeline Locally

| `02_highly_variable_genes.png` | Top 2,000 HVGs | ~150 KB |

| `03_pca_variance_ratio.png` | PCA variance explained | ~100 KB || `08_marker_gene_expression.png` | Known markers on UMAP |

| `04_clustering_resolutions.png` | Multi-resolution clustering | ~500 KB |

| `05_marker_genes_ranking.png` | Top markers per cluster | ~600 KB || `09_umap_clusters.png` | UMAP with clusters |#### Step 1: Preprocess Data

| `06_marker_genes_dotplot.png` | Marker expression dotplot | ~400 KB |

| `07_marker_genes_heatmap.png` | Marker expression heatmap | ~800 KB || `10_umap_qc_metrics.png` | UMAP with QC |```bash

| `08_marker_gene_expression.png` | Known markers on UMAP | ~1 MB |

| `09_umap_clusters.png` | UMAP with cluster labels | ~300 KB || `11_cluster_composition.png` | Cluster sizes |python src/preprocess.py --input data/cancer_expression.csv --output data/processed/preprocessed_data.h5ad

| `10_umap_qc_metrics.png` | UMAP colored by QC | ~800 KB |

| `11_cluster_composition.png` | Cell count per cluster | ~100 KB || `interactive_report.html` | **Complete interactive report** |```

| **Reports** | | |

| `interactive_report.html` | Complete HTML report | ~10 MB |

| `analysis_report.pdf` | PDF version | ~8 MB |

| `analysis_report.json` | Metrics summary | ~1 KB |## Requirements#### Step 2: Train Model

| **Data** | | |

| `marker_genes.csv` | Top markers per cluster | ~4 MB |```bash

| `processed_data.h5ad` | Processed AnnData (not on GitHub) | ~350 MB |

```python src/train.py --data data/processed/preprocessed_data.h5ad --model-type randomforest

---

scanpy>=1.9.0```

## 🐳 Docker Deployment

numpy>=1.24.0

### Build and Run

pandas>=2.0.0

```bash

# Build imagematplotlib>=3.7.0```bash

docker build -t single-cell-analysis .

seaborn>=0.12.0# Data automatically downloads on first run

# Run container

docker run -v $(pwd)/results:/app/results single-cell-analysisloguru>=0.7.0python src/preprocess.py --input data/raw/cancer_expression.h5ad --output data/processed/preprocessed_data.h5ad --split



# Or use Docker Composescipy>=1.11.0```

docker-compose up

```igraph>=0.11.0



### Dockerfile Featuresleidenalg>=0.10.0**Output:**

- Python 3.11 slim base image

- System dependencies (HDF5, build tools)```- `data/processed/preprocessed_data.h5ad` - Full preprocessed dataset

- Automated data download and analysis

- Results exported via volume mount- `data/processed/train_data.h5ad` - Training set (890 cells)



---## Docker- `data/processed/test_data.h5ad` - Test set (223 cells)



## 📊 Example Results



Based on PBMC 3k dataset analysis:```bash### 3. Train Model



- **Total Cells Analyzed**: 2,700# Build

- **Genes Detected**: ~13,700

- **Highly Variable Genes**: 2,000docker build -t sc-analysis .```bash

- **Clusters Identified**: 8-9 (depending on resolution)

- **Mean Genes per Cell**: ~847python src/train.py --data data/processed/train_data.h5ad --model-type randomforest

- **Mean Counts per Cell**: ~1,713

- **Mitochondrial Content**: ~1.48% (mean)# Run```



**Cell Type Distribution** (approximate):docker run -v $(pwd)/results:/app/results sc-analysis

- T cells: ~60%

- Monocytes: ~20%**Output:**

- B cells: ~15%

- NK cells: ~5%# Or use docker-compose- `models/best_model.pkl` - Trained model



---docker-compose up- `models/label_encoder.pkl` - Label encoder



## 🛠️ Requirements```- `mlruns/` - MLflow experiment tracking



### Python Dependencies

```

scanpy>=1.9.0## Author### 4. Evaluate Model

numpy>=1.24.0

pandas>=2.0.0

matplotlib>=3.7.0

seaborn>=0.12.0Bioinformatics Single-Cell Analysis Pipeline```bash

scipy>=1.11.0

igraph>=0.11.0python src/evaluate.py --model models --data data/processed/test_data.h5ad

leidenalg>=0.10.0

scikit-misc>=0.3.0## License```

loguru>=0.7.0

pyyaml>=6.0

playwright>=1.55.0  # For PDF generation

```MIT**Output:**



### System Requirements- `evaluation_results/confusion_matrix.png`

- Python 3.11+- `evaluation_results/roc_curves_multiclass.png`

- 4GB+ RAM- `evaluation_results/feature_importance.png`

- 2GB+ disk space- `evaluation_results/probability_distribution.png`

- `evaluation_results/evaluation_report.json`

---

### 5. Start API Server

## 🌐 GitHub Pages Deployment

```bash

The project is configured for automatic GitHub Pages deployment:python src/serve.py

```

1. **HTML Report**: Hosted at [https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)

2. **PDF Download**: Available at `/analysis_report.pdf`**Access:**

3. **Auto-Deploy**: GitHub Actions workflow triggers on push to `main`- API Documentation: http://localhost:8001/docs

- Health Check: http://localhost:8001/health

### Enable GitHub Pages- Prometheus Metrics: http://localhost:8001/metrics



1. Go to: **Settings → Pages**### 6. View Metrics

2. Source: **GitHub Actions**

3. Workflow runs automatically on push**Option 1: HTML Dashboard**

- Open `metrics_dashboard.html` in your browser

---

**Option 2: MLflow UI**

## 📖 Usage Examples```bash

python -m mlflow ui

### Run Full Pipeline# Visit http://localhost:5000

```

```python

# Download data---

from download_data import download_10k_dataset

download_10k_dataset()## 📊 View Results



# Run analysis### Metrics Dashboard

import subprocessDouble-click `metrics_dashboard.html` for an interactive view of all metrics.

subprocess.run(["python", "single_cell_analysis.py"])

```### Visualizations

Open any file in `evaluation_results/`:

### Load Processed Data- `confusion_matrix.png` - Prediction accuracy per class

- `roc_curves_multiclass.png` - ROC curves for all cell types

```python- `feature_importance.png` - Top contributing PCA components

import scanpy as sc- `probability_distribution.png` - Prediction confidence distribution



# Load processed data### MLflow Tracking

adata = sc.read_h5ad("results/single_cell_analysis/processed_data.h5ad")```bash

python -m mlflow ui --port 5000

# Access results```

print(f"Cells: {adata.n_obs}")View experiments, parameters, metrics, and artifacts at http://localhost:5000

print(f"Genes: {adata.n_vars}")

print(f"Clusters: {adata.obs['clusters'].unique()}")---



# Plot UMAP## 🔌 API Usage

sc.pl.umap(adata, color='clusters')

```### Example: Single Prediction



### Generate Custom PDF```python

import requests

```pythonimport numpy as np

from convert_to_pdf import html_to_pdf_playwright

# Generate 50 PCA features (or use your own preprocessed data)

# Convert any HTML to PDFfeatures = np.random.randn(50).tolist()

html_to_pdf_playwright()

```response = requests.post(

    "http://localhost:8001/predict",

---    json={

        "sample_id": "test_cell_001",

## 🔧 Configuration        "features": features

    }

Modify analysis parameters by editing `single_cell_analysis.py`:)



```pythonprint(response.json())

# Quality control thresholds# Output:

min_genes = 200          # Minimum genes per cell# {

max_genes = 5000         # Maximum genes per cell#   "sample_id": "test_cell_001",

max_mt_pct = 20          # Maximum mitochondrial percentage#   "predicted_label": "T-cell",

#   "probability": 0.95,

# Feature selection#   "all_probabilities": {

n_top_genes = 2000       # Number of highly variable genes#     "B-cell": 0.02,

#     "Monocyte": 0.01,

# Dimensionality reduction#     "NK-cell": 0.02,

n_pcs = 50               # Number of PCA components#     "T-cell": 0.95

n_neighbors = 15         # Number of neighbors for UMAP#   },

#   "model_version": "v1.0",

# Clustering#   "timestamp": "2025-11-04T..."

resolutions = [0.4, 0.8, 1.2]  # Leiden resolutions# }

``````



------



## 🤝 Contributing## 🐳 Docker Deployment



Contributions welcome! Please:### Run with Docker Compose



1. Fork the repository```bash

2. Create a feature branch (`git checkout -b feature/amazing-feature`)docker-compose up

3. Commit changes (`git commit -m 'Add amazing feature'`)```

4. Push to branch (`git push origin feature/amazing-feature`)

5. Open a Pull RequestThis starts:

- FastAPI server (port 8001)

---- MLflow server (port 5000)

- Prometheus (port 9090)

## 📄 License- Grafana (port 3000)



This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.### Build Custom Image



---```bash

docker build -t cancer-classifier:latest .

## 🙏 Acknowledgmentsdocker run -p 8001:8001 cancer-classifier:latest

```

- [Scanpy](https://scanpy.readthedocs.io/) - Single-cell analysis in Python```bash

- [10X Genomics](https://www.10xgenomics.com/) - PBMC datasetsdocker-compose up -d

- [Leiden Algorithm](https://www.nature.com/articles/s41598-019-41695-z) - Community detection# Services: API, MLflow, Prometheus, Grafana

- [Playwright](https://playwright.dev/) - HTML to PDF conversion```

- [GitHub Pages](https://pages.github.com/) - Static site hosting

---

---

## 🔄 CI/CD Pipeline

## 📞 Contact

The GitHub Actions workflow (`.github/workflows/mlops.yml`) automatically:

- **Repository**: [https://github.com/Muhammad-Usman678/Containerized-Single-Cell-analysis-](https://github.com/Muhammad-Usman678/Containerized-Single-Cell-analysis-)

- **Live Demo**: [https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/](https://muhammad-usman678.github.io/Containerized-Single-Cell-analysis-/)1. **Lint & Test**: Runs flake8, black, and pytest

- **Issues**: [GitHub Issues](https://github.com/Muhammad-Usman678/Containerized-Single-Cell-analysis-/issues)2. **Train Model**: Executes training pipeline with MLflow logging

3. **Build Docker**: Creates and pushes container image

---4. **Deploy**: Updates the production endpoint

5. **Monitor**: Triggers drift detection checks

## 📚 Additional Resources

### Trigger Workflow

- [Scanpy Tutorial](https://scanpy-tutorials.readthedocs.io/)Push to `main` branch or create a pull request:

- [Single-Cell Best Practices](https://www.sc-best-practices.org/)```bash

- [10X Genomics Support](https://support.10xgenomics.com/)git add .

- [Nature Protocols: scRNA-seq](https://www.nature.com/nprot/)git commit -m "Update model training"

git push origin main

---```



**Built with ❤️ for Bioinformatics Research**### Required Secrets

Configure in GitHub Settings > Secrets:

*Last Updated: November 2025*- `DOCKERHUB_USERNAME`: Docker Hub username

- `DOCKERHUB_TOKEN`: Docker Hub access token
- `MLFLOW_TRACKING_URI`: MLflow server URL (optional)
- `AWS_ACCESS_KEY_ID`: For S3 storage (optional)
- `AWS_SECRET_ACCESS_KEY`: For S3 storage (optional)

---

## 📈 MLflow Tracking

### Start MLflow UI
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
# Access at http://localhost:5000
```

### Track Experiments
All training runs are automatically logged with:
- **Parameters**: Model hyperparameters, preprocessing settings
- **Metrics**: Accuracy, F1-score, precision, recall, AUC-ROC
- **Artifacts**: Trained models, confusion matrices, feature importance plots
- **Tags**: Dataset version, experiment name

---

## 📊 Monitoring with EvidentlyAI

### Drift Detection
```bash
python monitoring/drift_detection.py \
  --reference data/processed/train_data.h5ad \
  --current data/new_batch.h5ad \
  --output monitoring/reports/
```

The drift report includes:
- **Data Drift**: Distribution changes in gene expression features
- **Target Drift**: Label distribution changes
- **Model Performance**: Accuracy degradation over time
- **Data Quality**: Missing values, duplicates, correlations

### Continuous Monitoring
Set up a cron job or scheduled task:
```bash
# Run drift detection daily
0 2 * * * cd /path/to/cancer-mlops && python monitoring/drift_detection.py
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

---

## 📦 Data Processing Pipeline

### Preprocessing Steps (Scanpy)
1. **Quality Control**: Filter cells and genes
   - Min genes per cell: 200
   - Min cells per gene: 3
   - Max mitochondrial content: 5%

2. **Normalization**: Total-count normalization (10,000 counts per cell)

3. **Log Transformation**: log(x + 1)

4. **Feature Selection**: Highly variable genes (top 2000)

5. **Dimensionality Reduction**: PCA (50 components)

6. **Scaling**: Standard scaling for ML models

### For Big Data (Spark Integration)
```python
# Optional: Process with PySpark
from src.utils.spark_processor import preprocess_with_spark

preprocessed_df = preprocess_with_spark(
    input_path="s3://bucket/cancer_data.csv",
    output_path="s3://bucket/processed/",
    n_partitions=100
)
```

---

## 🤖 Model Training

### Supported Models
- **RandomForestClassifier**: Default, robust for gene expression
- **XGBoost**: Better performance, handles imbalanced data
- **Logistic Regression**: Baseline model
- **Neural Network**: Deep learning option (TensorFlow/PyTorch)

### Hyperparameter Tuning
```bash
python src/train.py \
  --data data/processed/preprocessed_data.h5ad \
  --model-type xgboost \
  --tune \
  --n-trials 50
```

Uses Optuna for Bayesian optimization.

---

## 🌐 API Endpoints

### `GET /health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### `POST /predict`
Single cell prediction.

**Request**:
```json
{
  "gene_expression": [0.5, 1.2, 0.8, ...],
  "sample_id": "cell_001"
}
```

**Response**:
```json
{
  "sample_id": "cell_001",
  "predicted_label": "T-cell",
  "probability": 0.92,
  "all_probabilities": {
    "T-cell": 0.92,
    "B-cell": 0.05,
    "Malignant": 0.03
  },
  "model_version": "1.0.0",
  "timestamp": "2025-11-04T12:34:56"
}
```

### `POST /predict_batch`
Batch prediction for multiple cells.

### `GET /model_info`
Returns model metadata and feature importance.

---

## 🔬 Extension to Enzyme Expression Data (NRPS)

### Adapting for NRPS Data

1. **Data Format**:
   - Replace cell types with enzyme families
   - Gene features → Protein domain features
   - Use NRPS-specific databases (MIBiG, antiSMASH)

2. **Preprocessing Adjustments**:
   ```python
   # src/preprocess_nrps.py
   def preprocess_nrps_data(data):
       # Domain-specific normalization
       # Sequence-based features
       # Structural features from AlphaFold
       pass
   ```

3. **Feature Engineering**:
   - Add sequence motifs
   - Include protein structure features
   - Incorporate phylogenetic information

4. **Model Selection**:
   - Consider sequence-based models (CNNs, Transformers)
   - Use protein language models (ESM, ProtBERT)

### Example Extension
```python
# Future: NRPS prediction pipeline
from src.nrps.preprocess import preprocess_nrps
from src.nrps.train import train_nrps_model

data = preprocess_nrps("data/nrps_sequences.fasta")
model = train_nrps_model(data, model_type="transformer")
```

---

## 🏢 Production Deployment Options

### 1. Cloud Platforms

#### AWS
```bash
# Deploy to ECS/Fargate
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.region.amazonaws.com
docker tag cancer-mlops:latest <account>.dkr.ecr.region.amazonaws.com/cancer-mlops:latest
docker push <account>.dkr.ecr.region.amazonaws.com/cancer-mlops:latest
```

#### Google Cloud
```bash
# Deploy to Cloud Run
gcloud builds submit --tag gcr.io/project-id/cancer-mlops
gcloud run deploy cancer-mlops --image gcr.io/project-id/cancer-mlops --platform managed
```

#### Azure
```bash
# Deploy to Azure Container Instances
az container create --resource-group myResourceGroup --name cancer-mlops --image <registry>/cancer-mlops:latest
```

### 2. Kubernetes
```bash
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
kubectl apply -f k8s/ingress.yml
```

### 3. Feature Store (Feast)
```python
# Optional: Integrate Feast for feature management
from feast import FeatureStore

store = FeatureStore(repo_path=".")
features = store.get_online_features(
    features=["gene_expression:mean", "gene_expression:variance"],
    entity_rows=[{"cell_id": "cell_001"}]
).to_df()
```

---

## 📚 Additional Resources

### Documentation
- [Scanpy Documentation](https://scanpy.readthedocs.io/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [EvidentlyAI Documentation](https://docs.evidentlyai.com/)

### Datasets
- [GEO Database](https://www.ncbi.nlm.nih.gov/geo/)
- [CancerSEA](http://biocc.hrbmu.edu.cn/CancerSEA/)
- [Single Cell Portal](https://singlecell.broadinstitute.org/)

### Papers
- "Machine Learning for Single-Cell Analysis" (Nature Methods, 2020)
- "MLOps: Continuous delivery and automation pipelines in machine learning" (Google Cloud)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License - see LICENSE file for details.

---

## 👥 Authors

- Your Name - Initial work

---

## 🙏 Acknowledgments

- Single-cell analysis community
- MLOps best practices from Google, Netflix, and Uber
- Open-source bioinformatics tools

---

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/your-repo/issues)
- Email: support@example.com
- Slack: #cancer-mlops channel

---

**Last Updated**: November 2025
