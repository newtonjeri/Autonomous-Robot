import os
from launch import LaunchDescription
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
    FindExecutable
)
from launch_ros.substitutions import FindPackageShare

from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import (
    get_package_share_directory,
    get_package_prefix,
)
from launch.actions import (
    AppendEnvironmentVariable,
    IncludeLaunchDescription,
)

from launch_ros.actions import Node

description_pkg = "mobile_robot_description"
xacro_filename = "mobile_robot.urdf.xacro"
def generate_launch_description():

    # Path to xacro file
    xacro_file = os.path.join(get_package_share_directory(description_pkg), 'urdf', xacro_filename)
    world = os.path.join(get_package_share_directory(description_pkg), 'worlds', 'custom_world.sdf')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [
                    FindPackageShare(description_pkg),
                    "urdf",
                    xacro_filename,
                ]
            ),
        ]
    )
    robot_description = {"robot_description": robot_description_content}

    # Environment Variable
    os.environ["GZ_SIM_RESOURCE_PATH"] = os.path.join(get_package_prefix(description_pkg), "share")
    


    # Environment Variable
    # set_env_vars_resources = AppendEnvironmentVariable(
    #         'GZ_SIM_RESOURCE_PATH',
    #         os.path.join(get_package_share_directory(description_pkg)))

    # robot_state_publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
        arguments=[xacro_file],
    )

    # gazebo
    gz_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world], 'on_exit_shutdown': 'true'}.items()
    )
    
    start_gazebo_ros_spawner_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', "Mobile_Robot",
            "-topic",
            "robot_description",
            '-x', '0',
            '-y', '0',	
            '-z', '0.2'
        ],
        output='screen',
    )

            

    return LaunchDescription([
        # set_env_vars_resources,
        robot_state_publisher,
        gz_cmd,
        start_gazebo_ros_spawner_cmd,
    ])