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

    world_file = PathJoinSubstitution([description_pkg, "worlds", "obstacles_world.sdf"])
    world_cfg = LaunchConfiguration("world")
    use_sim_time = LaunchConfiguration("use_sim_time")

    declare_world_arg = DeclareLaunchArgument(
        "world", default_value=["-r ", world_file], description="SDF world file"
    )
    declare_use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time", default_value="true", description="Use simulation time"
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

    robot_description = {"robot_description": robot_description_content, use_sim_time: True}

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
        launch_arguments={'gz_args': ['-r ', world_cfg], 'on_exit_shutdown': 'true'}.items()
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
    
    # Bridge
    bridge_params = os.path.join(get_package_share_directory(description_pkg),'config','gz_bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ],
        output='screen'
    )

    rviz2 = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', PathJoinSubstitution([FindPackageShare("mobile_robot_description"), "rviz", "mobile_robot.rviz"])],
            output='screen'
        )
    
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )  
    
   
    return LaunchDescription([
        declare_use_sim_time_arg,
        declare_world_arg,
        robot_state_publisher,
        gz_sim,
        start_gazebo_ros_spawner_cmd,
        ros_gz_bridge,
        rviz2
    ])