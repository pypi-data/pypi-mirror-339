import os
from dotenv import load_dotenv

load_dotenv()

AWS_CONFIG = {
    'ACCESS_KEY': os.getenv('AWS_ACCESS_KEY_ID'),
    'SECRET_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'REGION': os.getenv('AWS_REGION')
}

EMR_CONFIG = {
    'CLUSTER_ID': os.getenv('EMR_CLUSTER_ID'),
    'S3_PATH': os.getenv('S3_PATH')
}
