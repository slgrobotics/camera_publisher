Back to [Main Project Home](https://github.com/slgrobotics/articubot_one/wiki)

## camera_publisher package

### A simple ROS2 Webcam or FPV grabber image publisher
 
This is a simple Python/OpenCV publisher, created by literally following directions here: 
- https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/

All credit goes to Mr. Addison Sears-Collins (https://automaticaddison.com) - his site is a great resource for anything Robotics.

Works with either a webcam or an *FPV Camera + FPV Video Grabber* on an Ubuntu 22.04 desktop machine.

### "Out-of-band" operation

Here's my "out-of-band" setup:
- https://www.amazon.com/dp/B06VY7L1N4 - placed on the robot and transmitting over 5.8 GHz band.
- https://www.amazon.com/dp/B07Q5MPC8V - connected to the *ground station* machine via USB.

It bypasses the robot's CPU and allows the video stream to go directly to the *ground station*,
where it feeds into ROS2. This frees the Wi-Fi network for more critical ROS2 traffic.

You can watch the FPV video in the Ubuntu **Cheese** app, view it in **RViz2**, 
or feed it into ROS2 processing nodes running on the workstation instead of the robot.

### Build instructions:

```
mkdir -p ~/grabber_ws/src
cd ~/grabber_ws/src/
git clone https://github.com/slgrobotics/camera_publisher.git
cd ..
colcon build
echo "ros2 run cv_basics img_publisher" > run.sh
chmod +x run.sh 

source cd ~/grabber_ws/install/setup.bash
~/grabber_ws/run.sh 
```

The node publishes:
- /camera/image_raw
- /camera/image_raw/compressed

You can also run it directly without creating a shell script:
```
ros2 run cv_basics img_publisher
```

Or use a simplified version (publishing only the `/camera/image_raw` topic):
```
ros2 run cv_basics img_publisher_raw
```

**Note:** the raw image stream uses about **20 MBytes/s**, while the compressed stream uses **less than 1 MBytes/s**.

See this guide: https://github.com/slgrobotics/robots_bringup/blob/main/Docs/Sensors/Camera.md

------------------

Back to [Main Project Home](https://github.com/slgrobotics/articubot_one/wiki)
