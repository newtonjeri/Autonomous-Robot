import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, ExecuteProcess
from ament_index_python.packages import get_package_share_directory
from launch.event_handlers import OnProcessExit

def generate_launch_description():
    # Path to the Gazebo simulation launch file
    gz_sim_launch_file = os.path.join(
        get_package_share_directory("mobile_robot_description"),
        "launch",
        "mobile_robot_gazebo_sim.launch.py"
    )

    # Path to the controllers launch file
    controllers_launch_file = os.path.join(
        get_package_share_directory("mobile_robot_description"),
        "launch",
        "mobile_robot_controllers.launch.py"
    )

    # Launch Gazebo simulation using ExecuteProcess
    gz_sim = ExecuteProcess(
        cmd=["ros2", "launch", gz_sim_launch_file, "is_sim_time:=true"],
        output="screen"
    )

    # Launch controllers using IncludeLaunchDescription
    controllers = IncludeLaunchDescription(
        controllers_launch_file,
        launch_arguments={"is_sim_time": "false"}.items()
    )

    # Event handler to launch controllers after Gazebo simulation exits
    launch_controllers_after_gz_sim = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=gz_sim,
            on_exit=[controllers]
        )
    )

    return LaunchDescription([
        gz_sim,
        controllers,
        # launch_controllers_after_gz_sim
    ])