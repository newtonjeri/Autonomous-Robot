from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import ExecuteProcess, DeclareLaunchArgument

controllers_pkg = 'mobile_robot_description'
def generate_launch_description():

   
    use_sim_time = LaunchConfiguration("use_sim_time")
    declare_use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time", default_value="true", description="Use simulation time"
    )
    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare(controllers_pkg),
            "config",
            "controllers.yaml",
        ]
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_controllers, {use_sim_time: True}], 
        output="both",
    )
        
    
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad", "--controller-manager", "/controller_manager"],
        output='screen',

    )
    load_forward_velocity_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'forward_velocity_controller'],
        output='screen'
    )

    load_forward_position_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'forward_position_controller'],
        output='screen'
    )

    # ackermann_steering_controller = ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
    #          'ackermann_steering_cont'],
    #     output='screen'
    # )

    ackermann_steering_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "ackermann_steering_cont",
            "--param-file",
            robot_controllers
        ],
        parameters=[{use_sim_time: True}],
        output='screen',
    )

    # ackermann_steering_controller = Node(
    #    package="controller_manager",
    #    executable="spawner",
    #    parameters=[{use_sim_time: True}],
    #    arguments=["ackermann_steering_cont"],
    # )
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diff_drive_controller",
            "--param-file",
            robot_controllers,
            # "--controller-ros-args",
            # "-r /diff_drive_controller/cmd_vel:=/cmd_vel",
        ],
        output='screen',
    )

    return LaunchDescription([
        declare_use_sim_time_arg,
        control_node,
        joint_state_broadcaster,
        # load_forward_velocity_controller,
        # load_forward_position_controller,
        # ackermann_steering_controller,
        diff_drive_spawner,
    ])