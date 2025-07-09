# Customer Churn Prediction with Vertex AI

A comprehensive machine learning project for predicting customer churn using Google Cloud's Vertex AI platform. This project implements a complete ML pipeline from feature engineering to model deployment with centralized configuration management and robust security practices.

## Project Overview

This project demonstrates a production-ready machine learning workflow for customer churn prediction, utilizing Google Cloud's Vertex AI services including Feature Store, AI Platform, and Kubeflow Pipelines. The project includes a robust configuration management system for secure secrets handling across different environments and comprehensive security measures to prevent accidental exposure of sensitive information.

## Project Structure

```
ChurnPrediction/
├── data/                    # Data storage directory
├── config/                  # Configuration and secrets management
│   ├── __init__.py         # Configuration package initialization
│   ├── secrets.py          # Centralized secrets and configuration
│   ├── config_utils.py     # Configuration utilities and helpers
│   ├── setup_config.py     # Interactive configuration setup
│   └── validate_config.py  # Configuration validation
├── feature_store/           # Feature store implementation
│   └── create_features.py   # Feature store setup and feature definitions
├── training/                # Model training components
│   └── train_custom.py      # Model training script
├── pipeline/                # ML pipeline orchestration
│   └── churn_pipeline.py    # Kubeflow pipeline definition
├── deployment/              # Model deployment components
│   └── deploy_model.py      # Model deployment script
├── scripts/                 # Utility scripts
│   ├── pre-commit-hook.sh   # Pre-commit security checks
│   └── setup-git-hooks.sh   # Git hooks setup script
├── env.example             # Example environment variables
├── .gitignore              # Git ignore rules
├── SECURITY.md             # Security guidelines
├── DO_NOT_COMMIT.md        # Files that should never be committed
└── README.md               # Project documentation
```

## 🔒 **Security & Git Management**

### **Comprehensive Security Setup**
This project includes enterprise-grade security measures to prevent accidental exposure of sensitive information:

#### **1. Git Ignore Rules**
- **`.gitignore`**: Comprehensive ignore rules covering:
  - Credentials and secrets (`.json`, `.env`, `*.key`)
  - Model artifacts (`*.joblib`, `*.pkl`, `*.h5`)
  - Data files (`*.csv`, `*.parquet`, `*.json`)
  - Logs and temporary files (`*.log`, `tmp/`, `cache/`)
  - IDE configurations (`.vscode/`, `.idea/`)
  - OS-generated files (`.DS_Store`, `Thumbs.db`)

#### **2. Pre-commit Security Hooks**
- **Automated Security Checks**: Prevents commits of sensitive files
- **File Type Validation**: Blocks credentials, large files, and data files
- **Pattern Detection**: Scans for hardcoded secrets in code
- **Size Limits**: Warns about files larger than 10MB

#### **3. Security Documentation**
- **`SECURITY.md`**: Comprehensive security guidelines and best practices
- **`DO_NOT_COMMIT.md`**: Complete list of files that should never be committed
- **Emergency Procedures**: Steps to take if secrets are accidentally exposed

### **Setting Up Security Measures**

#### **1. Install Git Hooks**
```bash
# Set up pre-commit hooks and security checks
./scripts/setup-git-hooks.sh
```

#### **2. Test Security Measures**
```bash
# Test the pre-commit hook
./scripts/pre-commit-hook.sh

# Try committing a .env file (should be blocked)
echo "TEST=value" > .env
git add .env
git commit -m "test"  # This should fail
```

#### **3. Validate Configuration**
```bash
# Validate your configuration before committing
python -m config.validate_config
```

## Configuration Management

This project includes a comprehensive configuration management system that supports:

### 🔐 **Centralized Secrets Management**
- All configuration values stored in `config/secrets.py`
- Environment-specific configurations (Development, Staging, Production)
- Secure handling of sensitive information
- Easy configuration updates across the entire project

### 🌍 **Multi-Environment Support**
- **Development**: `dev-churn-prediction-project`
- **Staging**: `staging-churn-prediction-project`  
- **Production**: `prod-churn-prediction-project`

### 📋 **Configuration Properties**

#### Google Cloud Platform
- `GCP_PROJECT_ID`: Your GCP project identifier
- `GCP_LOCATION`: GCP region (e.g., us-central1)
- `GCP_REGION`: GCP region for services

#### Vertex AI & Feature Store
- `FEATURE_STORE_ID`: Feature store identifier
- `ENTITY_TYPE_ID`: Entity type for customers
- `MODEL_DISPLAY_NAME`: Model display name
- `SERVING_CONTAINER_IMAGE`: Container image for serving

#### Storage Configuration
- `GCS_BUCKET_NAME`: Google Cloud Storage bucket
- `GCS_MODELS_PATH`: Path for model artifacts
- `GCS_DATA_PATH`: Path for data files

#### Model Configuration
- `RANDOM_FOREST_ESTIMATORS`: Number of estimators
- `FEATURE_COLUMNS`: List of feature columns
- `TARGET_COLUMN`: Target variable name
- `MACHINE_TYPE`: Compute machine type

#### Pipeline Configuration
- `PIPELINE_NAME`: Kubeflow pipeline name
- `PIPELINE_DESCRIPTION`: Pipeline description
- `CONTAINER_REGISTRY_PROJECT`: Container registry project

