# Single-Cell RNA-seq Analysis Pipeline 🧬# Cancer Single-Cell RNA-seq Classifier



A comprehensive, reproducible single-cell RNA-seq analysis pipeline for PBMC data using Scanpy.## 🧬 Project Overview



## FeaturesProduction-ready MLOps pipeline for cancer single-cell RNA-seq analysis. Classifies immune cell types (B-cells, T-cells, Monocytes, NK-cells) from single-cell gene expression data with 97.76% accuracy.



- **Quality Control**: Cell and gene filtering with QC visualizations### Key Features

- **Normalization**: Standard Scanpy preprocessing pipeline- ✅ **Real Data**: 10X Genomics PBMC dataset (1,176 cells, 15,246 genes)

- **Dimensionality Reduction**: PCA and UMAP- ✅ **High Accuracy**: 97.76% test accuracy with Random Forest

- **Clustering**: Multi-resolution Leiden clustering- ✅ **Production Ready**: FastAPI REST API with MLflow tracking

- **Marker Gene Discovery**: Wilcoxon rank-sum test- ✅ **Complete Pipeline**: Data preprocessing → Training → Evaluation → Deployment

- **Cell Type Annotation**: Automated annotation using known PBMC markers- ✅ **Visualizations**: Confusion matrix, ROC curves, feature importance

- **Interactive HTML Report**: Complete analysis with all plots- ✅ **Monitoring**: Prometheus metrics and drift detection

- **Docker Support**: Fully reproducible containerized pipeline

**Model Performance:**

## Dataset- Overall Accuracy: 97.76%

- Precision: 97.80% (weighted avg)

- **Source**: 10X Genomics PBMC 3k- Recall: 97.76% (weighted avg)

- **Cells**: 2,700 peripheral blood mononuclear cells- F1-Score: 97.73% (weighted avg)

- **Genes**: ~13,700 genes- ROC-AUC: 99.96%



## Quick Start---



### Using Docker (Recommended)## 📁 Project Structure



```bash```

# Build and runcancer-mlops/

docker-compose up├── data/

│   ├── raw/                          # Downloaded 10X Genomics data

# Results will be in results/single_cell_analysis/│   └── processed/                    # Preprocessed train/test splits

# Open results/single_cell_analysis/interactive_report.html├── src/

```│   ├── preprocess.py                 # Scanpy preprocessing pipeline

│   ├── train.py                      # Model training with MLflow

### Local Installation│   ├── evaluate.py                   # Evaluation with visualizations

│   ├── serve.py                      # FastAPI inference server

```bash│   └── utils/

# Install dependencies│       ├── config.py                 # Configuration management

pip install -r requirements.txt│       └── data_loader.py            # Data loading utilities

├── monitoring/

# Download data and run analysis│   ├── drift_detection.py            # EvidentlyAI drift detection

python download_data.py│   └── reports/                      # Drift reports

python single_cell_analysis.py├── models/                           # Trained model artifacts

│   ├── best_model.pkl

# View interactive report│   ├── label_encoder.pkl

start results/single_cell_analysis/interactive_report.html│   └── classification_report.json

```├── evaluation_results/               # Evaluation outputs

│   ├── confusion_matrix.png

## Project Structure│   ├── roc_curves_multiclass.png

│   ├── feature_importance.png

```│   ├── probability_distribution.png

.│   └── evaluation_report.json

├── single_cell_analysis.py    # Main pipeline├── mlruns/                          # MLflow experiment tracking

├── download_data.py            # Data download├── Dockerfile                        # Container definition

├── Dockerfile                  # Docker config├── docker-compose.yml               # Multi-service orchestration

├── docker-compose.yml          # Docker Compose├── requirements.txt                 # Python dependencies

├── requirements.txt            # Dependencies├── config.yml                       # Pipeline configuration

├── data/raw/                   # Raw data├── metrics_dashboard.html           # Interactive metrics dashboard

└── results/single_cell_analysis/└── README.md

    ├── figures/                # 11 plots```

    ├── interactive_report.html # HTML report

    ├── analysis_report.json    # Summary---

    ├── marker_genes.csv        # Markers

    └── processed_data.h5ad     # Processed data## 🚀 Quick Start

```

### Prerequisites

## Analysis Pipeline- Python 3.10 or 3.11

- 4GB+ RAM (for data processing)

1. **Data Loading** → Load PBMC 3k dataset

2. **Quality Control** → Calculate and visualize QC metrics### 1. Install Dependencies

3. **Filtering** → Filter low-quality cells and genes

4. **Normalization** → Normalize counts, log transform, find HVGs```bash

5. **Dimensionality Reduction** → PCA + UMAPcd cancer-mlops

6. **Clustering** → Leiden at resolutions 0.4, 0.8, 1.2pip install -r requirements.txt

7. **Marker Genes** → Identify cluster markers```

8. **Cell Type Annotation** → Annotate using known markers

9. **Report Generation** → Create interactive HTML report### 2. Download Data & Preprocess



## Output Files```python

# Download GSE72056 melanoma data

| File | Description |python -c "

|------|-------------|from src.utils.data_loader import download_sample_data

| `01_qc_metrics.png` | QC distributions |download_sample_data()

| `02_highly_variable_genes.png` | HVG identification |"

