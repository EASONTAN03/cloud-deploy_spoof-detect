# Cloud Deployment Guide

This directory contains the cloud deployment configuration for the Face Anti-Spoofing Detection project.

## 🔗 Repository Structure

- **Main Project**: `spoof-object-detect` (this repository)
- **Cloud Deployment**: `cloud-deploy_spoof-detect` (separate repository)
  - GitHub: https://github.com/EASONTAN03/cloud-deploy_spoof-detect
  - Render: Auto-deployed from the cloud deployment repo

## 📁 Current Setup

```
cloud-deploy_spoof-detect/
├── Dockerfile              # Docker configuration
├── render.yaml             # Render deployment config
├── requirements.txt        # Python dependencies
├── app/
│   ├── main.py            # FastAPI application
│   └── model/
│       └── best.pt        # Trained model (copy from main project)
└── DEPLOYMENT_GUIDE.md    # This file
```

## 🔄 Updating Model

When you update the model in the main project:

1. **Copy the new model** from main project:
   ```bash
   # From the main project directory
   cp outputs/models/Spoof-Detect-1-1/weights/best.pt deploy_models/cloud-deploy_spoof-detect/app/model/
   ```

2. **Update the cloud deployment repo**:
   ```bash
   cd deploy_models/cloud-deploy_spoof-detect
   git add app/model/best.pt
   git commit -m "Update model to latest version"
   git push origin main
   ```

3. **Render will auto-deploy** the updated model

## 🔧 Configuration

### Model Path
The FastAPI app loads the model from `app/model/best.pt`. Make sure this path is correct.

### Environment Variables
Add these to your Render environment if needed:
- `MODEL_PATH`: Path to the model file (default: `app/model/best.pt`)
- `CONFIDENCE_THRESHOLD`: Detection confidence (default: 0.45)
- `IOU_THRESHOLD`: IoU threshold (default: 0.8)

## 🚀 Deployment

This deployment is configured for Render.com:

1. **Repository**: https://github.com/EASONTAN03/cloud-deploy_spoof-detect
2. **Auto-deploy**: Enabled
3. **Environment**: Docker
4. **Build Command**: `docker build -t spoof-detect-api .`
5. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## 📡 API Endpoints

- `GET /`: Health check
- `POST /predict/`: Image prediction
  - Input: Image file (multipart/form-data)
  - Output: JSON with predictions

## 🔗 Integration with Main Project

The main project (`spoof-object-detect`) contains:
- Training code and notebooks
- Dataset processing utilities
- Model training scripts
- Local inference tools

This cloud deployment provides:
- REST API for predictions
- Docker containerization
- Cloud hosting on Render

## 📝 Usage Example

```python
import requests

# API endpoint
url = "https://your-render-app.onrender.com/predict/"

# Upload image
with open("test.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

# Get predictions
predictions = response.json()
print(predictions)
```

## 🔄 Workflow

1. **Develop** in main project (`spoof-object-detect`)
2. **Train** new models in main project
3. **Copy** best model to cloud deployment
4. **Push** cloud deployment changes
5. **Auto-deploy** on Render

## 📞 Support

For issues with:
- **Main project**: Create issue in `spoof-object-detect` repo
- **Cloud deployment**: Create issue in `cloud-deploy_spoof-detect` repo
- **Render deployment**: Check Render dashboard logs 