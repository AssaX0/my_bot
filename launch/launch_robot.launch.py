import os

from launch import LaunchDescription

from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution
from launch_ros.substitutions import FindPackageShare

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

    lidar_spawner = IncludeLaunchDescription(
       IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('ydlidar_ros2_driver'),
                    'ydlidar_launch.py'
                ])
            ]),
            # launch_arguments={
            #     'turtlesim_ns': 'turtlesim2',
            #     'use_provided_red': 'True',
            #     'new_background_r': TextSubstitution(text=str(colors['background_r']))
            # }.items()
        ))


    return LaunchDescription([
        md25_spawner,
        camera_spawner,
        lidar_spawner
    ])