| `03_pca_variance_ratio.png` | PCA variance |```

| `04_clustering_resolutions.png` | Multi-resolution clustering |

| `05_marker_genes_ranking.png` | Top markers |Or place your own `cancer_expression.csv` in the `data/` directory.

| `06_marker_genes_dotplot.png` | Marker dotplot |

| `07_marker_genes_heatmap.png` | Marker heatmap |### 3. Run the Pipeline Locally

| `08_marker_gene_expression.png` | Known markers on UMAP |

| `09_umap_clusters.png` | UMAP with clusters |#### Step 1: Preprocess Data

| `10_umap_qc_metrics.png` | UMAP with QC |```bash

| `11_cluster_composition.png` | Cluster sizes |python src/preprocess.py --input data/cancer_expression.csv --output data/processed/preprocessed_data.h5ad

| `interactive_report.html` | **Complete interactive report** |```



## Requirements#### Step 2: Train Model

```bash

```python src/train.py --data data/processed/preprocessed_data.h5ad --model-type randomforest

scanpy>=1.9.0```

numpy>=1.24.0

pandas>=2.0.0

matplotlib>=3.7.0```bash

seaborn>=0.12.0# Data automatically downloads on first run

loguru>=0.7.0python src/preprocess.py --input data/raw/cancer_expression.h5ad --output data/processed/preprocessed_data.h5ad --split

scipy>=1.11.0```

igraph>=0.11.0

leidenalg>=0.10.0**Output:**

```- `data/processed/preprocessed_data.h5ad` - Full preprocessed dataset

- `data/processed/train_data.h5ad` - Training set (890 cells)

## Docker- `data/processed/test_data.h5ad` - Test set (223 cells)



```bash### 3. Train Model

# Build

docker build -t sc-analysis .```bash

python src/train.py --data data/processed/train_data.h5ad --model-type randomforest

# Run```

docker run -v $(pwd)/results:/app/results sc-analysis

**Output:**

# Or use docker-compose- `models/best_model.pkl` - Trained model

docker-compose up- `models/label_encoder.pkl` - Label encoder

```- `mlruns/` - MLflow experiment tracking



## Author### 4. Evaluate Model



Bioinformatics Single-Cell Analysis Pipeline```bash

python src/evaluate.py --model models --data data/processed/test_data.h5ad

## License```



MIT**Output:**

- `evaluation_results/confusion_matrix.png`
- `evaluation_results/roc_curves_multiclass.png`
- `evaluation_results/feature_importance.png`
- `evaluation_results/probability_distribution.png`
- `evaluation_results/evaluation_report.json`

### 5. Start API Server

```bash
python src/serve.py
```

**Access:**
- API Documentation: http://localhost:8001/docs
- Health Check: http://localhost:8001/health
- Prometheus Metrics: http://localhost:8001/metrics

### 6. View Metrics

**Option 1: HTML Dashboard**
- Open `metrics_dashboard.html` in your browser

**Option 2: MLflow UI**
```bash
python -m mlflow ui
# Visit http://localhost:5000
```

---

## 📊 View Results

### Metrics Dashboard
Double-click `metrics_dashboard.html` for an interactive view of all metrics.

### Visualizations
Open any file in `evaluation_results/`:
- `confusion_matrix.png` - Prediction accuracy per class
- `roc_curves_multiclass.png` - ROC curves for all cell types
- `feature_importance.png` - Top contributing PCA components
- `probability_distribution.png` - Prediction confidence distribution

### MLflow Tracking
```bash
python -m mlflow ui --port 5000
```
View experiments, parameters, metrics, and artifacts at http://localhost:5000

---

## 🔌 API Usage

### Example: Single Prediction

```python
import requests
import numpy as np

# Generate 50 PCA features (or use your own preprocessed data)
features = np.random.randn(50).tolist()

response = requests.post(
    "http://localhost:8001/predict",
    json={
        "sample_id": "test_cell_001",
        "features": features
    }
)

print(response.json())
# Output:
# {
#   "sample_id": "test_cell_001",
#   "predicted_label": "T-cell",
#   "probability": 0.95,
#   "all_probabilities": {
#     "B-cell": 0.02,
#     "Monocyte": 0.01,
#     "NK-cell": 0.02,
#     "T-cell": 0.95
#   },
#   "model_version": "v1.0",
#   "timestamp": "2025-11-04T..."
# }
```

---

## 🐳 Docker Deployment

### Run with Docker Compose

```bash
docker-compose up
```

This starts:
- FastAPI server (port 8001)
- MLflow server (port 5000)
- Prometheus (port 9090)
- Grafana (port 3000)

### Build Custom Image

```bash
docker build -t cancer-classifier:latest .
docker run -p 8001:8001 cancer-classifier:latest
```
```bash
docker-compose up -d
# Services: API, MLflow, Prometheus, Grafana
```

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/mlops.yml`) automatically:

1. **Lint & Test**: Runs flake8, black, and pytest
2. **Train Model**: Executes training pipeline with MLflow logging
3. **Build Docker**: Creates and pushes container image
4. **Deploy**: Updates the production endpoint
5. **Monitor**: Triggers drift detection checks

### Trigger Workflow
Push to `main` branch or create a pull request:
```bash
git add .
git commit -m "Update model training"
git push origin main
```

### Required Secrets
Configure in GitHub Settings > Secrets:
- `DOCKERHUB_USERNAME`: Docker Hub username
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
