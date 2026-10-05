"""
Launch the camera publisher and synthetic camera-info node.

Find camera names with:
 gst-device-monitor-1.0 Video 2>/dev/null | grep name

Launch:
 ros2 launch cv_basics camera_publisher.launch.py

View:
 ros2 run image_view image_view --ros-args -r image:=/camera/image_raw -p image_transport:=compressed

"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    camera_name = LaunchConfiguration('camera_name')
    default_config = PathJoinSubstitution([
        FindPackageShare('cv_basics'),
        'config',
        'camera_publisher.yaml',
    ])

    config_arg = DeclareLaunchArgument(
        'params_file',
        default_value=default_config,
        description='Path to the ROS 2 parameter YAML file.',
    )

    camera_name_arg = DeclareLaunchArgument(
        'camera_name',
        default_value='/base/axi/pcie@1000120000/rp1/i2c@88000/imx219@10',
        description='GStreamer libcamerasrc camera-name value',
    )

    # Arducam camera on Raspberry Pi 4 with the Raspberry Pi Camera Module v2.1 (Sony IMX219)
    # using GStreamer and the Ubuntu 24/26 libcamera stack
    camera_publisher_gs_node = Node(
        package='cv_basics',
        executable='img_publisher_gs',
        name='camera_publisher_gs',
        output='screen',
        parameters=[
            LaunchConfiguration('params_file'),
            {'camera_name': camera_name}
        ],
    )

    # webcam on a workstartion using standard OpenCV backend
    webcam_publisher_raw_node = Node(
        package='cv_basics',
        executable='img_publisher_raw',
        name='webcam_publisher_raw',
        output='screen',
        parameters=[
            LaunchConfiguration('params_file'),
            {'camera_name': camera_name}
        ],
    )

    # webcam on a workstartion using standard OpenCV backend
    webcam_publisher_node = Node(
        package='cv_basics',
        executable='img_publisher',
        name='webcam_publisher',
        output='screen',
        parameters=[
            LaunchConfiguration('params_file'),
            {'camera_name': camera_name}
        ],
    )

    fake_camera_info_node = Node(
        package='cv_basics',
        executable='fake_camera_info_node',
        name='fake_camera_info_node',
        output='screen',
        parameters=[
            LaunchConfiguration('params_file'),
        ],
    )

    return LaunchDescription([
        camera_name_arg,
        config_arg,
        LogInfo(msg='Launching Camera Publisher:'),
        LogInfo(msg=['    camera_name: ', camera_name]),
        LogInfo(msg=['    params_file: ', LaunchConfiguration('params_file')]),
        #camera_publisher_gs_node,
        #webcam_publisher_raw_node,
        webcam_publisher_node,
        #fake_camera_info_node,
    ])
