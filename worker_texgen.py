import os
import subprocess
import yaml

def clone_repo(repo_url, destination):
    subprocess.run(['git', 'clone', repo_url, destination])

def build_docker_image():
    subprocess.run(['docker', 'build', '-t', config['worker_config']['image_name'], '.'])

def run_docker_container(exec_type, ports, network, container_name, image_name, **kwargs):
    command = ['docker', 'run', '-d', '-p', ports, '--network', network, '--name', container_name]

    if exec_type:
        command.insert(2, '-'+exec_type)

    for key, value in kwargs.items():
        command.append('--'+key)
        command.append(value)

    command.append(image_name)
    
    subprocess.run(command)

if __name__ == "__main__":
    # ASCII Art
    print('''
   _   _ _____ _     _____ ____  __  __ _____ 
  / \ | | ____| |   | ____|  _ \|  \/  | ____|
 / _ \| |  _| | |   |  _| | |_) | |\/| |  _|  
/ ___ \ | |___| |___| |___|  _ <| |  | | |___ 
/_/   \_\_____|_____|_____|_| \_\_|  |_|_____|
                                              
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

    # Change directory to cloned repositories
    os.chdir("AI-Horde-Worker")
    # Build worker docker image
    build_docker_image()

    os.chdir("../aphrodite-engine")
    # Run worker docker container
    run_docker_container(**config['worker_config'])

    # Change directory back to the main directory
    os.chdir("..")

    os.chdir("aphrodite-engine")
    # Run aphrodite-engine docker container
    run_docker_container(**config['aphrodite_config'])
