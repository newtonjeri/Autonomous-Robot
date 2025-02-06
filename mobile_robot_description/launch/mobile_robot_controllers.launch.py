from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import ExecuteProcess

controllers_pkg = 'mobile_robot_description'
def generate_launch_description():
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
        parameters=[robot_controllers],
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
    # diff_drive_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=[
    #         "diff_drive_controller",
    #         "--param-file",
    #         robot_controllers,
    #         # "--controller-ros-args",
    #         # "-r /diff_drive_controller/cmd_vel:=/cmd_vel",
    #     ],
    #     output='screen',
    # )

    return LaunchDescription([
        control_node,
        joint_state_broadcaster,
        load_forward_velocity_controller,
        load_forward_position_controller,
        # diff_drive_spawner,
    ])