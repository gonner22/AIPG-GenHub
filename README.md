# Generation Hub!
This repository serves a dual purpose. 
- Firstly, it facilitates the automated setup and execution of two Docker containers, streamlining the process for users interested in TextGen. 
- Additionally, it provides an efficient solution for those working with ImageGen, enabling image generation, post-processing, or analysis with ease through Docker containers.

## Quick access links:

- [TextGen Automation section](#textgen-automation)
- [ImageGen Automation section](#imagegen-automation)
  
Feel free to jump to the section that interests you the most!

## TextGen Automation
**AI-Grid-Worker**  
This component enables the setup of an AI Grid Worker, designed to complete text inference jobs on The Grid.

**aphrodite-engine**  
Aphrodite serves as the official backend engine for Text Inference.

### Installation
#### Pre-requisites
- Install and configure 
  - Docker: https://docs.docker.com/engine/install
  - Python 
  - CUDA Driver, CUDA Toolkit and NVIDIA Container Toolkit on your system: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
  - On Ubuntu you will also need to run: ```sudo apt install python3.10-venv```

To use TextGen, follow these steps:
1. Clone the repository AIPG-GenHub.
```bash 
git clone https://github.com/gonner22/AIPG-GenHub
```
2. Navigate into the cloned directory.
```bash
cd AIPG-GenHub
```
3. Create a Python virtual environment.
```bash
python3 -m venv venv
```
4. Activate the virtual environment.
```bash
source venv/bin/activate
```
5. Install PyYAML.
```bash
pip install pyyaml
```

To customize your TextGen Worker, follow these steps:

1. Create a copy of `bridgeData_textgen_template.yaml` in the root directory of the cloned repository and rename it to `bridgeData.yaml`. Update the following mandatory fields in `bridgeData.yaml`:
   - `api_key` _(required)_: Enter your Grid API key. If you don't have one, [register here](https://api.aipowergrid.io/register) to get an API key.
   - `scribe_name` _(required)_: Choose a custom name for your worker.

   _Optionally, you can also modify these fields:_
   - `max_threads`: Set the number of concurrent requests your worker should handle. Higher values require more VRAM. Default is 1.
   - `kai_url`: Specify the Aphrodite URL. By default, it should be `http://<container_name>:7860`. In the template, it's set to `http://aphrodite-engine:7860`. Note that `<container_name>` refers to the name of the Aphrodite container.
   - `max_length`: Define the maximum number of tokens per request. A recommended value is `512`. 
   - `max_context_length`: Set the maximum context length of the Grid worker. This should match your model's default max length or the value you provided for `--max-model-len` when starting the engine.

2. Edit `config.yaml` in the root directory of the cloned repository to configure container settings:
   - `MODEL_NAME` _(required)_: Specify the name of the model you want to use. Refer to the [Model List](to be added) for supported models and their VRAM requirements.
   - `HF_TOKEN` _(required for gated models)_: If you're using a gated model like llama 3, provide your [Hugging Face token](https://huggingface.co/settings/tokens).
   - `GPU_MEMORY_UTILIZATION` (optional): If you encounter memory issues, consider reducing this value.

Please ensure that you provide the mandatory fields `MODEL_NAME`, `HF_TOKEN` (if using a gated model), and `api_key` in the respective configuration files. The other fields are optional and can be left at their default values if desired.

For the complete list of environment variables, please refer to [here](https://github.com/PygmalionAI/aphrodite-engine/blob/main/docker/.env). These represent the default configuration, which can be further customized based on individual user requirements and hardware specifications.

### Running the Python script to launch Worker and Aphrodite
```bash
sudo python3 worker_texgen.py
```
Run to clean up containers when you are done
```bash
sudo ./cleanup.sh
```
After both containers are up and running, Aphrodite-engine will begin downloading additional models, which total around 14-48 GB in size depending on the model. Please allow a few extra minutes for this process to finish. Once completed, you will observe both containers starting to communicate with each other.

**Note:** To interact with the Docker container, you can follow these steps:
- To list your running containers, use the command `docker ps -a`
- To enter the running container, use the command `docker attach <container_name>`
- To exit the container without stopping it, press `Ctrl + P`, followed by `Ctrl + Q`
- If your Texgen application utilizes ports other than 7860 for internal Docker-to-Docker communication and 2242 for internal Docker-to-host communication, you will need to adjust them accordingly. After modifying these ports, ensure to update them both in the Dockerfile and the bridgeData.yaml configuration file.

## ImageGen Automation
**AI Power Grid Image Worker**
This module facilitates the setup of an AI Power Grid Image Worker through the creation and execution of a Docker container, offering capabilities for image generation, post-processing, or analysis for diverse applications.

### Installation
#### Pre-requisites
- Install and configure
  - Docker: https://docs.docker.com/engine/install
  - Python
  - CUDA Driver 12.1, 12.2 or 12.3 only. Ensure that one of these three versions is installed on your system, as you will later need to select the container image that matches the installed version.
  - CUDA Toolkit and NVIDIA Container Toolkit on your system: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
  - On Ubuntu you will also need to run: ```sudo apt install python3.10-venv```

To use ImageGen, follow these steps:
1. Clone the repository AIPG-GenHub.
```bash 
git clone https://github.com/gonner22/AIPG-GenHub
```
2. Navigate into the cloned directory.
```bash
cd AIPG-GenHub
```
3. Create a Python virtual environment.
```bash
python3 -m venv venv-imagegen
```
4. Activate the virtual environment.
```bash
source imagegen/bin/activate
```
5. Install Dependencies.
```bash
pip install python-dotenv loguru ruamel.yaml horde-model-reference horde-sdk
```

To customize your ImageGen Worker, follow these steps:

1. Create a copy of `bridgeData_imagegen_template.yaml` in the root directory of the cloned repository and rename it to `bridgeData.yaml`. Update the following mandatory fields in `bridgeData.yaml`:
   - `horde_url` _(required)_: Enter horde url ("https://api.aipowergrid.io")
   - `api_key` _(required)_: Enter your Grid API key. If you don't have one, [register here](https://api.aipowergrid.io/register) to get an API key.
   - `dreamer_name` _(required)_: Choose a custom name for your worker.
   - `cache_home` _(required)_: The location in which stable diffusion ckpt models are stored

   _Optionally, you can also modify these fields:_
   - `max_threads`: Set the number of concurrent requests your worker should handle. Higher values require more VRAM. Default is 1.
   - `models_to_load`: The models to use
   - Please ensure to review and adjust other parameters as needed for specific configurations.

2. Execute the following script to convert the configuration parameters defined in the previous step (`bridgeData.yaml`) into a format compatible with the Docker container:
```bash
python3 convert_config_to_env.py
```
   After executing the script, you will find `bridgeData.env` in the same directory. This file contains the environment variables compatible with the container.

3. Edit `config-imagengen.yaml` in the root directory of the cloned repository to configure container settings:
  - exec_type: Define the exec type of the container
  - ports: Ports enabled
  - container_name: Define the container name
  - gpus: All the gpus with "all", or using the gpu number
  - env-file: the file where the container env variables are stored, default file is `bridgeData.env`
  - image_name: Define the image name

### Running the Python script to launch Image Worker
```bash
sudo python3 worker_imagegen.py
```

After executing this command, the container will be loaded. Please wait a few minutes as it downloads the models.

**Note:** To interact with the Docker container, you can follow these steps:
- To list your running containers, use the command `docker ps -a`
- To enter the running container, use the command `docker attach <container_name>`
- To exit the container without stopping it, press `Ctrl + P`, followed by `Ctrl + Q`
