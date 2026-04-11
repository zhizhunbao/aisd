# Lab 5 Follow-up Prompts & Responses

Author: Peng Wang (041107730)

---

## Follow-up 1: X11 Forwarding on WSL2

### Prompt:
```
How do I enable X11 forwarding so that Gazebo and RViz2 windows appear on my 
Windows desktop when running from a Docker container inside WSL2?
```

### Response:
To enable X11 forwarding from Docker on WSL2:

1. **Install an X server on Windows** (if not using WSLg):
   - VcXsrv or Xming

2. **If using WSLg (Windows 11)**: X11 is already supported natively. Set:
   ```bash
   export DISPLAY=:0
   ```

3. **Allow Docker to use the X display**:
   ```bash
   xhost +local:docker
   ```

4. **The docker-compose.yml already maps** `/tmp/.X11-unix` and passes `DISPLAY`.

5. **Test inside the container**:
   ```bash
   # Quick test with a simple X11 app
   xeyes
   
   # Then try Gazebo
   gazebo --verbose
   ```

---

## Follow-up 2: Rebuilding After Code Changes

### Prompt:
```
If I modify my Assignment 2 Python code (e.g., qlearning.py), do I need to 
rebuild the entire Docker image?
```

### Response:
No, there are two approaches:

**Option A: Volume mount (for development)**
Uncomment the volume mount in `docker-compose.yml`:
```yaml
volumes:
  - ./assn2:/ros2_ws/assn2
```
This way, changes on the host are immediately reflected inside the container without rebuilding.

**Option B: Rebuild (for final submission)**
```bash
# Update the assn2/ directory in build context
cp -r ../assn2 ./assn2/

# Rebuild — Docker layer caching means only the COPY layer and later rebuild
docker compose build
```

Docker's layer caching makes this fast since only the final layers (after the COPY) need to rebuild.

---

## Follow-up 3: GPU Acceleration

### Prompt:
```
My laptop has an NVIDIA GPU. How do I ensure the Docker container can use it 
for Gazebo rendering?
```

### Response:
1. **Install NVIDIA Container Toolkit** on the host:
   ```bash
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
       sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
       sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo nvidia-ctk runtime configure --runtime=docker
   sudo systemctl restart docker
   ```

2. **Add runtime to docker-compose.yml** (if needed):
   ```yaml
   services:
     ros2-create3:
       runtime: nvidia
   ```

3. The environment variables `NVIDIA_VISIBLE_DEVICES=all` and `NVIDIA_DRIVER_CAPABILITIES=all` are already set in the compose file.

4. **Verify inside container**:
   ```bash
   nvidia-smi
   glxinfo | grep "OpenGL renderer"
   ```
