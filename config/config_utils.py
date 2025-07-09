"""
Configuration Utilities for Churn Prediction Project
Helper functions for loading, validating, and managing configuration.
"""

import os
import json
from typing import Dict, Any, Optional
from .secrets import get_secrets, Secrets

class ConfigManager:
    """Configuration manager for the Churn Prediction project"""
    
    def __init__(self, environment: Optional[str] = None):
        """Initialize configuration manager"""
        self.environment = environment or os.getenv("ENVIRONMENT", "development")
        self.secrets = get_secrets()
    
    def validate_config(self) -> bool:
        """Validate that all required configuration is present"""
        required_fields = [
            'GCP_PROJECT_ID',
            'GCP_LOCATION', 
            'GCS_BUCKET_NAME',
            'FEATURE_STORE_ID',
            'MODEL_DISPLAY_NAME'
        ]
        
        for field in required_fields:
            if not hasattr(self.secrets, field) or not getattr(self.secrets, field):
                print(f"Missing required configuration: {field}")
                return False
        
        return True
    
    def get_gcp_credentials_path(self) -> str:
        """Get path to GCP service account key file"""
        return os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    
    def export_environment_variables(self) -> Dict[str, str]:
        """Export configuration as environment variables"""
        env_vars = {
            "GCP_PROJECT_ID": self.secrets.GCP_PROJECT_ID,
            "GCP_LOCATION": self.secrets.GCP_LOCATION,
            "GCS_BUCKET_NAME": self.secrets.GCS_BUCKET_NAME,
            "FEATURE_STORE_ID": self.secrets.FEATURE_STORE_ID,
            "MODEL_DISPLAY_NAME": self.secrets.MODEL_DISPLAY_NAME,
            "ENVIRONMENT": self.environment
        }
        
        for key, value in env_vars.items():
            os.environ[key] = value
        
        return env_vars
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration"""
        return {
            "environment": self.environment,
            "gcp_config": self.secrets.get_gcp_config(),
            "feature_store_config": self.secrets.get_feature_store_config(),
            "model_config": self.secrets.get_model_config(),
            "storage_config": self.secrets.get_storage_config(),
            "pipeline_config": self.secrets.get_pipeline_config()
        }
    
    def print_config_summary(self):
        """Print configuration summary to console"""
        summary = self.get_config_summary()
        print("=== Configuration Summary ===")
        print(f"Environment: {summary['environment']}")
        print(f"GCP Project: {summary['gcp_config']['project_id']}")
        print(f"GCP Location: {summary['gcp_config']['location']}")
        print(f"Feature Store ID: {summary['feature_store_config']['featurestore_id']}")
        print(f"Model Name: {summary['model_config']['display_name']}")
        print(f"Storage Bucket: {summary['storage_config']['bucket_name']}")
        print("=============================")

def load_config_from_file(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Invalid JSON in configuration file: {config_path}")
        return {}

def save_config_to_file(config: Dict[str, Any], config_path: str):
    """Save configuration to JSON file"""
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Configuration saved to: {config_path}")
    except Exception as e:
        print(f"Error saving configuration: {e}")

def create_env_file(config_manager: ConfigManager, env_file_path: str = ".env"):
    """Create .env file with configuration"""
    env_vars = config_manager.export_environment_variables()
    
    with open(env_file_path, 'w') as f:
        f.write("# Churn Prediction Project Environment Variables\n")
        f.write(f"ENVIRONMENT={config_manager.environment}\n")
        f.write(f"GCP_PROJECT_ID={config_manager.secrets.GCP_PROJECT_ID}\n")
        f.write(f"GCP_LOCATION={config_manager.secrets.GCP_LOCATION}\n")
        f.write(f"GCS_BUCKET_NAME={config_manager.secrets.GCS_BUCKET_NAME}\n")
        f.write(f"FEATURE_STORE_ID={config_manager.secrets.FEATURE_STORE_ID}\n")
        f.write(f"MODEL_DISPLAY_NAME={config_manager.secrets.MODEL_DISPLAY_NAME}\n")
        f.write(f"CONTAINER_REGISTRY_PROJECT={config_manager.secrets.CONTAINER_REGISTRY_PROJECT}\n")
    
    print(f"Environment file created: {env_file_path}")

# Convenience function to get configuration
def get_config(environment: Optional[str] = None) -> ConfigManager:
    """Get configuration manager instance"""
    return ConfigManager(environment) 