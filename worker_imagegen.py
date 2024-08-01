import os
import shutil
import subprocess
import yaml
import re
import sys

# Function to clone a repository from a given URL to a specified destination
def clone_repo(repo_url, destination):
    print(f"Cloning repository from {repo_url} to {destination}...")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    subprocess.run(['git', 'clone', repo_url, destination])
    print("Repository cloned successfully.")

# Function to convert config to env
def convert_config_to_env():
    print("Converting config to environment variables...")
    subprocess.run(['python3', 'convert_config_to_env.py'])
    print("Config conversion complete.")

# Function to detect CUDA version
def detect_cuda_version():
    print("Detecting CUDA version...")
    try:
        output = subprocess.check_output(['nvidia-smi']).decode('utf-8')
        match = re.search(r"CUDA Version: (\d+\.\d+)", output)
        return match.group(1) if match else None
    except Exception as e:
        print("Error detecting CUDA version:", e)
        return None

# Function to build a Docker image
def build_docker_image(cuda_version):
    print("Building Docker image...")
    supported_versions = ["12.1", "12.2", "12.3"]
    if cuda_version in supported_versions:
        cuda_major_version = cuda_version.split('.')[0]
        dockerfile_found = False
        for filename in os.listdir("Dockerfiles"):
            if f"Dockerfile.{cuda_major_version}" in filename:
                dockerfile_name = filename
                dockerfile_found = True
                break

        if not dockerfile_found:
            print("Error: No compatible Dockerfile found for the detected CUDA version.")
            sys.exit(1)  # Exit the script with status code 1
    else:
        print("Error: Detected CUDA version is not supported. Please install CUDA 12.1, 12.2, or 12.3.")
        sys.exit(1)  # Exit the script with status code 1

    subprocess.run(['docker', 'build', '-t', config['worker_config']['image_name'], '-f', f'Dockerfiles/{dockerfile_name}', '.'])
    print("Docker image built successfully.")

# Function to run a Docker container
def run_docker_container(exec_type, ports, gpus, env_file, container_name, image_name, **kwargs):
    print(f"Running Docker container {container_name}...")
    command = ['docker', 'run', '--gpus', gpus, '-p', ports, '--env-file', env_file,  '--name', container_name]

    if exec_type:
        command.insert(2, '-'+exec_type)

    command.append(image_name)

    command_str = ' '.join(command)
    print(f"Running command: {command_str}")

    subprocess.run(command_str, shell=True)
    print("Docker container is running.")

if __name__ == "__main__":
    print('''
           _____ _____   _____         _____            _    _       _     
     /\   |_   _|  __ \ / ____|       / ____|          | |  | |     | |    
    /  \    | | | |__) | |  __ ______| |  __  ___ _ __ | |__| |_   _| |__  
   / /\ \   | | |  ___/| | |_ |______| | |_ |/ _ \ '_ \|  __  | | | | '_ \ 
  / ____ \ _| |_| |    | |__| |      | |__| |  __/ | | | |  | | |_| | |_) |
 /_/    \_\_____|_|     \_____|       \_____|\___|_| |_|_|  |_|\__,_|_.__/ 

    ''')
    print("Centralized repository for AI Power Grid Workers")
    print("Location: United States of America / Web: aipowergrid.io / X: @AIPowerGrid / e-mail: admin@aipowergrid.io\n")

    # Detect CUDA version
    cuda_version = detect_cuda_version()
    if cuda_version:
        print(f"Detected CUDA version: {cuda_version}")
    else:
        print("Error detecting CUDA version. Please make sure NVIDIA drivers are installed.")
        sys.exit(1)  # Exit the script with status code 1

    # Loading configurations from config.yaml
    print("Loading configuration from config-imagegen.yaml...")
    with open('config-imagegen.yaml') as file:
        config = yaml.safe_load(file)
    print("Configuration loaded.")

    # Cloning repositories from GitHub
    clone_repo("https://github.com/gonner22/image-worker", "image-worker")

    # Checking for existence of bridgeData.yaml
    if not os.path.exists("bridgeData.yaml"):
        print("Error: bridgeData.yaml not found!")
        print("Please copy bridgeData_imagegen_template.yaml file with the name bridgeData.yaml in the root directory including your configurations.")
        sys.exit(1)  # Exit the script with status code 1

    # Copying bridgeData.yaml to image-worker directory
    print("Copying bridgeData.yaml to image-worker directory...")
    shutil.copy("bridgeData.yaml", "image-worker")
    print("bridgeData.yaml copied successfully.")

    # Changing directory to image-worker
    print("Changing directory to image-worker...")
    os.chdir("image-worker")

    # Convert config to env
    convert_config_to_env()

    # Building worker Docker image
    build_docker_image(cuda_version)

    # Running worker Docker container
    run_docker_container(**config['worker_config'], env_file=config['worker_config']['env-file'])
