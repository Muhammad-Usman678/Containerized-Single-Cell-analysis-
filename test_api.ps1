# Test the Cancer Cell Classifier API

Write-Host "Testing Cancer Cell Classifier API on http://localhost:8001" -ForegroundColor Green
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing /health endpoint..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8001/health" -Method Get
    Write-Host "✓ Health Status: $($health.status)" -ForegroundColor Green
    Write-Host "  Model Loaded: $($health.model_loaded)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Model Info
Write-Host "2. Testing /model_info endpoint..." -ForegroundColor Cyan
try {
    $info = Invoke-RestMethod -Uri "http://localhost:8001/model_info" -Method Get
    Write-Host "✓ Model Version: $($info.model_version)" -ForegroundColor Green
    Write-Host "  Model Type: $($info.model_type)" -ForegroundColor Green
    Write-Host "  Classes: $($info.classes -join ', ')" -ForegroundColor Green
    Write-Host "  Features: $($info.n_features)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ Model info failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Prediction (sample data)
Write-Host "3. Testing /predict endpoint..." -ForegroundColor Cyan
try {
    # Create sample PCA features (50 random values)
    $features = @()
    for ($i = 0; $i -lt 50; $i++) {
        $features += (Get-Random -Minimum -2.0 -Maximum 2.0)
    }
    
    $body = @{
        sample_id = "test_cell_001"
        features = $features
    } | ConvertTo-Json
    
    $prediction = Invoke-RestMethod -Uri "http://localhost:8001/predict" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✓ Sample ID: $($prediction.sample_id)" -ForegroundColor Green
    Write-Host "  Predicted: $($prediction.predicted_label)" -ForegroundColor Green
    Write-Host "  Confidence: $([math]::Round($prediction.probability * 100, 2))%" -ForegroundColor Green
    Write-Host "  Model Version: $($prediction.model_version)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ Prediction failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "API testing complete!" -ForegroundColor Green
