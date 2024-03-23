import os
import shutil
import subprocess
import yaml

def clone_repo(repo_url, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    subprocess.run(['git', 'clone', repo_url, destination])

def build_docker_image():
    subprocess.run(['docker', 'build', '-t', config['worker_config']['image_name'], '.'])

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

    print("Final Docker Command for Aphrodite:")
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
    print("Centralized repository for AI worker and generators")
    print("Location: United States of America / Web: aipowergrid.io / X: @AIPowerGrid / e-mail: admin@aipowergrid.io\n")

    with open('config.yaml') as file:
        config = yaml.safe_load(file)

    # Creating Docker network 'ai_network'
    subprocess.run(['docker', 'network', 'create', config['worker_config']['network']])

    # Clone repositories
    clone_repo("https://github.com/gonner22/AI-Horde-Worker", "AI-Horde-Worker")
    clone_repo("https://github.com/gonner22/aphrodite-engine", "aphrodite-engine")

    # Check if bridgeData.yaml exists
    if not os.path.exists("bridgeData.yaml"):
        print("Error: bridgeData.yaml not found!")
        print("Please copy bridgeData_template.yaml file with the name bridgeData.yaml in the root directory including your configurations.")
        exit(1)

    # Copy bridgeData.yaml to AI-Horde-Worker directory
    shutil.copy("bridgeData.yaml", "AI-Horde-Worker")

    # Change directory to AI-Horde-Worker
    os.chdir("AI-Horde-Worker")

    # Build worker docker image
#    build_docker_image()

    # Run worker docker container
#    run_docker_container(**config['worker_config'])

    # Change directory back to the main directory
    os.chdir("..")

    os.chdir("aphrodite-engine")
    # Run aphrodite-engine docker container
    print("Aphrodite Config:", config['aphrodite_config'])
    run_docker_container(**config['aphrodite_config'])
