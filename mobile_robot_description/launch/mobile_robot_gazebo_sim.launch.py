import os
from launch import LaunchDescription
from launch.substitutions import (
    Command,
    PathJoinSubstitution,
    FindExecutable,
    LaunchConfiguration
)
from launch_ros.substitutions import FindPackageShare

from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import (
    get_package_share_directory,
    get_package_prefix,
)
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument
)
from launch_ros.actions import (
    Node,
    SetParameter,
)


description_pkg = "mobile_robot_description"
xacro_filename = "mobile_robot.urdf.xacro"

def generate_launch_description():
    # Path to xacro file
    xacro_file = os.path.join(get_package_share_directory(description_pkg), 'urdf', xacro_filename)

    world_file = PathJoinSubstitution([description_pkg, "worlds", "custom_world.sdf"])
    world_cfg = LaunchConfiguration("world")
    declare_world_arg = DeclareLaunchArgument(
        "world", default_value=["-r ", world_file], description="SDF world file"
    )

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
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    get_package_share_directory("ros_gz_sim"),
                    "launch",
                    "gz_sim.launch.py",
                ]
            )
        ),
        launch_arguments={"gz_args": world_cfg}.items(),
    )
    
    # gazebo_ros_spawner	
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

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    # Bridge
    bridge_params = os.path.join(get_package_share_directory(description_pkg),'config','gz_bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ]
    )

    return LaunchDescription([
        # Sets use_sim_time for all nodes started below (doesn't work for nodes started from Gazebo)
        SetParameter(name="use_sim_time", value=True),
        declare_world_arg,
        robot_state_publisher,
        gz_sim,
        start_gazebo_ros_spawner_cmd,
        diff_drive_spawner,
    ])