import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math
import time

# ─────────────────────────────────────────────
# Configuration — adjust to match your robot
# ─────────────────────────────────────────────
TICKS_PER_REVOLUTION = 500   # Encoder resolution
WHEEL_RADIUS_M       = 0.05  # Wheel radius in metres (5 cm)
PUBLISH_RATE_HZ      = 10    # Publisher frequency


class WheelRpmPublisher(Node):
    """
    Simulates reading wheel encoder ticks and publishes
    calculated RPM to the /wheel_rpm topic.
    """

    def __init__(self):
        super().__init__('wheel_rpm_publisher')

        # Publisher: topic name, message type, queue size
        self.publisher_ = self.create_publisher(
            Float64, 'wheel_rpm', 10
        )

        # Timer fires at PUBLISH_RATE_HZ
        timer_period = 1.0 / PUBLISH_RATE_HZ
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Simulated encoder state
        self._tick_count       = 0
        self._last_tick_time   = self.get_clock().now()
        self._simulated_speed  = 1.0  # rad/s — change to simulate motor

        self.get_logger().info(
            f'WheelRpmPublisher started. '
            f'Ticks/rev={TICKS_PER_REVOLUTION}, '
            f'Wheel radius={WHEEL_RADIUS_M}m'
        )

    def _simulate_encoder_ticks(self) -> int:
        """
        Simulate encoder ticks accumulated since last call.
        In a real robot, replace this with actual encoder reads.
        """
        now = self.get_clock().now()
        dt  = (now - self._last_tick_time).nanoseconds * 1e-9  # seconds

        # Simulate slowly accelerating wheel
        self._simulated_speed += 0.05  # increase rad/s each tick
        self._simulated_speed  = min(self._simulated_speed, 10.0)

        # ticks = (speed_rad_s / 2π) * ticks_per_rev * dt
        ticks = int(
            (self._simulated_speed / (2 * math.pi))
            * TICKS_PER_REVOLUTION * dt
        )
        self._last_tick_time = now
        return ticks

    def timer_callback(self):
        """Called at PUBLISH_RATE_HZ. Computes RPM and publishes."""
        now  = self.get_clock().now()
        dt   = (now - self._last_tick_time).nanoseconds * 1e-9

        if dt <= 0:
            return

        new_ticks      = self._simulate_encoder_ticks()
        ticks_per_sec  = new_ticks / dt if dt > 0 else 0.0

        # RPM = (ticks/sec ÷ ticks/rev) × 60
        rpm = (ticks_per_sec / TICKS_PER_REVOLUTION) * 60.0

        msg       = Float64()
        msg.data  = rpm
        self.publisher_.publish(msg)

        self.get_logger().info(f'Published RPM: {rpm:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = WheelRpmPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()