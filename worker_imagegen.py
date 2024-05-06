# Importing necessary modules
import os
import shutil
import subprocess
import yaml

# Function to clone a repository from a given URL to a specified destination
def clone_repo(repo_url, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    subprocess.run(['git', 'clone', repo_url, destination])

# Function to convert config to env
def convert_config_to_env():
    subprocess.run(['python3', 'convert_config_to_env.py'])

# Function to build a Docker image
def build_docker_image():
    subprocess.run(['docker', 'build', '-t', config['worker_config']['image_name'], '-f', 'Dockerfiles/Dockerfile.12.3.2-22.04', '.'])

# Function to run a Docker container
def run_docker_container(exec_type, ports, gpus, env_file, container_name, image_name, **kwargs):
    command = ['docker', 'run', '--gpus', gpus, '-p', ports, '--env-file', env_file,  '--name', container_name]

    if exec_type:
        command.insert(2, '-'+exec_type)

    command.append(image_name)

    command_str = ' '.join(command)

    print(command_str)  # Print the final Docker command

    subprocess.run(command_str, shell=True)

if __name__ == "__main__":
    # ASCII Art
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

    # Loading configurations from config.yaml
    with open('config-imagegen.yaml') as file:
        config = yaml.safe_load(file)

    # Cloning repositories from GitHub
    clone_repo("https://github.com/gonner22/image-worker", "image-worker")

    # Checking for existence of bridgeData.yaml
    if not os.path.exists("bridgeData.yaml"):
        print("Error: bridgeData.yaml not found!")
        print("Please copy bridgeData_imagegen_template.yaml file with the name bridgeData.yaml in the root directory including your configurations.")
        exit(1)

    # Copying bridgeData.yaml to grid-image-worker directory
    shutil.copy("bridgeData.yaml", "image-worker")

    # Changing directory to grid-text-worker
    os.chdir("image-worker")

    # Convert config to env
    convert_config_to_env()

    # Building worker Docker image
    build_docker_image()

    # Running worker Docker container
    run_docker_container(**config['worker_config'], env_file=config['worker_config']['env-file'])

