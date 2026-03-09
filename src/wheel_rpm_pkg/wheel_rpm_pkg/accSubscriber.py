import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import math

WHEEL_RADIUS_M = 0.05  # Must match publisher (metres)


class AccelerationSubscriber(Node):
    """
    Subscribes to /wheel_rpm (Float64) and computes:
      - Angular velocity (rad/s)
      - Linear velocity (m/s)
      - Linear acceleration (m/s²) via finite differencing
    """

    def __init__(self):
        super().__init__('acceleration_subscriber')

        # Subscribe to the RPM topic
        self.subscription = self.create_subscription(
            Float64,
            'wheel_rpm',
            self.rpm_callback,
            10
        )

        # State for derivative calculation
        self._prev_velocity_ms  = None
        self._prev_time         = None

        self.get_logger().info(
            'AccelerationSubscriber ready. Listening on /wheel_rpm...'
        )

    def rpm_callback(self, msg: Float64):
        """
        Called every time a new RPM message arrives.
        Computes angular velocity, linear velocity, and acceleration.
        """
        rpm        = msg.data
        now        = self.get_clock().now()

        # ── Step 1: RPM → Angular velocity ──────────────────
        omega_rad_s = rpm * (2 * math.pi) / 60.0

        # ── Step 2: Angular velocity → Linear velocity ──────
        velocity_ms = omega_rad_s * WHEEL_RADIUS_M

        # ── Step 3: Δv/Δt → Linear acceleration ────────────
        accel_ms2 = 0.0
        if self._prev_velocity_ms is not None and self._prev_time is not None:
            dt = (now - self._prev_time).nanoseconds * 1e-9
            if dt > 1e-6:  # guard against division by near-zero
                accel_ms2 = (velocity_ms - self._prev_velocity_ms) / dt

        # ── Update state ────────────────────────────────────
        self._prev_velocity_ms = velocity_ms
        self._prev_time        = now

        # ── Log results ─────────────────────────────────────
        self.get_logger().info(
            f'\n'
            f'  RPM          : {rpm:.2f} rev/min\n'
            f'  Angular vel  : {omega_rad_s:.4f} rad/s\n'
            f'  Linear vel   : {velocity_ms:.4f} m/s\n'
            f'  Acceleration : {accel_ms2:.4f} m/s²'
        )


def main(args=None):
    rclpy.init(args=args)
    node = AccelerationSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()