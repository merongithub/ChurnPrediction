"""
Secrets and Configuration Management for Churn Prediction Project
This file contains all the configuration values and secrets used across the project.
In production, these should be stored securely (e.g., Google Secret Manager, environment variables).
"""

import os
from typing import Dict, Any

class Secrets:
    """Centralized secrets and configuration management"""
    
    # Google Cloud Platform Configuration
    GCP_PROJECT_ID = "your-gcp-project-id"
    GCP_LOCATION = "us-central1"
    GCP_REGION = "us-central1"
    
    # Vertex AI Configuration
    VERTEX_AI_PROJECT = "your-gcp-project-id"
    VERTEX_AI_LOCATION = "us-central1"
    
    # Feature Store Configuration
    FEATURE_STORE_ID = "churn_featurestore"
    ENTITY_TYPE_ID = "customers"
    
    # Model Configuration
    MODEL_DISPLAY_NAME = "churn_model"
    MODEL_ARTIFACT_URI = "gs://your-bucket-name/models/churn_model.joblib"
    SERVING_CONTAINER_IMAGE = "us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest"
    MACHINE_TYPE = "n1-standard-4"
    
    # Storage Configuration
    GCS_BUCKET_NAME = "your-bucket-name"
    GCS_MODELS_PATH = "models/"
    GCS_DATA_PATH = "data/"
    
    # Container Registry Configuration
    CONTAINER_REGISTRY_PROJECT = "your-gcp-project-id"
    CONTAINER_IMAGE_TAG = "latest"
    
    # Kubeflow Pipeline Configuration
    PIPELINE_NAME = "churn-pipeline"
    PIPELINE_DESCRIPTION = "A pipeline to train churn model"
    PIPELINE_PACKAGE_PATH = "churn_pipeline.json"
    
    # Data Configuration
    DATA_FILE_NAME = "customers.csv"
    MODEL_FILE_NAME = "churn_model.joblib"
    
    # Model Training Configuration
    RANDOM_FOREST_ESTIMATORS = 100
    FEATURE_COLUMNS = ["tenure", "MonthlyCharges"]
    TARGET_COLUMN = "Churn"
    TARGET_MAPPING = {"Yes": 1, "No": 0}
    
    # API Configuration
    API_ENDPOINT_NAME = "churn_prediction_endpoint"
    API_VERSION = "v1"
    
    # Monitoring Configuration
    MONITORING_INTERVAL = 3600  # seconds
    ALERT_THRESHOLD = 0.8
    
    @classmethod
    def get_gcp_config(cls) -> Dict[str, str]:
        """Get GCP configuration dictionary"""
        return {
            "project_id": cls.GCP_PROJECT_ID,
            "location": cls.GCP_LOCATION,
            "region": cls.GCP_REGION
        }
    
    @classmethod
    def get_feature_store_config(cls) -> Dict[str, str]:
        """Get Feature Store configuration dictionary"""
        return {
            "featurestore_id": cls.FEATURE_STORE_ID,
            "entity_type_id": cls.ENTITY_TYPE_ID
        }
    
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """Get model configuration dictionary"""
        return {
            "display_name": cls.MODEL_DISPLAY_NAME,
            "artifact_uri": cls.MODEL_ARTIFACT_URI,
            "serving_container_image": cls.SERVING_CONTAINER_IMAGE,
            "machine_type": cls.MACHINE_TYPE,
            "estimators": cls.RANDOM_FOREST_ESTIMATORS
        }
    
    @classmethod
    def get_storage_config(cls) -> Dict[str, str]:
        """Get storage configuration dictionary"""
        return {
            "bucket_name": cls.GCS_BUCKET_NAME,
            "models_path": cls.GCS_MODELS_PATH,
            "data_path": cls.GCS_DATA_PATH
        }
    
    @classmethod
    def get_pipeline_config(cls) -> Dict[str, str]:
        """Get pipeline configuration dictionary"""
        return {
            "name": cls.PIPELINE_NAME,
            "description": cls.PIPELINE_DESCRIPTION,
            "package_path": cls.PIPELINE_PACKAGE_PATH
        }
    
    @classmethod
    def get_container_config(cls) -> Dict[str, str]:
        """Get container configuration dictionary"""
        return {
            "project": cls.CONTAINER_REGISTRY_PROJECT,
            "image_tag": cls.CONTAINER_IMAGE_TAG,
            "full_image_path": f"gcr.io/{cls.CONTAINER_REGISTRY_PROJECT}/python:{cls.CONTAINER_IMAGE_TAG}"
        }

# Environment-specific configurations
class DevelopmentSecrets(Secrets):
    """Development environment secrets"""
    GCP_PROJECT_ID = "dev-churn-prediction-project"
    GCS_BUCKET_NAME = "dev-churn-prediction-bucket"
    CONTAINER_REGISTRY_PROJECT = "dev-churn-prediction-project"

class StagingSecrets(Secrets):
    """Staging environment secrets"""
    GCP_PROJECT_ID = "staging-churn-prediction-project"
    GCS_BUCKET_NAME = "staging-churn-prediction-bucket"
    CONTAINER_REGISTRY_PROJECT = "staging-churn-prediction-project"

class ProductionSecrets(Secrets):
    """Production environment secrets"""
    GCP_PROJECT_ID = "prod-churn-prediction-project"
    GCS_BUCKET_NAME = "prod-churn-prediction-bucket"
    CONTAINER_REGISTRY_PROJECT = "prod-churn-prediction-project"

# Environment detection
def get_secrets() -> Secrets:
    """Get secrets based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSecrets()
    elif env == "staging":
        return StagingSecrets()
    else:
        return DevelopmentSecrets() 