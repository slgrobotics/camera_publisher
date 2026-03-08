"""
ROS2 webcam publisher node.

Captures frames from a local camera using OpenCV and publishes them at ~20 Hz
as both:
  • sensor_msgs/msg/Image              (/camera/image_raw)
  • sensor_msgs/msg/CompressedImage    (/camera/image_raw/compressed)

Intended for visualization in RViz and efficient transport to downstream perception nodes.

Author: Sergei Grichine / ChatGPT.com
"""

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
import cv2


class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')

        self.raw_pub = self.create_publisher(Image, '/camera/image_raw', 10)
        self.compressed_pub = self.create_publisher(
            CompressedImage,
            '/camera/image_raw/compressed',
            10
        )

        self.br = CvBridge()

        # Prefer V4L2 on Linux instead of default backend
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            self.get_logger().error('Could not open video device')
            raise RuntimeError('Could not open video device')

        # Reduce load
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 20)

        # Optional: ask camera for MJPEG, often much faster on USB webcams
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        self.timer = self.create_timer(0.05, self.timer_callback)  # 20 Hz

        self.get_logger().info('Image publisher node has been started.')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret or frame is None:
            self.get_logger().error('Error grabbing video frame')
            return

        stamp = self.get_clock().now().to_msg()
        frame_id = 'camera_frame'

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
    image_publisher = ImagePublisher()

    try:
        rclpy.spin(image_publisher)
    except KeyboardInterrupt:
        print('Keyboard interrupt, shutting down.')
    finally:
        try:
            image_publisher.destroy_node()
        finally:
            if rclpy.ok():
                rclpy.shutdown()

if __name__ == '__main__':
    main()