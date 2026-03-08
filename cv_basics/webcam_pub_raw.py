# Basic ROS 2 program to publish real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
# - https://automaticaddison.com/getting-started-with-opencv-in-ros-2-foxy-fitzroy-python/
  
# Import the necessary libraries
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
 
class ImagePublisher(Node):
  """
  Create an ImagePublisher class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_publisher_raw')
      
    # Create the publisher. This publisher will publish an Image
    # to the video_frames topic. The queue size is 10 messages.
    self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)  # 10 is queue size
      
    # We will publish a message every 0.05 seconds
    timer_period = 0.05  # seconds
      
    # Create the timer
    self.timer = self.create_timer(timer_period, self.timer_callback)

    # -------------------------------------------------------
    # Create a VideoCapture object
    # The argument '0' gets the default webcam.

    self.cap = cv2.VideoCapture(0)

    # -------------------------------------------------------

    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
    self.get_logger().info('Raw image publisher node has been started.')

  def timer_callback(self):
    """
    Callback function.
    This function gets called every 0.1 seconds.
    """
    # Capture frame-by-frame
    # This method returns True/False as well
    # as the video frame.
    ret, frame = self.cap.read()
          
    if ret == True:
      # Publish the image.
      # The 'cv2_to_imgmsg' method converts an OpenCV
      # image to a ROS 2 image message
      self.publisher_.publish(self.br.cv2_to_imgmsg(frame))
    else: 
      # Display the message on the console
      self.get_logger().error('grabbing video frame')
  
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