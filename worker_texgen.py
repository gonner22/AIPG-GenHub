# ************************************* AIPG-GenHub    MIT 2024 **********************************************************************
# Centralized AI Worker Repository Automation
#
# This script automates the setup process for a centralized repository handling AI worker and generators.
# It includes functionality to clone repositories from GitHub, create Docker networks, build Docker images, and run Docker containers.
#
#************************************************************************************************************************************

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

# Function to build a Docker image
def build_docker_image():
    subprocess.run(['docker', 'build', '-t', config['worker_config']['image_name'], '.'])

# Function to run a Docker container
def run_docker_container(exec_type, ports, network, container_name, image_name, **kwargs):
    command = ['docker', 'run', '-d', '-p', ports, '--network', network, '--name', container_name]

    if exec_type:
        command.insert(2, '-'+exec_type)

    # Check for Aphrodite-specific arguments
    if 'gpus' in kwargs:
        command.extend(['--gpus', kwargs['gpus']])
    if 'shm-size' in kwargs:
        command.extend(['--shm-size', kwargs['shm-size']])
    if 'env' in kwargs:
        for env_var in kwargs['env']:
            command.extend(['-e', env_var])

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
    with open('config.yaml') as file:
        config = yaml.safe_load(file)

    # Creating Docker network
    subprocess.run(['docker', 'network', 'create', config['worker_config']['network']])

    # Cloning repositories from GitHub
    clone_repo("https://github.com/GoldenWind8/grid-text-worker", "AI-Horde-Worker")
    clone_repo("https://github.com/gonner22/aphrodite-engine", "aphrodite-engine")

    # Checking for existence of bridgeData.yaml
    if not os.path.exists("bridgeData.yaml"):
        print("Error: bridgeData.yaml not found!")
        print("Please copy bridgeData_template.yaml file with the name bridgeData.yaml in the root directory including your configurations.")
        exit(1)

    # Copying bridgeData.yaml to AI-Horde-Worker directory
    shutil.copy("bridgeData.yaml", "AI-Horde-Worker")

    # Changing directory to AI-Horde-Worker
    os.chdir("AI-Horde-Worker")

    # Building worker Docker image
    build_docker_image()

    # Running worker Docker container
    run_docker_container(**config['worker_config'])

    # Changing directory back to the main directory
    os.chdir("..")

    # Navigating to aphrodite-engine directory
    os.chdir("aphrodite-engine")

    # Running aphrodite-engine Docker container
    run_docker_container(**config['aphrodite_config'])
