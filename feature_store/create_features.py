from google.cloud import aiplatform
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_config

def create_featurestore():
    # Get configuration
    config = get_config()
    secrets = config.secrets
    
    # Initialize Vertex AI
    aiplatform.init(
        project=secrets.GCP_PROJECT_ID, 
        location=secrets.GCP_LOCATION
    )

    # Create feature store
    featurestore = aiplatform.Featurestore.create(
        featurestore_id=secrets.FEATURE_STORE_ID
    )

    # Create entity type
    entity_type = featurestore.create_entity_type(
        entity_type_id=secrets.ENTITY_TYPE_ID
    )

    # Create features
    entity_type.create_feature(
        feature_id="tenure",
        value_type="DOUBLE",
        description="Customer tenure"
    )
    entity_type.create_feature(
        feature_id="monthly_charges",
        value_type="DOUBLE"
    )

    print("Feature Store and Features created successfully")

if __name__ == "__main__":
    create_featurestore()