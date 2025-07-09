#!/usr/bin/env python3
"""
Example Usage of Vertex AI Data Preparation Pipeline
This script demonstrates how to use the data preparation pipeline with different configurations.
"""

import sys
import os
from vertex_ai_data_prep import DataPreparationPipeline

def example_basic_usage():
    """Basic usage example"""
    print("📚 Example 1: Basic Data Preparation")
    print("-" * 40)
    
    # Initialize pipeline
    pipeline = DataPreparationPipeline()
    
    # Run the complete pipeline
    results = pipeline.run_pipeline()
    
    if results["success"]:
        print("✅ Basic pipeline completed successfully!")
        print(f"📊 Dataset shape: {results['data_shape']}")
        print(f"☁️  Data uploaded to: {results['gcs_uri']}")
    else:
        print(f"❌ Pipeline failed: {results['error']}")

def example_custom_configuration():
    """Example with custom configuration"""
    print("\n📚 Example 2: Custom Configuration")
    print("-" * 40)
    
    # Initialize pipeline
    pipeline = DataPreparationPipeline()
    
    # Customize the pipeline
    pipeline.data_url = "https://your-custom-dataset-url.csv"
    pipeline.gcs_data_path = "data/custom/churn_data_custom.csv"
    
    # Run only specific steps
    print("🔄 Running custom pipeline steps...")
    
    # Step 1: Load data
    df = pipeline.load_data()
    print(f"📥 Loaded {len(df)} records")
    
    # Step 2: Clean data
    df_cleaned = pipeline.clean_data(df)
    print(f"🧹 Cleaned data: {len(df_cleaned)} records")
    
    # Step 3: Engineer features
    df_engineered = pipeline.engineer_features(df_cleaned)
    print(f"⚙️  Engineered features: {len(df_engineered.columns)} columns")
    
    # Step 4: Validate data
    validation = pipeline.validate_data(df_engineered)
    print(f"🔍 Validation: {validation['total_rows']} rows, {validation['total_columns']} columns")

def example_data_quality_check():
    """Example focusing on data quality validation"""
    print("\n📚 Example 3: Data Quality Check")
    print("-" * 40)
    
    pipeline = DataPreparationPipeline()
    
    # Load and clean data
    df = pipeline.load_data()
    df_cleaned = pipeline.clean_data(df)
    df_engineered = pipeline.engineer_features(df_cleaned)
    
    # Detailed validation
    validation = pipeline.validate_data(df_engineered)
    
    print("📊 Data Quality Report:")
    print(f"   • Total Records: {validation['total_rows']:,}")
    print(f"   • Total Features: {validation['total_columns']}")
    print(f"   • Missing Values: {validation['missing_values']}")
    print(f"   • Duplicate Rows: {validation['duplicate_rows']}")
    print(f"   • Target Distribution: {validation['target_distribution']}")
    
    if validation['issues']:
        print(f"   ⚠️  Issues Found: {', '.join(validation['issues'])}")
    else:
        print("   ✅ No data quality issues detected")

def example_feature_store_only():
    """Example focusing only on feature store ingestion"""
    print("\n📚 Example 4: Feature Store Ingestion Only")
    print("-" * 40)
    
    pipeline = DataPreparationPipeline()
    
    # Load and prepare data
    df = pipeline.load_data()
    df_cleaned = pipeline.clean_data(df)
    df_engineered = pipeline.engineer_features(df_cleaned)
    
    # Ingest to feature store only
    success = pipeline.ingest_to_feature_store(df_engineered)
    
    if success:
        print("✅ Features successfully ingested to Vertex AI Feature Store")
        print(f"📈 Ingested {len(df_engineered.columns) - 2} features")  # Exclude ID and target
    else:
        print("❌ Feature store ingestion failed")

def example_error_handling():
    """Example demonstrating error handling"""
    print("\n📚 Example 5: Error Handling")
    print("-" * 40)
    
    try:
        pipeline = DataPreparationPipeline()
        
        # Simulate an error by using an invalid URL
        pipeline.data_url = "https://invalid-url-that-does-not-exist.csv"
        
        # This should fail gracefully
        df = pipeline.load_data()
        
    except FileNotFoundError as e:
        print(f"✅ Error handled correctly: {e}")
        print("🔄 Falling back to local file...")
        
        # Try with local file
        if os.path.exists("data/raw_telco_data.csv"):
            pipeline.data_url = "data/raw_telco_data.csv"
            df = pipeline.load_data()
            print("✅ Successfully loaded from local file")
        else:
            print("❌ No local backup file available")

def main():
    """Run all examples"""
    print("🚀 Vertex AI Data Preparation Pipeline Examples")
    print("=" * 60)
    
    # Check if configuration is set up
    try:
        from config import get_config
        config = get_config()
        print(f"✅ Using configuration for environment: {config.environment}")
        print(f"   • GCP Project: {config.secrets.GCP_PROJECT_ID}")
        print(f"   • GCS Bucket: {config.secrets.GCS_BUCKET_NAME}")
        print(f"   • Feature Store: {config.secrets.FEATURE_STORE_ID}")
    except Exception as e:
        print(f"⚠️  Configuration issue: {e}")
        print("   Please run: python -m config.setup_config")
        return
    
    # Run examples
    try:
        example_basic_usage()
        example_custom_configuration()
        example_data_quality_check()
        example_feature_store_only()
        example_error_handling()
        
        print("\n🎉 All examples completed!")
        print("\n💡 Tips:")
        print("   • Check the logs in 'data_prep.log' for detailed information")
        print("   • Use the validation report to assess data quality")
        print("   • Monitor your GCS bucket for uploaded files")
        print("   • Check Vertex AI Feature Store for ingested features")
        
    except KeyboardInterrupt:
        print("\n⏹️  Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

if __name__ == "__main__":
    main() 