#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_interfaces.srv import AnglePic
import os

VALID_ANGLES = [-30, -15, 0, 15, 30]
IMAGES_DIR = os.path.expanduser('~/ros2_ws/src/srv/images')

class AngleImageServer(Node):
    def __init__(self):
        super().__init__('angle_image_server')
        self.srv = self.create_service(
            AnglePic,
            'angle_image',
            self.handle_request
        )
        self.get_logger().info('Angle Image Server is running...')
        self.get_logger().info(f'Images directory: {IMAGES_DIR}')

    def handle_request(self, request, response):
        angle = int(request.angle)
        self.get_logger().info(f'Received angle: {angle}')

        if angle not in VALID_ANGLES:
            response.success    = False
            response.image_path = ''
            response.message    = (
                f'Angle {angle} not supported. '
                f'Valid angles: {VALID_ANGLES}'
            )
            return response

        image_file = os.path.join(IMAGES_DIR, f'{angle}.png')

        if not os.path.exists(image_file):
            response.success    = False
            response.image_path = ''
            response.message    = f'Image file not found: {image_file}'
            return response

        response.success    = True
        response.image_path = image_file
        response.message    = f'Image found for angle {angle}'
        self.get_logger().info(f'Returning: {image_file}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AngleImageServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()