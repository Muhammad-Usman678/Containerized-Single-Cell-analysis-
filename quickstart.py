"""Quick start script to run the entire pipeline."""

import os
import sys
from pathlib import Path

from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.data_loader import download_sample_data
from src.preprocess import preprocess_pipeline
from src.train import train_pipeline
from src.evaluate import evaluate_model


def main():
    """Run the complete pipeline."""
    logger.info("=" * 80)
    logger.info("CANCER MLOPS PIPELINE - QUICK START")
    logger.info("=" * 80)
    
    # Step 1: Download/generate sample data
    logger.info("\n[STEP 1/4] Downloading sample data...")
    data_path = download_sample_data("data/raw")
    logger.info(f"✓ Data ready at {data_path}")
    
    # Step 2: Preprocess data
    logger.info("\n[STEP 2/4] Preprocessing data...")
    preprocessed_path = "data/processed/preprocessed_data.h5ad"
    preprocess_pipeline(
        input_path=data_path,
        output_path=preprocessed_path
    )
    logger.info(f"✓ Preprocessed data saved to {preprocessed_path}")
    
    # Step 3: Train model
    logger.info("\n[STEP 3/4] Training model...")
    model_path = train_pipeline(
        data_path=preprocessed_path,
        model_type="randomforest",
        tune=False,
        output_dir="models"
    )
    logger.info(f"✓ Model saved to {model_path}")
    
    # Step 4: Evaluate model
    logger.info("\n[STEP 4/4] Evaluating model...")
    
    # Create test data by splitting
    from src.utils.data_loader import load_h5ad_data, split_train_test, save_data
    adata = load_h5ad_data(preprocessed_path)
    _, test_adata = split_train_test(adata, test_size=0.2)
    test_path = "data/processed/test_data.h5ad"
    save_data(test_adata, test_path)
    
    evaluate_model(
        model_path="models",
        data_path=test_path,
        output_dir="evaluation_results"
    )
    logger.info("✓ Evaluation complete")
    
    logger.info("\n" + "=" * 80)
    logger.info("PIPELINE COMPLETE!")
    logger.info("=" * 80)
    logger.info("\nNext steps:")
    logger.info("1. View MLflow UI: mlflow ui --backend-store-uri sqlite:///mlflow.db")
    logger.info("2. Start API server: python src/serve.py")
    logger.info("3. Test API: curl http://localhost:8000/health")
    logger.info("4. View evaluation results in: evaluation_results/")
    logger.info("\nTo run with Docker:")
    logger.info("  docker-compose up -d")
    logger.info("\nTo monitor drift:")
    logger.info("  python monitoring/drift_detection.py --reference data/processed/train_data.h5ad --current data/processed/test_data.h5ad")


if __name__ == "__main__":
    main()
