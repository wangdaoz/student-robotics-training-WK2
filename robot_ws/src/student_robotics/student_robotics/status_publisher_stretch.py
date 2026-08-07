import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rcl_interfaces.msg import SetParametersResult
import time

class StatusPublisher(Node):
    def __init__(self):
        super().__init__('status_publisher')
        
        # Declare parameters for publish rate and topic name for Mile 2.5-task 2
        self.declare_parameter('publish_rate', 1.0)
        self.declare_parameter('topic_name', 'robot_status') 

        publish_rate = self.get_parameter('publish_rate').get_parameter_value().double_value
        while publish_rate <= 0.0:
            self.get_logger().warn('publish_rate must be greater than 0. Please input a valid value for publish_rate!')
            publish_rate = float(input('Enter a valid publish_rate (greater than 0): '))
        topic_name = self.get_parameter('topic_name').get_parameter_value().string_value

        self.publisher_ = self.create_publisher(String, topic_name, 10)
        timer_period = 1.0 / publish_rate
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.sequence_number = 0
        self.start_time = time.time()

        # Register the callback that fires whenever a parameter is set
        self.add_on_set_parameters_callback(self.parameter_callback)

        self.get_logger().info(f'Status publisher started at {publish_rate} Hz.')

    def timer_callback(self):
        elapsed = time.time() - self.start_time
        msg = String()
        msg.data = f'seq={self.sequence_number}, elapsed={elapsed:.2f}s'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.sequence_number += 1

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'publish_rate':
                if param.value <= 0.0:
                    # Reject invalid values; node keeps the old rate
                    return SetParametersResult(
                        successful=False,
                        reason='publish_rate must be greater than 0'
                    )

                # Destroy the old timer and create a new one at the new rate
                self.destroy_timer(self.timer)
                self.timer = self.create_timer(1.0 / param.value, self.timer_callback)
                self.get_logger().info(f'publish_rate changed to {param.value} Hz.')

            elif param.name == 'topic_name':
                if not param.value:
                    return SetParametersResult(successful=False, reason='topic_name must not be empty')
                self.destroy_publisher(self.publisher_)
                self.publisher_ = self.create_publisher(String, param.value, 10)
                self.get_logger().info(f'topic_name changed to "{param.value}".')

        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    node = StatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info('Shutting down status publisher.')
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()