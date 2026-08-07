from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    publish_rate_arg = DeclareLaunchArgument('publish_rate', default_value='1.0')
    topic_name_arg = DeclareLaunchArgument('topic_name', default_value='robot_status')
    # codes for Mile 2.5 task 2
    publisher_node = Node(
        package='student_robotics',
        executable='status_publisher_stretch',
        name='status_publisher',
        output='screen',
        parameters=[{
            'publish_rate': LaunchConfiguration('publish_rate'),
            'topic_name': LaunchConfiguration('topic_name'),
        }]
    )
    
    subscriber_node = Node(
        package='student_robotics',
        executable='status_subscriber',
        name='status_subscriber',
        output='screen',
        parameters=[{'topic_name': LaunchConfiguration('topic_name')}]
    )
    
    return LaunchDescription([publish_rate_arg, topic_name_arg, publisher_node, subscriber_node])