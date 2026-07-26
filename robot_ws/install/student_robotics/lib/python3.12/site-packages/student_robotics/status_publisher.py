import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class StatusPublisher(Node):
    def __init__(self):
        super().__init__('status_publisher')

        # publisher: topic name: 'robot_status', messsage type: String, queue size(Qos depth): 10
        self.publisher_ = self.create_publisher(String, 'robot_status', 10)  # create a publisher object that knows 
                                                                             # message type, topic name and Qos depth (queue size) for the topic
        
        # Timer: callback fires every 1.0 second -> 1Hz
        self.timer_period = 1.0 # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        self.sequence_number = 0
        self.start_time = time.time()

        self.get_logger().info('Status publisher node has started.') # Output log message to the console indicating that the node has started

    def timer_callback(self):
        elapsed_time = time.time() - self.start_time

        msg = String() # msg is also a object of the String message type, which is defined in the std_msgs package.

        """
         In the following expression, 'f' before the string literal indicates this is an f-string (formatted string literal). 
          It was introduced in Python 3.6 to make it easy to insert the values of variables or expressions directly into a string.

          Anything inside {} is treated as a Python expression. Python evaluates the expression and replaces it with its value.
        """
        msg.data = f'Robot is operational. Sequence number: {self.sequence_number}, Elapsed time: {elapsed_time:.2f} seconds'

        self.publisher_.publish(msg) # when 'publish(msg) executes,
        """
            the publisher:
                1. take the 'msg' object
                2. converts/serializes it into a format suitable for transmission over the ROS 2 
                        communication system
                3. sends it on the topic "robot_status"
                4. any subscribers(nodes) currently listening to the "robot_status" topic receives a copy

        """
        self.get_logger().info(f'Publishing: "{msg.data}"') # Output log message to the console 
                                                            # indicate the timer is callback and the message is published

        self.sequence_number += 1

def main(args=None):
    rclpy.init(args=args)
    node = StatusPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        """
        'finally' block is used for cleanup or guaranteed actions;
        it always executes after the try block, regardless of whether an exception was raised or not.
        """
        node.get_logger().info('Shutting down status publisher node.')
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
