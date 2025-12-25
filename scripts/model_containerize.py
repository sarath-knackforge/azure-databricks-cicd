import mlflow.sagemaker
import os
import argparse
from pyspark.sql import SparkSession
from pyspark.dbutils import DBUtils

spark = SparkSession.builder.getOrCreate()
dbutils = DBUtils(spark)

# Parse arguments to get the model name
parser = argparse.ArgumentParser()
parser.add_argument("--model_name", required=True)
args = parser.parse_args()

# 1. Securely get AWS credentials from Databricks Secrets
# Ensure you have created this scope and these keys in Databricks
access_key = dbutils.secrets.get(scope="aws-secrets", key="access-key")
secret_key = dbutils.secrets.get(scope="aws-secrets", key="secret-key")

# 2. Set environment for AWS CLI
os.environ["AWS_ACCESS_KEY_ID"] = access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = secret_key
os.environ["AWS_DEFAULT_REGION"] = "us-east-1" # Update to your region

# 3. Define URI using Unity Catalog format
# Use the @latest alias or the specific version from your previous tasks
model_uri = f"models:/{args.model_name}/latest"
# Replace 123456789012 with your AWS Account ID
image_uri = f"123456789012.dkr.ecr.us-east-1.amazonaws.com"

print(f"Starting containerization for {model_uri}...")

# 4. Build and Push to ECR
mlflow.sagemaker.build_and_push_container(
    model_uri=model_uri,
    image_uri=image_uri
)

print("Successfully pushed container to ECR.")
