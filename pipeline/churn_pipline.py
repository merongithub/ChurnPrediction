import kfp
from kfp import dsl
from kfp.v2 import compiler
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_config

@dsl.pipeline(
    name="churn-pipeline",
    description="A pipeline to train churn model"
)
def churn_pipeline():
    # Get configuration
    config = get_config()
    secrets = config.secrets
    container_config = secrets.get_container_config()
    
    # Create feature store step
    ingest = dsl.ContainerOp(
        name="create-feature-store",
        image=container_config["full_image_path"],
        command=["python", "create_features.py"]
    )

    # Train model step
    train = dsl.ContainerOp(
        name="train-model",
        image=container_config["full_image_path"],
        command=["python", "train_custom.py"]
    )
    train.after(ingest)

# Compile pipeline
compiler.Compiler().compile(
    pipeline_func=churn_pipeline,
    package_path=secrets.PIPELINE_PACKAGE_PATH
)