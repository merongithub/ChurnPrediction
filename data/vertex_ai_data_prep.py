#!/usr/bin/env python3
"""
Vertex AI Data Preparation Pipeline for Churn Prediction
This script loads, cleans, and prepares customer churn data for Vertex AI services.

What this script does:
1. Downloads and loads customer churn dataset
2. Cleans and preprocesses the data
3. Performs feature engineering (encoding, transformations)
4. Uploads cleaned data to Google Cloud Storage
5. Ingests features into Vertex AI Feature Store
6. Provides data quality reports and validation

Usage:
    python data/vertex_ai_data_prep.py
"""

import pandas as pd
import numpy as np
from google.cloud import storage, aiplatform
from datetime import datetime
import os
import sys
import logging
from typing import Dict, Any, Optional

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_prep.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataPreparationPipeline:
    """Data preparation pipeline for Vertex AI churn prediction"""
    
    def __init__(self):
        """Initialize the data preparation pipeline"""
        self.config = get_config()
        self.secrets = self.config.secrets
        
        # Initialize Google Cloud clients
        self._init_gcp_clients()
        
        # Data URLs and paths
        self.data_url = "https://raw.githubusercontent.com/dphi-official/Datasets/master/Telco-Customer-Churn.csv"
        self.local_data_path = "data/raw_telco_data.csv"
        self.cleaned_data_path = "data/cleaned_telco_data.csv"
        self.gcs_data_path = f"data/churn/cleaned_telco_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Feature engineering configuration
        self.categorical_columns = [
            "gender", "Partner", "Dependents", "PhoneService", "MultipleLines",
            "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
            "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
            "PaperlessBilling", "PaymentMethod"
        ]
        
        self.numeric_columns = ["tenure", "MonthlyCharges", "TotalCharges"]
        self.target_column = "Churn"
        self.id_column = "customerID"
    
    def _init_gcp_clients(self):
        """Initialize Google Cloud clients"""
        try:
            # Initialize Vertex AI
            aiplatform.init(
                project=self.secrets.GCP_PROJECT_ID,
                location=self.secrets.GCP_LOCATION
            )
            
            # Initialize Cloud Storage client
            self.storage_client = storage.Client()
            self.bucket = self.storage_client.bucket(self.secrets.GCS_BUCKET_NAME)
            
            logger.info("Google Cloud clients initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud clients: {e}")
            raise
    
    def load_data(self) -> pd.DataFrame:
        """Load data from URL or local file"""
        logger.info("Loading customer churn dataset...")
        
        try:
            # Try to load from URL first
            df = pd.read_csv(self.data_url)
            logger.info(f"Loaded {len(df)} records from URL")
            
            # Save raw data locally
            os.makedirs("data", exist_ok=True)
            df.to_csv(self.local_data_path, index=False)
            logger.info(f"Saved raw data to {self.local_data_path}")
            
        except Exception as e:
            logger.warning(f"Failed to load from URL: {e}")
            
            # Try to load from local file
            if os.path.exists(self.local_data_path):
                df = pd.read_csv(self.local_data_path)
                logger.info(f"Loaded {len(df)} records from local file")
            else:
                raise FileNotFoundError("No data source available")
        
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the data"""
        logger.info("Cleaning and preprocessing data...")
        
        initial_rows = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_rows - len(df)} duplicate rows")
        
        # Handle missing values
        missing_before = df.isnull().sum().sum()
        df = df.dropna()
        missing_after = df.isnull().sum().sum()
        logger.info(f"Removed {missing_before - missing_after} missing values")
        
        # Convert data types
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
        df = df.dropna()  # Remove rows with conversion errors
        
        # Map target variable
        df[self.target_column] = df[self.target_column].map({"Yes": 1, "No": 0})
        
        # Validate target distribution
        target_dist = df[self.target_column].value_counts()
        logger.info(f"Target distribution: {target_dist.to_dict()}")
        
        logger.info(f"Data cleaning completed. Final dataset: {len(df)} rows")
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform feature engineering"""
        logger.info("Performing feature engineering...")
        
        # Create new features
        df['TotalChargesPerMonth'] = df['TotalCharges'] / df['tenure']
        df['MonthlyChargesRatio'] = df['MonthlyCharges'] / df['TotalCharges']
        
        # Encode categorical variables
        df_encoded = pd.get_dummies(df, columns=self.categorical_columns, drop_first=True)
        
        # Log feature information
        logger.info(f"Original features: {len(df.columns)}")
        logger.info(f"Features after encoding: {len(df_encoded.columns)}")
        logger.info(f"New engineered features: TotalChargesPerMonth, MonthlyChargesRatio")
        
        return df_encoded
    
    def validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data quality and generate reports"""
        logger.info("Validating data quality...")
        
        validation_report = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": df.isnull().sum().sum(),
            "duplicate_rows": df.duplicated().sum(),
            "target_distribution": df[self.target_column].value_counts().to_dict(),
            "numeric_features": len(df.select_dtypes(include=[np.number]).columns),
            "categorical_features": len(df.select_dtypes(include=['object']).columns),
            "data_types": df.dtypes.to_dict()
        }
        
        # Check for data quality issues
        issues = []
        if validation_report["missing_values"] > 0:
            issues.append("Missing values detected")
        if validation_report["duplicate_rows"] > 0:
            issues.append("Duplicate rows detected")
        if validation_report["target_distribution"][1] < 100:
            issues.append("Low positive class count")
        
        validation_report["issues"] = issues
        
        logger.info("Data validation completed")
        logger.info(f"Validation report: {validation_report}")
        
        return validation_report
    
    def upload_to_gcs(self, df: pd.DataFrame) -> str:
        """Upload cleaned data to Google Cloud Storage"""
        logger.info("Uploading data to Google Cloud Storage...")
        
        try:
            # Save cleaned data locally first
            os.makedirs("data", exist_ok=True)
            df.to_csv(self.cleaned_data_path, index=False)
            
            # Upload to GCS
            blob = self.bucket.blob(self.gcs_data_path)
            blob.upload_from_filename(self.cleaned_data_path)
            
            gcs_uri = f"gs://{self.secrets.GCS_BUCKET_NAME}/{self.gcs_data_path}"
            logger.info(f"Data uploaded to GCS: {gcs_uri}")
            
            return gcs_uri
            
        except Exception as e:
            logger.error(f"Failed to upload to GCS: {e}")
            raise
    
    def ingest_to_feature_store(self, df: pd.DataFrame) -> bool:
        """Ingest features into Vertex AI Feature Store"""
        logger.info("Ingesting features into Vertex AI Feature Store...")
        
        try:
            # Get or create feature store
            try:
                featurestore = aiplatform.Featurestore(self.secrets.FEATURE_STORE_ID)
                logger.info(f"Using existing feature store: {self.secrets.FEATURE_STORE_ID}")
            except Exception:
                featurestore = aiplatform.Featurestore.create(
                    featurestore_id=self.secrets.FEATURE_STORE_ID
                )
                logger.info(f"Created new feature store: {self.secrets.FEATURE_STORE_ID}")
            
            # Get or create entity type
            try:
                entity_type = featurestore.get_entity_type(self.secrets.ENTITY_TYPE_ID)
                logger.info(f"Using existing entity type: {self.secrets.ENTITY_TYPE_ID}")
            except Exception:
                entity_type = featurestore.create_entity_type(
                    entity_type_id=self.secrets.ENTITY_TYPE_ID
                )
                logger.info(f"Created new entity type: {self.secrets.ENTITY_TYPE_ID}")
            
            # Prepare features (exclude ID and target columns)
            feature_columns = [col for col in df.columns if col not in [self.id_column, self.target_column]]
            
            # Ingest features
            entity_type.ingest_from_df(
                feature_ids=feature_columns,
                feature_time=datetime.now(),
                feature_values=df,
                entity_id_column=self.id_column,
            )
            
            logger.info(f"Ingested {len(feature_columns)} features into feature store")
            return True
            
        except Exception as e:
            logger.error(f"Failed to ingest to feature store: {e}")
            return False
    
    def run_pipeline(self) -> Dict[str, Any]:
        """Run the complete data preparation pipeline"""
        logger.info("Starting data preparation pipeline...")
        
        try:
            # Step 1: Load data
            df = self.load_data()
            
            # Step 2: Clean data
            df_cleaned = self.clean_data(df)
            
            # Step 3: Engineer features
            df_engineered = self.engineer_features(df_cleaned)
            
            # Step 4: Validate data
            validation_report = self.validate_data(df_engineered)
            
            # Step 5: Upload to GCS
            gcs_uri = self.upload_to_gcs(df_engineered)
            
            # Step 6: Ingest to Feature Store
            feature_store_success = self.ingest_to_feature_store(df_engineered)
            
            # Prepare results
            results = {
                "success": True,
                "data_shape": df_engineered.shape,
                "gcs_uri": gcs_uri,
                "feature_store_success": feature_store_success,
                "validation_report": validation_report,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("Data preparation pipeline completed successfully!")
            logger.info(f"Results: {results}")
            
            return results
            
        except Exception as e:
            logger.error(f"Data preparation pipeline failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

def main():
    """Main function to run the data preparation pipeline"""
    print("🚀 Starting Vertex AI Data Preparation Pipeline")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = DataPreparationPipeline()
    
    # Run pipeline
    results = pipeline.run_pipeline()
    
    # Print summary
    print("\n📊 Pipeline Results:")
    print("=" * 30)
    
    if results["success"]:
        print(f"✅ Pipeline completed successfully!")
        print(f"📈 Data shape: {results['data_shape']}")
        print(f"☁️  GCS URI: {results['gcs_uri']}")
        print(f"🏪 Feature Store: {'✅ Success' if results['feature_store_success'] else '❌ Failed'}")
        
        # Print validation summary
        validation = results["validation_report"]
        print(f"🔍 Validation:")
        print(f"   - Total rows: {validation['total_rows']}")
        print(f"   - Total columns: {validation['total_columns']}")
        print(f"   - Target distribution: {validation['target_distribution']}")
        
        if validation["issues"]:
            print(f"   - Issues: {', '.join(validation['issues'])}")
        else:
            print(f"   - ✅ No data quality issues detected")
            
    else:
        print(f"❌ Pipeline failed: {results['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
