import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class StatusSubscriber(Node):
    def __init__(self):
        super().__init__('status_subscriber')
        self.declare_parameter('topic_name', 'robot_status') # Declare a parameter for the topic name
        topic_name = self.get_parameter('topic_name').get_parameter_value().string_value
        
        # subscription: topic name: 'robot_status', message type: callback, queue size(Qos depth):
        self.subscription = self.create_subscription(String, topic_name,
            self.listener_callback, 10)
        """
         This line alone is what matters. By assigning the returned subscription object to self.subscription (an instance attribute), 
         it stays referenced as long as the node object exists.

         if you instead written: subscription = self.create_subscription(...)  # local variable
         Python's garbage collector could reclaim that object once '__init__' finishes,
         since nothing outside the method holds a reference to it anymore — and the callback would silently stop firing.
         So the assignment-to-'self' is the functional part.
        """

        self.subscription
        """
         a no-op: it just evaluates the attribute and throws the result away.
         it functions more like an inline comment: a visual signal to a human reader (or to some IDEs that flag "attribute assigned
          but never read elsewhere in the file") saying "yes, this attribute is intentionally kept around even though I never call 
          self.subscription again.
        """

        self.get_logger().info('Status Subscriber Node has started.')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received status message: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = StatusSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()