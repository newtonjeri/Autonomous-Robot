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
    
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad", "--controller-manager", "/controller_manager"],
        output='screen',

    )

    ackermann_steering_controller = Node(
       package="controller_manager",
       executable="spawner",
       parameters=[{use_sim_time: True}],
       arguments=["ackermann_steering_cont"],
    )


    return LaunchDescription([
        declare_use_sim_time_arg,
        joint_state_broadcaster,
        ackermann_steering_controller,
    ])