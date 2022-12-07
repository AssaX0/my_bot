import os

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    md25_spawner = Node(
            package='my_package',
            namespace='my_bot',
            executable='md25_drive_node',
            name='driver'
    )

    camera_spawner = Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            output='screen',
            parameters=[{
                'image_size': [1920,1080],
                'camera_frame_id': 'camera_link_optical'
                }]
    )

    # Für Lidar
    share_dir = get_package_share_directory('ydlidar_ros2_driver')
    parameter_file = LaunchConfiguration('params_file')
    node_name = 'ydlidar_ros2_driver_node'

    params_declare = DeclareLaunchArgument('params_file',
                                           default_value=os.path.join(
                                               share_dir, 'params', 'ydlidar.yaml'),
                                           description='FPath to the ROS2 parameters file to use.')

    driver_node = LifecycleNode(package='ydlidar_ros2_driver',
                                node_executable='ydlidar_ros2_driver_node',
                                node_name='ydlidar_ros2_driver_node',
                                output='screen',
                                emulate_tty=True,
                                parameters=[parameter_file],
                                node_namespace='/',
                                )
    tf2_node = Node(package='tf2_ros',
                    node_executable='static_transform_publisher',
                    node_name='static_tf_pub_laser',
                    arguments=['0', '0', '0.02','0', '0', '0', '1','base_link','laser_frame'],
                    )

    return LaunchDescription([
        md25_spawner,
        camera_spawner,
        params_declare,
        driver_node,
        tf2_node,
    ])