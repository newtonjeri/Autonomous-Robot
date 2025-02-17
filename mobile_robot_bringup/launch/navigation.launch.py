import os
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    nav2_localization = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("mobile_robot_description"),
            "launch",
            "localization_launch.py"
        )
    )

    nav2 = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("mobile_robot_description"),
            "launch",
            "navigation_launch.py"
        )
    )

    ackermann_twist_publisher = Node(
        package="mobile_robot_description",
        executable="ackermann_twist_publisher.py",
        name="ackermann_twist_publisher_node",
        output="screen"
    )
    
    return LaunchDescription([
        nav2_localization,
        nav2,
        ackermann_twist_publisher
    ])