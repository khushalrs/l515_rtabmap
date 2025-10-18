# Intel RealSense L515 – ROS 2 Setup Guide

This guide documents the full setup process and configurable parameters for the **Intel RealSense L515** LiDAR camera, tested with **ROS 2 Jazzy**, **librealsense v2.54.1**, and the **realsense-ros wrapper v4.54.1**.

---

## 🧰 Requirements

- **Ubuntu 22.04 LTS** (recommended)  
- **ROS 2 Jazzy Jalisco**  
- **CMake ≥ 3.10**  
- **libusb 1.0 ≥ 1.0.23**  
- Internet connection for cloning repositories  

---

## ⚙️ 1. Install Intel RealSense SDK 2.0 (v2.54.1)

```bash
# 1) Install prerequisites
sudo apt update
sudo apt install -y build-essential cmake git libusb-1.0-0-dev pkg-config

# 2) Clone the SDK at the required version
git clone --branch v2.54.1 https://github.com/IntelRealSense/librealsense.git
cd librealsense

# 3) Configure build
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_TOOLS=ON -DBUILD_EXAMPLES=ON

# (Optional) If USB or kernel issues occur:
# cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_TOOLS=ON -DBUILD_EXAMPLES=ON -DFORCE_RSUSB_BACKEND=ON

# 4) Compile & install
make -j"$(nproc)"
sudo make install
sudo ldconfig

# 5) Enable device permissions
cd ../config
sudo cp 99-realsense-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

**Test camera detection:**

```bash
rs-enumerate-devices -v
realsense-viewer
```

---

## 🤖 2. Install ROS 2 Wrapper (v4.54.1)

```bash
# 0) Prerequisites
sudo apt update
sudo apt install -y git python3-colcon-common-extensions   ros-jazzy-image-transport ros-jazzy-cv-bridge ros-jazzy-diagnostic-updater

# 1) Create workspace
mkdir -p ~/rs_ws/src && cd ~/rs_ws/src

# 2) Clone wrapper at the specific tag
git clone --branch 4.54.1 https://github.com/IntelRealSense/realsense-ros.git
```

### (Optional) Patch for ROS 2 Jazzy Support

If your ROS 2 version isn’t natively supported by the tag:

```bash
cd ~/rs_ws/src/realsense-ros/realsense2_camera
sed -i '/STREQUAL "rolling"/aelseif("$ENV{ROS_DISTRO}" STREQUAL "jazzy")  message(STATUS "Build for ROS2 Jazzy")  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DJAZZY")  set(SOURCES "${SOURCES}" src/ros_param_backend_rolling.cpp)' CMakeLists.txt
```

### Build and Source Workspace

```bash
cd ~/rs_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source ~/rs_ws/install/setup.bash
```

---

## 🧪 3. Testing the Camera

**Launch the camera node:**
```bash
ros2 launch realsense2_camera rs_launch.py
```

**Confirm published topics:**
```bash
ros2 topic list
```

---

## 🗺️ 4. Testing with RTAB-Map (Depth + RGB)

For visual SLAM or mapping:
```bash
ros2 launch realsense2_camera rs_launch.py align_depth.enable:=true

ros2 launch rtabmap_launch rtabmap.launch.py   rgb_topic:=/camera/color/image_raw   depth_topic:=/camera/aligned_depth_to_color/image_raw   camera_info_topic:=/camera/color/camera_info   frame_id:=camera_link   approx_sync:=true   qos:=2
```

---

## ⚙️ 5. Configurable Parameters

All adjustable parameters for the **L515** ROS 2 driver are listed in [`L515_param.txt`](./L515_param.txt).  
Key groups include:

| Category | Example Parameters |
|-----------|------------------|
| **Depth Module** | `depth_module.laser_power`, `depth_module.min_distance`, `depth_module.profile` |
| **RGB Camera** | `rgb_camera.profile`, `rgb_camera.enable_auto_exposure`, `rgb_camera.white_balance` |
| **Filters** | `decimation_filter.enable`, `spatial_filter.enable`, `temporal_filter.enable` |
| **Pointcloud** | `pointcloud.enable`, `pointcloud.ordered_pc`, `pointcloud.pointcloud_qos` |
| **Motion Modules** | `enable_accel`, `enable_gyro`, `unite_imu_method` |
| **QoS / Diagnostics** | `diagnostics_period`, `depth_qos`, `color_qos` |

Edit your desired values inside a `.yaml` or `.launch.py` file to tune the behavior for mapping or navigation use-cases.

---

## 🧩 6. Troubleshooting

- **Camera not detected:**  
  Ensure USB 3.0 connection and re-run `sudo udevadm trigger`.
- **No topics published:**  
  Check your workspace is sourced (`source ~/rs_ws/install/setup.bash`).
- **Driver version mismatch:**  
  Confirm `librealsense` and `realsense-ros` versions match (v2.54.1 + v4.54.1).
- **Depth alignment issues:**  
  Set `align_depth.enable:=true` in the launch file.

---

## 🧾 References

- Intel RealSense SDK 2.0 → [v2.54.1 release](https://github.com/IntelRealSense/librealsense/releases/tag/v2.54.1)  
- realsense-ros → [v4.54.1 release](https://github.com/IntelRealSense/realsense-ros/releases/tag/4.54.1)  
- Full parameter list → [`L515_param.txt`](./L515_param.txt)  
- Setup instructions → [`L515_setup.txt`](./L515_setup.txt)

---
