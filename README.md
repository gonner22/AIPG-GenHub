# AIPG-GenHub

This repository serves a dual purpose. Firstly, it facilitates the automated setup and execution of two Docker containers, streamlining the process for users interested in TextGen. Additionally, it provides an efficient solution for those working with ImageGen, enabling image generation, post-processing, or analysis with ease through Docker containers.

## Quick access links:

- [TextGen Automation section](#textgen-automation)
- [ImageGen Automation section](#imagegen-automation)
  
Feel free to jump to the section that interests you the most!"

## TextGen Automation
**AI-Horde-Worker**  
This component enables the setup of an AI Horde Worker, designed to generate or alchemize images for various purposes.

**aphrodite-engine**  
Aphrodite serves as the official backend engine for PygmalionAI. It is tailored to serve as the inference endpoint for the PygmalionAI website and deliver Pygmalion models to users swiftly and efficiently.

### Installation
To use TextGen, follow these steps:

- Install and configure Docker and Python on your system.
- Clone the repository AIPG-GenHub.
```bash 
git clone https://github.com/gonner22/AIPG-GenHub
```
- Navigate into the cloned directory.
```bash
cd AIPG-GenHub
```
- Create a Python virtual environment.
```bash
python3 -m venv venv
```
- Activate the virtual environment.
```bash
source venv/bin/activate
```
- Install PyYAML.
```bash
pip install pyyaml
```

### Usage
Follow these steps to configure and use the TextGen:

- Create a duplicate of bridgeData_template.yaml and rename it to bridgeData.yaml in the root directory of the cloned repository. Configure the following values within `bridgeData.yaml`:

  - `api_key`: Your horde API key. [Register here](https://api.aipowergrid.io/register) to acquire one.
  - `max_threads`: specifies how many concurrent requests your worker should run. Higher values require more VRAM.
  - `scribe_name`: your custom worker name.
  - `kai_url`: the Aphrodite URL. By default, this should be `http://<container_name>:7860, in our template is set to: http://aphrodite-engine:7860`. Attention: the 'container_name' field refers to the name of the Aphrodite container.
  - `max_length`: this specifies the max number of tokens every request can make. A good value is `512`.
  - `max_context_length`: The maximum context length of the horde worker. Set this to your model's default max length, or whatever value you passed to `--max-model-len` when launching the engine.
  
- Configure `config.yaml` in the root directory of the cloned repository, where the user defines values for the containers.
```bash
worker_config:
  exec_type: it
  ports: "443:443"
  network: ai_network
  container_name: worker
  image_name: worker-image

aphrodite_config:
  exec_type: it
  ports: "2242:7860"
  network: ai_network
  container_name: aphrodite-engine
  gpus: "all"
  shm-size: "8g"
  env:
    - MODEL_NAME=PygmalionAI/pygmalion-2-7b
    - KOBOLD_API=true
    - GPU_MEMORY_UTILIZATION=0.8 #If you are running out of memory, consider decreasing this value
  image_name: alpindale/aphrodite-engine
```
For the complete list of environment variables, please refer to [here](/docker/.env). These represent the default configuration, which can be further customized based on individual user requirements and hardware specifications.

- Running the Python script to launch TextGen, including worker and Aphrodite
```bash
python3 worker_texgen.py
```

**Note:** To interact with the Docker container, you can follow these steps:
- To list your running containers, use the command `docker ps -a`
- To enter the running container, use the command `docker attach <container_name>`
- To exit the container without stopping it, press `Ctrl + P`, followed by `Ctrl + Q`
- If your Texgen application utilizes ports other than 7860 for internal Docker-to-Docker communication and 2242 for internal Docker-to-host communication, you will need to adjust them accordingly. After modifying these ports, ensure to update them both in the Dockerfile and the bridgeData.yaml configuration file.

## ImageGen Automation
**AI Power Grid Image Worker**  
This module facilitates the setup of an AI Power Grid Worker, offering capabilities for image generation, post-processing, or analysis for diverse applications.

TBD TBD TBD !!! In active development, it will be ready for release and published in this repository soon.
