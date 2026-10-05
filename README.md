Back to [Main Project Home](https://github.com/slgrobotics/articubot_one/wiki)

## camera_publisher package

### A simple ROS2 Arducam, Webcam or FPV grabber image publisher
 
> This is a simple Python/OpenCV publisher, created by literally following directions here: 
> - https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/
>
> All credit goes to Mr. Addison Sears-Collins (https://automaticaddison.com) - his site is a great resource for anything Robotics.

Works with either a webcam or an *FPV Camera + FPV Video Grabber* on an Ubuntu 22/24/26 workstation.

**Tips:** 
- use this package if standard [camera_ros binaries](https://github.com/christianrauch/camera_ros) don't work for you on a Raspberry Pi.
- see [this guide](https://github.com/slgrobotics/robots_bringup/blob/main/Docs/Sensors/Camera.md) for *Arducams* and similar cameras on Raspberry Pi's.
- the `camera_publisher_gs_node` uses GStreamer on Raspberry Pi's.
- other nodes are for Workstation webcams, where _libcamera_ works fine with standard OpenCV calls.
- you may want to review and edit the [launch file](https://github.com/slgrobotics/camera_publisher/blob/main/launch/camera_publisher.launch.py).

### Build instructions:

```
mkdir -p ~/grabber_ws/src
cd ~/grabber_ws/src/
git clone https://github.com/slgrobotics/camera_publisher.git

cd ~/grabber_ws
colcon build
source ~/grabber_ws/install/setup.bash

Launch:
 ros2 launch cv_basics camera_publisher.launch.py

View:
 ros2 run image_view image_view --ros-args -r image:=/camera/image_raw -p image_transport:=compressed
```

The nodes would typically publish:
- /camera/image_raw
- /camera/image_raw/compressed

**Note:** the raw image stream uses about **20 MBytes/s**, while the compressed stream uses **much less**.

See these guides:
- https://github.com/slgrobotics/robots_bringup/blob/main/Docs/Sensors/Camera.md
- https://github.com/slgrobotics/robots_bringup/blob/main/Docs/Sensors/Camera_FPV.md

### "Fake" CameraInfo node

See [this guide](https://github.com/slgrobotics/image_to_3d/blob/main/README.md#fake-camerainfo-node) for reasons and use.

### "Out-of-band" operation (FPV Camera)

Here's my "out-of-band" setup:
- https://www.amazon.com/dp/B06VY7L1N4 - placed on the robot and transmitting over 5.8 GHz band.
- https://www.amazon.com/dp/B07Q5MPC8V - connected to the *ground station* machine via USB.

It bypasses the robot's CPU and allows the video stream to go directly to the *ground station*,
where it feeds into ROS2. This frees the Wi-Fi network for more critical ROS2 traffic.

You can watch the FPV video in the Ubuntu **Cheese** app, view it in **RViz2**, 
or feed it into ROS2 processing nodes running on the workstation instead of the robot.

------------------

Back to [Main Project Home](https://github.com/slgrobotics/articubot_one/wiki)
