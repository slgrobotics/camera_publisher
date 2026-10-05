"""
ROS2 camera publisher node using GStreamer.

This node works on Raspberry Pi 4 with the Raspberry Pi Camera Module v2.1 (Sony IMX219) and the Ubuntu 24/26 libcamera stack.

Captures frames from a local camera using GStreamer and OpenCV and publishes them at ~20 Hz
as both:
  • sensor_msgs/msg/Image              (camera/image_raw)
  • sensor_msgs/msg/CompressedImage    (camera/image_raw/compressed)

Author: Sergei Grichine / ChatGPT.com

See https://github.com/slgrobotics/robots_bringup/blob/main/Docs/Sensors/Camera.md#python-opencv-and-gstreamer

sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base \
 gstreamer1.0-plugins-good gstreamer1.0-plugins-base-apps \
 gstreamer1.0-libcamera

Find camera names with:
 gst-device-monitor-1.0 Video 2>/dev/null | grep name

"""

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import cv2


def parse_image_size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split('x')
        width, height = int(width_text.strip()), int(height_text.strip())
    except ValueError:
        raise ValueError(
            f'Invalid image_size {value!r}; expected WIDTHxHEIGHT, e.g. 640x480'
        ) from None

    if width <= 0 or height <= 0:
        raise ValueError('image_size width and height must be greater than zero')
    return width, height



class ImagePublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher_gs')

        self.raw_pub = self.create_publisher(Image, 'camera/image_raw', 10)
        self.compressed_pub = self.create_publisher(
            CompressedImage,
            'camera/image_raw/compressed',
            10
        )

        self.br = CvBridge()

        self.fps = self.declare_parameter('fps', 5).value
        if self.fps <= 0:
            raise ValueError('The fps parameter must be greater than zero')
        self.frame_id = str(
            self.declare_parameter('frame_id', 'camera_frame').value)
        self.image_width, self.image_height = parse_image_size(
            self.declare_parameter('image_size', '640x480').value)

        # Find camera names with:
        #     gst-device-monitor-1.0 Video 2>/dev/null | grep name
        camera = self.declare_parameter(
            'camera_name',
            '/base/axi/pcie@1000120000/rp1/i2c@88000/imx219@10',
        ).value

        self.get_logger().info(f'Using camera: {camera}')

        cam_pipeline_str = (
            f"libcamerasrc camera-name={camera} ! "
            "video/x-raw,width=self.image_width,height=self.image_height,framerate=10/1,format=RGBx ! "
            "videoconvert ! videoscale ! "
            "video/x-raw,width=self.image_width,height=self.image_height,format=BGR ! appsink"
        )

        # Use gstreamer:
        self.cap = cv2.VideoCapture(cam_pipeline_str, cv2.CAP_GSTREAMER)

        if not self.cap.isOpened():
            self.get_logger().error('Could not open video device')
            raise RuntimeError('Could not open video device')

        self.timer = self.create_timer(1.0 / self.fps, self.timer_callback)

        self.get_logger().info('Camera publisher node has been started.')
        self.get_logger().info('    Image size: %dx%d' % (self.image_width, self.image_height))
        self.get_logger().info('    Publishing at %.2f FPS' % self.fps)
        self.get_logger().info('    Frame ID: %s' % self.frame_id)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret or frame is None:
            self.get_logger().error('Error grabbing video frame')
            return

        #self.get_logger().info('OK: grabbed video frame -------------------')

        stamp = self.get_clock().now().to_msg()
        frame_id = self.frame_id

        # Raw image
        raw_msg = self.br.cv2_to_imgmsg(frame, encoding='bgr8')
        raw_msg.header.stamp = stamp
        raw_msg.header.frame_id = frame_id
        self.raw_pub.publish(raw_msg)

        # Compressed image
        ok, encoded = cv2.imencode(
            '.jpg',
            frame,
            [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        )
        if not ok:
            self.get_logger().error('Failed to encode frame as JPEG')
            return

        comp_msg = CompressedImage()
        comp_msg.header.stamp = stamp
        comp_msg.header.frame_id = frame_id
        comp_msg.format = 'jpeg'
        comp_msg.data = encoded.tobytes()
        self.compressed_pub.publish(comp_msg)

    def destroy_node(self):
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = ImagePublisher()

    try:
        rclpy.spin(camera_publisher)
    except KeyboardInterrupt:
        print('Keyboard interrupt, shutting down.')
    finally:
        try:
            camera_publisher.destroy_node()
        finally:
            if rclpy.ok():
                rclpy.shutdown()

if __name__ == '__main__':
    main()
