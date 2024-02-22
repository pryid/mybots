## Overview

This repository contains the necessary files to build and run a Docker container for my Telegram bots. Using Podman, an alternative to Docker, this guide will walk you through the process of building and running your bot container.

## Prerequisites

Before proceeding, ensure you have Podman installed on your system. Podman is a daemonless container engine for developing, managing, and running OCI Containers on your Linux system.

## Getting Started

### Step 1: Customize Dockerfile

Replace the constants in square brackets with your specific values in the Dockerfile. These constants are placeholders for your specific configurations.

### Step 2: Build and Run the Container

Navigate to the directory containing your Dockerfile and execute the following commands:

```bash
podman build -t mybots .
podman run --name mybots mybots
```

This will build a Docker container named `mybots` and run it.

### Step 3: Reinstalling After Repository Updates

In case you update the repository and need to reinstall the bot, follow these steps to remove the old container and build a new one:

```bash
podman rm mybots
podman rmi mybots
podman build -t mybots .
podman run --name mybots mybots
```

This will ensure that your bot is running with the latest updates from your repository.

## Support

For any issues or queries, feel free to open an issue in this repository.