## Components

### 1. Feature Store (`feature_store/create_features.py`)
- Creates a Vertex AI Feature Store for centralized feature management
- Defines customer entity type with features:
  - `tenure`: Customer tenure (DOUBLE)
  - `monthly_charges`: Monthly charges (DOUBLE)
- Provides scalable feature serving for ML models
- **Uses centralized configuration** for all GCP settings

### 2. Model Training (`training/train_custom.py`)
- Implements Random Forest classifier for churn prediction
- Uses customer data with features: tenure and monthly charges
- Saves trained model as joblib file
- Handles binary classification (Churn: Yes/No)
- **Configurable model parameters** via secrets

### 3. ML Pipeline (`pipeline/churn_pipeline.py`)
- Kubeflow Pipeline for orchestrating the ML workflow
- Sequential execution: Feature Store creation → Model Training
- Containerized operations for reproducibility
- Compiles to JSON format for deployment
- **Dynamic container image configuration**

### 4. Model Deployment (`deployment/deploy_model.py`)
- Deploys trained model to Vertex AI endpoints
- Uses scikit-learn serving container
- Configures machine type for inference
- Provides REST API endpoint for predictions
- **Environment-aware deployment settings**

## Prerequisites

- Google Cloud Platform account
- Vertex AI API enabled
- Kubeflow Pipelines SDK
- Required Python packages:
  - `google-cloud-aiplatform`
  - `kfp` (Kubeflow Pipelines)
  - `pandas`
  - `scikit-learn`
  - `joblib`

## Setup Instructions

### 1. **Security Setup**
```bash
# Set up Git hooks and security measures
./scripts/setup-git-hooks.sh

# Copy and configure environment variables
cp env.example .env
# Edit .env with your actual values
```

### 2. **Configuration Setup**
```bash
# Run interactive configuration setup
python -m config.setup_config

# Validate your configuration
python -m config.validate_config
```

### 3. **Configure Google Cloud Project**
```bash
# Set your GCP project ID
export PROJECT_ID="your-gcp-project"
gcloud config set project $PROJECT_ID
```

### 4. **Enable Required APIs**
```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable container.googleapis.com
```

### 5. **Install Dependencies**
```bash
pip install google-cloud-aiplatform kfp pandas scikit-learn joblib
```

## Usage

### 1. Create Feature Store
```bash
cd feature_store
python create_features.py
```

### 2. Train Model
```bash
cd training
python train_custom.py
```

### 3. Run ML Pipeline
```bash
cd pipeline
python churn_pipeline.py
```

### 4. Deploy Model
```bash
cd deployment
python deploy_model.py
```

## Configuration Management

### Setting Environment
```bash
# Set environment (development, staging, production)
export ENVIRONMENT=development
```

### Using Configuration in Code
```python
from config import get_config

# Get configuration for current environment
config = get_config()
secrets = config.secrets

# Use configuration values
project_id = secrets.GCP_PROJECT_ID
bucket_name = secrets.GCS_BUCKET_NAME
```

### Configuration Validation
```bash
# Validate configuration before running
python -m config.validate_config
```

## Data Requirements

The training script expects a CSV file named `customers.csv` with the following columns:
- `tenure`: Customer tenure (numeric)
- `MonthlyCharges`: Monthly charges (numeric)
- `Churn`: Target variable (Yes/No)

## Model Performance

The Random Forest classifier is configured with:
- 100 estimators (configurable)
- Binary classification for churn prediction
- Features: tenure and monthly charges

## API Endpoints

Once deployed, the model provides a REST API endpoint for real-time predictions:
- Input: JSON with `tenure` and `monthly_charges`
- Output: Churn prediction (0 or 1)

## Security Best Practices

### 🔒 **Secrets Management**
- Never commit real secrets to version control
- Use environment variables for sensitive data
- Consider using Google Secret Manager for production
- Validate configuration before deployment

### 🛡️ **Environment Isolation**
- Separate configurations for each environment
- Use different GCP projects for dev/staging/prod
- Implement proper IAM roles and permissions

### 🚨 **Pre-commit Security**
- Automated checks prevent accidental commits of sensitive files
- Pattern detection identifies potential secrets in code
- File size limits prevent large file commits
- Comprehensive validation before each commit

## Monitoring and Maintenance

- Monitor model performance through Vertex AI console
- Set up alerts for model drift
- Regularly retrain models with new data
- Update feature store with new features as needed
- Validate configuration changes before deployment
- Run security scans regularly

## Troubleshooting

### Common Issues
1. **Configuration not found**: Run `python -m config.validate_config`
2. **GCP authentication**: Set `GOOGLE_APPLICATION_CREDENTIALS`
3. **Missing environment**: Set `ENVIRONMENT` variable
4. **Invalid project ID**: Update `GCP_PROJECT_ID` in configuration
5. **Pre-commit hook fails**: Check `SECURITY.md` for guidance

### Getting Help
- Run configuration validation: `python -m config.validate_config`
- Check environment variables: `echo $ENVIRONMENT`
- Verify GCP credentials: `gcloud auth list`
- Review security guidelines: `SECURITY.md`
- Check what not to commit: `DO_NOT_COMMIT.md`

