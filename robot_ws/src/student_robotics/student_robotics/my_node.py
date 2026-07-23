"""
rclpy is the Python client library for ROS 2 (Robot Operating System 2). 
It allows you to write ROS 2 applications (called nodes) in Python.

with rclpy you can:
    ● Create and manage ROS 2 nodes that can communicate with other nodes in the ROS 2 ecosystem
    ● Publish messages to topics
    ● Subscribe to topics
    ● Provide and call services
    ● create and use actions
    ● Set timers
    ● Access paraeters
    ● Interact with the ROS 2 communication system
"""
"""
 Common rclpy functions:
    ● rclpy.init(args=None): Initializes the ROS 2 client library. This function must be called before any other rclpy functions are used. 
       It sets up the necessary resources for communication with the ROS 2 system.
    ● rclpy.shutdown(): Shuts down the ROS 2 client Library. This function should be called when your node is done using ROS 2 resources. 
       It cleans up any resources that were allocated during initialization.
    ● rclpy.spin(node): enters a loop that keeps the node alive and responsive to incoming messages, service requests, and other events.
    ● Node: base class for creating ROS 2 nodes. It provides methods for publishing and subscribing to topics, 
        providing and calling services, setting timers, and accessing parameters.
    ● create_publisher(msg_type, topic_name, qos_profile): creates a publisher for a specific message type and topic.
    ● create_subscription(msg_type, topic_name, callback, qos_profile): creates a subscription to a specific message type and topic,
       with a callback function that is called when a message is received.
    ● create_timer(timer_period_sec, callback): creates a timer that calls a specified callback function at a specified interval.
    ● get_logger(): returns a logger object that can be used to log messages at different severity levels (info, warning, error, etc.).
"""
import rclpy
from rclpy.node import Node


class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')  # In Python, "super()"" is a built-in function that gives you access to methods and 
                                      #attributes of a parent (superclass) from within a child (subclass).

                                     # super().__init__(), Calls the parent class's constructor.
        self.get_logger().info('my_node has started') # Output log message to the console indicating that the node has started

def main(args=None):
    rclpy.init(args=args)  # Initialize the ROS 2 client library. This function must be called before any other rclpy_functions are used.
                           # It sets up the necessary resources for communication with the ROS 2 system.
    node = MyNode()
    try:
        rclpy.spin(node)      # keeps the node running and responsive to incoming messages, service requests, and other events.
    except KeyboardInterrupt:
           pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()  # shut down the ROS 2 client library. This function should be called when your nod is done using ROS 2 resources.
                              # It cleans up any resources that were allocated during initialization.

if __name__ == '__main__':
    main()
