import launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    tcp_node = Node(
        package='plc',
        executable='tcp_node',
        name='tcp_node',
        output='screen'
    )

    process_node = Node(
        package='plc',
        executable='process_node',
        name='process_node',
        output='screen'
    )

    return LaunchDescription([
        process_node,
        tcp_node
    ])

