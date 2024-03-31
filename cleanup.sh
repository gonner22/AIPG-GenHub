#!/bin/bash

# Function to remove a Docker container and its associated image
remove_docker_container_and_image() {
    local container_name=$1
    local image_name=$2

    # Stop and remove the Docker container if it exists
    if docker ps -a --format '{{.Names}}' | grep -Eq "^${container_name}\$"; then
        docker stop "$container_name"
        docker rm "$container_name"
        echo "Docker container '$container_name' stopped and removed."
    fi

    # Remove the Docker image if it exists
    if docker images --format '{{.Repository}}:{{.Tag}}' | grep -Eq "^${image_name}:latest\$"; then
        docker rmi "$image_name"
        echo "Docker image '$image_name' removed."
    fi
}

# Function to remove a cloned Git repository
remove_cloned_repo() {
    local repo_dir=$1

    if [ -d "$repo_dir" ]; then
        rm -rf "$repo_dir"
        echo "Cloned repository '$repo_dir' removed."
    fi
}

# Function to remove a Docker network
remove_docker_network() {
    local network_name=$1

    # Check if the network exists
    if docker network ls --format '{{.Name}}' | grep -Eq "^${network_name}\$"; then
        docker network rm "$network_name"
        echo "Docker network '$network_name' removed."
    fi
}

# Remove worker Docker container and image
remove_docker_container_and_image "worker" "worker_image_name"

# Remove aphrodite-engine Docker container and image
remove_docker_container_and_image "aphrodite-engine" "aphrodite_image_name"

# Remove cloned repositories
#remove_cloned_repo "AI-Horde-Worker"
#remove_cloned_repo "aphrodite-engine"

# Remove Docker network. Replace with actual network name
remove_docker_network "ai_network"

echo "Cleanup completed."