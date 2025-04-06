# EMRRunner

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![Amazon EMR](https://img.shields.io/badge/Amazon%20EMR-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

A powerful command-line tool for managing and deploying Python-based (e.g., PySpark) data pipeline jobs on Amazon EMR clusters.

## 🚀 Features

- Command-line interface for quick job submission
- Basic POST API for fast job submission
- Support for both client and cluster deploy modes

## 📋 Prerequisites

- Python 3.9+
- AWS Account with EMR access
- Configured AWS credentials
- Active EMR cluster

## 🛠️ Installation

### From PyPI
```bash
pip install emrrunner
```

### From Source
```bash
# Clone the repository
git clone https://github.com/Haabiy/EMRRunner.git && cd EMRRunner

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install the package
pip install -e .
```

## ⚙️ Configuration

### AWS Configuration

Create a `.env` file in the project root with your AWS configuration or export these variables in your terminal before running:
```Bash
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_REGION="your_region"
export EMR_CLUSTER_ID="your_cluster_id"
export S3_PATH="s3://your-bucket/path" # The path to your jobs (the directory containing your job_package.zip file)...see `S3 Job Structure` below
```

or a better approach — instead of exporting these variables in each terminal session, you can add them permanently to your terminal by editing your `~/.zshrc` file:
1. Open your `~/.zshrc` file:
   ```bash
   nano ~/.zshrc
   ```
2. Add the following lines at the end of the file (replace with your own AWS credentials):
   ```bash
   export AWS_ACCESS_KEY_ID="your_access_key"
   export AWS_SECRET_ACCESS_KEY="your_secret_key"
   export AWS_REGION="your_region"
   export EMR_CLUSTER_ID="your_cluster_id"
   export S3_PATH="s3://your-bucket/path"
   ```
3. Save and exit the file (`Ctrl + X`).
4. To apply the changes immediately, run:
   ```bash
   source ~/.zshrc
   ```

Now, you won’t have to export the variables manually in each session, and they’ll be available whenever you open a new terminal session.

--- 


### Bootstrap Actions
For EMR cluster setup with required dependencies, create a bootstrap script (e.g.: `bootstrap.sh`);

```bash
#!/bin/bash -xe

# Example structure of a bootstrap script
# Create and activate virtual environment
python3 -m venv /home/hadoop/myenv
source /home/hadoop/myenv/bin/activate

# Install system dependencies
sudo yum install python3-pip -y
sudo yum install -y [your-system-packages]

# Install Python packages
pip3 install [your-required-packages]

deactivate
```

E.g
```bash
#!/bin/bash -xe

# Create and activate a virtual environment
python3 -m venv /home/hadoop/myenv
source /home/hadoop/myenv/bin/activate

# Install pip for Python 3.x
sudo yum install python3-pip -y

# Install required packages
pip3 install \
    pyspark==3.5.5 \

deactivate
```

Upload the bootstrap script to S3 and reference it in your EMR cluster configuration.

## 📁 Project Structure

```
EMRRunner/
├── Dockerfile
├── LICENSE.md
├── README.md
├── app/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── emr_client.py       # EMR interaction logic
│   ├── emr_job_api.py      # Flask API endpoints
│   ├── run_api.py          # API server runner
│   └── schema.py           # Request/Response schemas
├── bootstrap/
│   └── bootstrap.sh        # EMR bootstrap script
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_emr_job_api.py
│   └── test_schema.py
├── pyproject.toml
├── requirements.txt
└── setup.py
```

## 📦 S3 Job Structure

The `S3_PATH` in your configuration should point to a bucket with the following structure:

```
s3://your-bucket/
├── jobs/
│   ├── job1/
│   │   ├── job_package.zip  # Include shared functions and utilities, make sure your main script is named `main.py`, and name your zip file `job_package.zip`.
│   └── job2/
│   │   ├── job_package.zip  # Include shared functions and utilities, make sure your main script is named `main.py`, and name your zip file `job_package.zip`.
```

### Job Script (`main.py`)

Your job script should include the necessary logic for executing the tasks in your data pipeline, using functions from your dependencies.

Example of `main.py`:

```python
from dependencies import clean, transform, sink  # Import your core job functions

def main():
    # Step 1: Clean the data
    clean()

    # Step 2: Transform the data
    transform()

    # Step 3: Sink (store) the processed data
    sink()

if __name__ == "__main__":
    main()  # Execute the main function when the script is run
```


## 💻 Usage

### Command Line Interface

Start a job in client mode:
```bash
emrrunner start --job job1
```

Start a job in cluster mode:
```bash
emrrunner start --job job1 --deploy-mode cluster
```

### API Endpoints

Start a job via API in client mode (default):
```bash
curl -X POST http://localhost:8000/emrrunner/start \
     -H "Content-Type: application/json" \
     -d '{"job": "job1"}'
```

Start a job via API in cluster mode:
```bash
curl -X POST http://localhost:8000/emrrunner/start \
     -H "Content-Type: application/json" \
     -d '{"job": "job1", "deploy_mode": "cluster"}'
```

## 🔧 Development

To contribute to EMRRunner:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 💡 Best Practices

1. **Bootstrap Actions**
   - Keep bootstrap scripts modular
   - Version control your dependencies
   - Use specific package versions
   - Test bootstrap scripts locally when possible
   - Store bootstrap scripts in S3 with versioning enabled

2. **Job Dependencies**
   - Maintain a requirements.txt for each job
   - Document system-level dependencies
   - Test dependencies in a clean environment

3. **Job Organization**
   - Follow the standard structure for jobs
   - Use clear naming conventions
   - Document all functions and modules

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Bug Reports

If you discover any bugs, please create an issue on GitHub with:
- Any details about your local setup that might be helpful in troubleshooting
- Detailed steps to reproduce the bug

---

Built with ❤️ using Python and AWS EMR