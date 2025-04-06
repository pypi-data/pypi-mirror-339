import boto3
from app.config import AWS_CONFIG, EMR_CONFIG

# Initialize Boto3 EMR client
emr_client = boto3.client(
    'emr', 
    aws_access_key_id=AWS_CONFIG['ACCESS_KEY'],
    aws_secret_access_key=AWS_CONFIG['SECRET_KEY'],
    region_name=AWS_CONFIG['REGION']
)

def create_step_config(job, deploy_mode):
    """Create the configuration for an EMR step."""
    deploy_mode_arg = "--deploy-mode cluster" if deploy_mode == 'cluster' else ""

    return {
        'Name': job,
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'bash',
                '-c',
                f'cd /home/hadoop/ && '
                f'aws s3 cp {EMR_CONFIG["S3_PATH"]}/{job}/job_package.zip /home/hadoop/{job}/job_package.zip && '
                f'cd /home/hadoop/{job} && '
                f'unzip -o job_package.zip && '
                'spark-submit '
                '--conf spark.pyspark.python=/home/hadoop/myenv/bin/python '
                f'{deploy_mode_arg} '
                '--py-files job_package.zip '
                'main.py'
            ]
        }
    }

def start_emr_job(job, deploy_mode='client'):
    """
    Start an EMR job.
    
    Args:
        job (str): Name of the job
        deploy_mode (str): Deployment mode ('client' or 'cluster')
    """
    step_config = create_step_config(job, deploy_mode)
    response = emr_client.add_job_flow_steps(
        JobFlowId=EMR_CONFIG['CLUSTER_ID'],
        Steps=[step_config]
    )
    print(f"{job} job started in {deploy_mode} mode!")
    return response['StepIds'][0]