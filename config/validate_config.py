#!/usr/bin/env python3
"""
Configuration Validation Script for Churn Prediction Project
This script validates that all required configuration is properly set up.
"""

import os
import sys
from typing import List, Dict, Any
from .config_utils import get_config

def validate_gcp_config(secrets) -> List[str]:
    """Validate GCP configuration"""
    errors = []
    
    if not secrets.GCP_PROJECT_ID or secrets.GCP_PROJECT_ID == "your-gcp-project-id":
        errors.append("GCP_PROJECT_ID is not set or is using default value")
    
    if not secrets.GCP_LOCATION:
        errors.append("GCP_LOCATION is not set")
    
    return errors

def validate_storage_config(secrets) -> List[str]:
    """Validate storage configuration"""
    errors = []
    
    if not secrets.GCS_BUCKET_NAME or secrets.GCS_BUCKET_NAME == "your-bucket-name":
        errors.append("GCS_BUCKET_NAME is not set or is using default value")
    
    return errors

def validate_feature_store_config(secrets) -> List[str]:
    """Validate feature store configuration"""
    errors = []
    
    if not secrets.FEATURE_STORE_ID:
        errors.append("FEATURE_STORE_ID is not set")
    
    if not secrets.ENTITY_TYPE_ID:
        errors.append("ENTITY_TYPE_ID is not set")
    
    return errors

def validate_model_config(secrets) -> List[str]:
    """Validate model configuration"""
    errors = []
    
    if not secrets.MODEL_DISPLAY_NAME:
        errors.append("MODEL_DISPLAY_NAME is not set")
    
    if not secrets.MODEL_ARTIFACT_URI or "your-bucket-name" in secrets.MODEL_ARTIFACT_URI:
        errors.append("MODEL_ARTIFACT_URI is not properly configured")
    
    if not secrets.SERVING_CONTAINER_IMAGE:
        errors.append("SERVING_CONTAINER_IMAGE is not set")
    
    if not secrets.MACHINE_TYPE:
        errors.append("MACHINE_TYPE is not set")
    
    return errors

def validate_container_config(secrets) -> List[str]:
    """Validate container configuration"""
    errors = []
    
    if not secrets.CONTAINER_REGISTRY_PROJECT or secrets.CONTAINER_REGISTRY_PROJECT == "your-gcp-project-id":
        errors.append("CONTAINER_REGISTRY_PROJECT is not set or is using default value")
    
    return errors

def validate_data_config(secrets) -> List[str]:
    """Validate data configuration"""
    errors = []
    
    if not secrets.DATA_FILE_NAME:
        errors.append("DATA_FILE_NAME is not set")
    
    if not secrets.MODEL_FILE_NAME:
        errors.append("MODEL_FILE_NAME is not set")
    
    if not secrets.FEATURE_COLUMNS:
        errors.append("FEATURE_COLUMNS is not set")
    
    if not secrets.TARGET_COLUMN:
        errors.append("TARGET_COLUMN is not set")
    
    return errors

def validate_environment_variables() -> List[str]:
    """Validate environment variables"""
    errors = []
    
    # Check if ENVIRONMENT is set
    env = os.getenv("ENVIRONMENT")
    if not env:
        errors.append("ENVIRONMENT variable is not set")
    
    # Check if GCP credentials are available
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS not set. Using default credentials.")
    
    return errors

def print_config_summary(config):
    """Print configuration summary"""
    secrets = config.secrets
    
    print("\n=== Configuration Summary ===")
    print(f"Environment: {config.environment}")
    print(f"GCP Project: {secrets.GCP_PROJECT_ID}")
    print(f"GCP Location: {secrets.GCP_LOCATION}")
    print(f"Feature Store ID: {secrets.FEATURE_STORE_ID}")
    print(f"Model Name: {secrets.MODEL_DISPLAY_NAME}")
    print(f"Storage Bucket: {secrets.GCS_BUCKET_NAME}")
    print(f"Container Registry: {secrets.CONTAINER_REGISTRY_PROJECT}")
    print("=============================")

def main():
    """Main validation function"""
    print("Churn Prediction Project - Configuration Validation")
    print("=" * 55)
    
    # Get configuration
    try:
        config = get_config()
        secrets = config.secrets
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return False
    
    # Collect all validation errors
    all_errors = []
    
    # Validate each configuration section
    all_errors.extend(validate_gcp_config(secrets))
    all_errors.extend(validate_storage_config(secrets))
    all_errors.extend(validate_feature_store_config(secrets))
    all_errors.extend(validate_model_config(secrets))
    all_errors.extend(validate_container_config(secrets))
    all_errors.extend(validate_data_config(secrets))
    all_errors.extend(validate_environment_variables())
    
    # Print configuration summary
    print_config_summary(config)
    
    # Report validation results
    if all_errors:
        print(f"\n❌ Configuration validation failed with {len(all_errors)} errors:")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")
        
        print("\nTo fix these issues:")
        print("1. Run the configuration setup script: python -m config.setup_config")
        print("2. Update your .env file with the correct values")
        print("3. Set the ENVIRONMENT variable")
        print("4. Ensure you have proper GCP credentials")
        
        return False
    else:
        print("\n✅ Configuration validation passed!")
        print("All required configuration is properly set up.")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 