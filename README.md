# camera_publisher
## ROS2 Webcam or FPV grabber image publisher
 
This is a simple Python/OpenCV publisher, created by literally following directions here: 

    https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/

All credit go to Mr. Addison Sears-Collins (https://automaticaddison.com) - his site is a great resource for anything Robotics.

Works with a Webcam or FPV Grabber Camera on Ubuntu 22.04 Desktop.

It allows video feed to go directly to "ground station" and feed into ROS2 there, freeing the network to more critical traffic. You can watch FPV video in Ubuntu Cheese app, or see it in Rviz2 and feed it into ROS2 processing nodes.

Here's my "out-of-band" setup:

https://www.amazon.com/dp/B06VY7L1N4

https://www.amazon.com/dp/B07Q5MPC8V

## Build instructions:

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

