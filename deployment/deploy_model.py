from google.cloud import aiplatform
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_config

def deploy_model():
    # Get configuration
    config = get_config()
    secrets = config.secrets
    
    # Initialize Vertex AI
    aiplatform.init(
        project=secrets.GCP_PROJECT_ID, 
        location=secrets.GCP_LOCATION
    )
    
    # Upload model
    model = aiplatform.Model.upload(
        display_name=secrets.MODEL_DISPLAY_NAME,
        artifact_uri=secrets.MODEL_ARTIFACT_URI,
        serving_container_image_uri=secrets.SERVING_CONTAINER_IMAGE
    )
    
    # Deploy model
    endpoint = model.deploy(machine_type=secrets.MACHINE_TYPE)
    print(f"Model deployed to endpoint: {endpoint.name}")

if __name__ == "__main__":
    deploy_model()