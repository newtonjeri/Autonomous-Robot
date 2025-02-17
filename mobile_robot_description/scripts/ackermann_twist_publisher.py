#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped
from std_msgs.msg import Header

class TwistToTwistStampedRepublisher(Node):
    def __init__(self):
        super().__init__('twist_to_twist_stamped_republisher')
        
        # Create a subscriber to /cmd_vel_nav (Twist)
        self.cmd_vel_nav_sub = self.create_subscription(
            Twist,
            '/cmd_vel_nav',
            self.cmd_vel_nav_callback,
            10)
        
        # Create a publisher to /ackermann_steering_cont/reference (TwistStamped)
        self.ackermann_pub = self.create_publisher(
            TwistStamped,
            '/ackermann_steering_cont/reference',
            10)
        
        # Create a subscriber to /ackermann_steering_cont/reference (TwistStamped)
        self.ackermann_sub = self.create_subscription(
            TwistStamped,
            '/ackermann_steering_cont/reference',
            self.ackermann_callback,
            10)
        
        # Create a publisher to /cmd_vel (Twist)
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)
        
    def cmd_vel_nav_callback(self, msg):
        # Convert the Twist message to TwistStamped
        twist_stamped_msg = TwistStamped()
        twist_stamped_msg.header = Header(stamp=self.get_clock().now().to_msg(), frame_id='odom')
        twist_stamped_msg.twist = msg
        
        # Publish the TwistStamped message to /ackermann_steering_cont/reference
        self.ackermann_pub.publish(twist_stamped_msg)
        # self.get_logger().info('Published TwistStamped to /ackermann_steering_cont/reference')
    
    def ackermann_callback(self, msg):
        # Extract the Twist part of the TwistStamped message
        twist_msg = Twist()
        twist_msg.linear = msg.twist.linear
        twist_msg.angular = msg.twist.angular
        
        # Publish the Twist message to /cmd_vel
        self.cmd_vel_pub.publish(twist_msg)
        # self.get_logger().info('Republished Twist to /cmd_vel')

def main(args=None):
    rclpy.init(args=args)
    
    twist_republisher = TwistToTwistStampedRepublisher()
    
    rclpy.spin(twist_republisher)
    
    # Destroy the node explicitly
    twist_republisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()