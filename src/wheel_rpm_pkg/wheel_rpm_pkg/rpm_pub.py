#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node 
from std_msgs.msg import Float32

RPM_DEFAULT = 10

class RpmPublisher(Node):
	def __init__(self):
		super().__init__("rpm_pub_node")
		# self.declare_parameter("rpm_rate", RPM_DEFAULT)
		self.pub = self.create_publisher(Float32, "rpm", 10)
		self.timer = self.create_timer(0.5, self.publish_rpm)
		self.counter = 0

	def publish_rpm(self):
		msg = Float32()
		# rpm_param = self.get_parameter("rpm_rate").get_parameter_value().double_value
		msg.data = float(RPM_DEFAULT)
		self.pub.publish(msg)
		self.counter += 1

def main(args=None):
	rclpy.init()
	my_pub = RpmPublisher()
	print("RPM Publisher Node Running...")

	try:
		rclpy.spin(my_pub)
	except KeyboardInterrupt:
		print("Terminating Node...")
		my_pub.destroy_node()


if __name__ == '__main__':
	main()