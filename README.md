## Installation and Setup

### Initial Setup

1. **Customize Dockerfile**: Before building the container, make sure to replace the constants in square brackets with your own values in the `Dockerfile`.

2. **Build and Run Container**: To build and run the container, you first need to copy the `Dockerfile` to your local machine. Then, navigate to the directory containing the `Dockerfile` and execute the following commands:

   ```shell
   podman build -t mybots .
   chmod -R 777 ~/mybots/data
   podman run -v ~/mybots_data:/app/data:Z -d --name mybots mybots
   ```

### Updating the Container

To update the container after making changes or pulling updates from the repository, follow these steps:

1. **Remove the Existing Container and Image**: Before you can rebuild the container, you need to remove the current version. Run these commands to delete the existing container and image:

   ```shell
   podman stop mybots
   podman rm mybots
   podman rmi mybots
   ```

2. **Rebuild and Run the Updated Container**: After removing the old container and image, rebuild and run the container using the updated `Dockerfile`:

   ```shell
   podman build -t mybots .
   podman run -v ~/mybots_data:/app/data:Z -d --name mybots mybots
   ```

---

Note: Ensure that you're always running these commands in the directory containing the `Dockerfile`. This README assumes familiarity with basic Docker/Podman operations. If you're new to Docker or Podman, it might be helpful to refer to their respective documentation for more detailed instructions.

---

## License
This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE.md) file for details.
