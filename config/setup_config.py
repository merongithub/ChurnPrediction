#!/usr/bin/env python3
"""
Configuration Setup Script for Churn Prediction Project
This script helps users set up their configuration with custom values.
"""

import os
import json
from typing import Dict, Any
from .secrets import Secrets, DevelopmentSecrets, StagingSecrets, ProductionSecrets

def get_user_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default value"""
    if default:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def setup_environment_config(environment: str) -> Dict[str, Any]:
    """Set up configuration for a specific environment"""
    print(f"\n=== Setting up {environment.upper()} environment ===")
    
    config = {}
    
    # GCP Configuration
    config['GCP_PROJECT_ID'] = get_user_input(
        "Enter your GCP Project ID",
        f"{environment}-churn-prediction-project"
    )
    
    config['GCP_LOCATION'] = get_user_input(
        "Enter your GCP Location/Region",
        "us-central1"
    )
    
    # Storage Configuration
    config['GCS_BUCKET_NAME'] = get_user_input(
        "Enter your GCS Bucket Name",
        f"{environment}-churn-prediction-bucket"
    )
    
    # Container Registry Configuration
    config['CONTAINER_REGISTRY_PROJECT'] = get_user_input(
        "Enter your Container Registry Project ID",
        config['GCP_PROJECT_ID']
    )
    
    # Feature Store Configuration
    config['FEATURE_STORE_ID'] = get_user_input(
        "Enter your Feature Store ID",
        "churn_featurestore"
    )
    
    # Model Configuration
    config['MODEL_DISPLAY_NAME'] = get_user_input(
        "Enter your Model Display Name",
        "churn_model"
    )
    
    return config

def create_custom_secrets_class(environment: str, config: Dict[str, Any]) -> type:
    """Create a custom secrets class with user-provided values"""
    
    class CustomSecrets(Secrets):
        """Custom secrets class for user configuration"""
        
        # Override default values with user input
        GCP_PROJECT_ID = config.get('GCP_PROJECT_ID', Secrets.GCP_PROJECT_ID)
        GCP_LOCATION = config.get('GCP_LOCATION', Secrets.GCP_LOCATION)
        GCS_BUCKET_NAME = config.get('GCS_BUCKET_NAME', Secrets.GCS_BUCKET_NAME)
        CONTAINER_REGISTRY_PROJECT = config.get('CONTAINER_REGISTRY_PROJECT', Secrets.CONTAINER_REGISTRY_PROJECT)
        FEATURE_STORE_ID = config.get('FEATURE_STORE_ID', Secrets.FEATURE_STORE_ID)
        MODEL_DISPLAY_NAME = config.get('MODEL_DISPLAY_NAME', Secrets.MODEL_DISPLAY_NAME)
        
        # Update derived values
        VERTEX_AI_PROJECT = GCP_PROJECT_ID
        VERTEX_AI_LOCATION = GCP_LOCATION
        MODEL_ARTIFACT_URI = f"gs://{GCS_BUCKET_NAME}/models/churn_model.joblib"
    
    return CustomSecrets

def save_config_to_file(config: Dict[str, Any], filepath: str):
    """Save configuration to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Configuration saved to: {filepath}")
    except Exception as e:
        print(f"Error saving configuration: {e}")

def main():
    """Main configuration setup function"""
    print("Churn Prediction Project - Configuration Setup")
    print("=" * 50)
    
    # Ask user which environment to configure
    print("\nAvailable environments:")
    print("1. Development")
    print("2. Staging") 
    print("3. Production")
    print("4. All environments")
    
    choice = input("\nSelect environment to configure (1-4): ").strip()
    
    environments = []
    if choice == "1":
        environments = ["development"]
    elif choice == "2":
        environments = ["staging"]
    elif choice == "3":
        environments = ["production"]
    elif choice == "4":
        environments = ["development", "staging", "production"]
    else:
        print("Invalid choice. Exiting.")
        return
    
    # Create config directory if it doesn't exist
    config_dir = os.path.join(os.path.dirname(__file__), "user_configs")
    os.makedirs(config_dir, exist_ok=True)
    
    # Set up each environment
    for env in environments:
        config = setup_environment_config(env)
        
        # Save configuration to file
        config_file = os.path.join(config_dir, f"{env}_config.json")
        save_config_to_file(config, config_file)
        
        # Create custom secrets class
        CustomSecrets = create_custom_secrets_class(env, config)
        
        # Save custom secrets class to file
        secrets_file = os.path.join(config_dir, f"{env}_secrets.py")
        with open(secrets_file, 'w') as f:
            f.write(f"# Custom secrets for {env} environment\n")
            f.write("from ..secrets import Secrets\n\n")
            f.write("class CustomSecrets(Secrets):\n")
            for key, value in config.items():
                if isinstance(value, str):
                    f.write(f"    {key} = \"{value}\"\n")
                else:
                    f.write(f"    {key} = {value}\n")
        
        print(f"\n{env.capitalize()} environment configuration completed!")
    
    print("\nConfiguration setup completed successfully!")
    print("\nNext steps:")
    print("1. Update your .env file with the new values")
    print("2. Set the ENVIRONMENT variable to your desired environment")
    print("3. Run your scripts with the new configuration")

if __name__ == "__main__":
    main() 