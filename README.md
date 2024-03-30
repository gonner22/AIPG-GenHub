# AIPG-GenHub

This repository serves a dual purpose. 
- Firstly, it facilitates the automated setup and execution of two Docker containers, streamlining the process for users interested in TextGen. 
- Additionally, it provides an efficient solution for those working with ImageGen, enabling image generation, post-processing, or analysis with ease through Docker containers.

## Quick access links:

- [TextGen Automation section](#textgen-automation)
- [ImageGen Automation section](#imagegen-automation)
  
Feel free to jump to the section that interests you the most!

## TextGen Automation
**AI-Horde-Worker**  
This component enables the setup of an AI Horde Worker, designed to complete text inference jobs on the Horde.

**aphrodite-engine**  
Aphrodite serves as the official backend engine for PygmalionAI. Will be used by the worker for inference.

### Installation
#### Pre-requisites
- Install and configure Docker and Python on your system.

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

### Usage
Follow these steps to customize your TextGen Worker:

- Create a duplicate of bridgeData_template.yaml and rename it to bridgeData.yaml in the root directory of the cloned repository. Configure the following values within `bridgeData.yaml`:

  - `api_key`: Your horde API key. [Register here](https://api.aipowergrid.io/register) to acquire one.
  - `max_threads`: specifies how many concurrent requests your worker should run. Higher values require more VRAM.
  - `scribe_name`: your custom worker name.
  - `kai_url`: the Aphrodite URL. By default, this should be `http://<container_name>:7860, in our template is set to: http://aphrodite-engine:7860`. Attention: the 'container_name' field refers to the name of the Aphrodite container.
  - `max_length`: this specifies the max number of tokens every request can make. A good value is `512`.
  - `max_context_length`: The maximum context length of the horde worker. Set this to your model's default max length, or whatever value you passed to `--max-model-len` when launching the engine.
  
- Configure `config.yaml` in the root directory of the cloned repository, where the user defines values for the containers.

  - `MODEL_NAME`: Path to the model on hugging face
  - `GPU_MEMORY_UTILIZATION`: If you are running out of memory, consider decreasing this value

For the complete list of environment variables, please refer to [here](/docker/.env). These represent the default configuration, which can be further customized based on individual user requirements and hardware specifications.

- Running the Python script to launch TextGen, including worker and Aphrodite
```bash
python3 worker_texgen.py
```
After both containers are up and running, Aphrodite-engine will begin downloading additional models, which total around 14-48 GB in size depending on the model . Please allow a few extra minutes for this process to finish. Once completed, you will observe both containers starting to communicate with each other.

**Note:** To interact with the Docker container, you can follow these steps:
- To list your running containers, use the command `docker ps -a`
- To enter the running container, use the command `docker attach <container_name>`
- To exit the container without stopping it, press `Ctrl + P`, followed by `Ctrl + Q`
- If your Texgen application utilizes ports other than 7860 for internal Docker-to-Docker communication and 2242 for internal Docker-to-host communication, you will need to adjust them accordingly. After modifying these ports, ensure to update them both in the Dockerfile and the bridgeData.yaml configuration file.

## ImageGen Automation
**AI Power Grid Image Worker**  
This module facilitates the setup of an AI Power Grid Worker through the creation and execution of a Docker container, offering capabilities for image generation, post-processing, or analysis for diverse applications.

TBD TBD TBD !!! In active development, it will be ready for release and published in this repository soon.
