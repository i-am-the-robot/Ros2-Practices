#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_interfaces.srv import AnglePic
import cv2

class AngleImageClient(Node):
    def __init__(self):
        super().__init__('angle_image_client')
        self.client = self.create_client(AnglePic, 'angle_image')

        self.get_logger().info('Waiting for angle_image server...')
        while not self.client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('Server not available, waiting...')
        self.get_logger().info('Server connected!')

    def send_request(self, angle):
        request       = AnglePic.Request()
        request.angle = float(angle)
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result()

    def show_image(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            self.get_logger().error(f'Could not load image: {image_path}')
            return
        cv2.imshow('Angle Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def main(args=None):
    rclpy.init(args=args)
    node = AngleImageClient()

    try:
        while True:
            user_input = input('\nEnter angle (-30, -15, 0, 15, 30) or q to quit: ')

            if user_input.lower() == 'q':
                break

            try:
                angle = float(user_input)
            except ValueError:
                print('Please enter a valid number!')
                continue

            response = node.send_request(angle)

            if response.success:
                print(f'Success: {response.message}')
                node.show_image(response.image_path)
            else:
                print(f'Failed: {response.message}')

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()