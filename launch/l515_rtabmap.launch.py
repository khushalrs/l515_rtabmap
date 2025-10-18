#!/usr/bin/env python3

"""Launch RealSense L515 sensor together with RTAB-Map integration."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    """Return launch description running RealSense and RTAB-Map."""
    realsense_params_default = PathJoinSubstitution([
        FindPackageShare('l515_rtabmap'),
        'config',
        'realsense.yaml',
    ])

    realsense_params_arg = DeclareLaunchArgument(
        'realsense_params_file',
        default_value=realsense_params_default,
        description='Path to the RealSense parameters file.',
    )

    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('realsense2_camera'),
                'launch',
                'rs_launch.py',
            ])
        ),
        launch_arguments={
            'params_file': LaunchConfiguration('realsense_params_file'),
        }.items(),
    )

    rtabmap_delay_default = '8.0'

    rtabmap_delay_arg = DeclareLaunchArgument(
        'rtabmap_start_delay',
        default_value=rtabmap_delay_default,
        description='Seconds to wait before starting RTAB-Map.',
    )

    rtabmap_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rtabmap_launch'),
                'launch',
                'rtabmap.launch.py',
            ])
        ),
        launch_arguments={
            'rgb_topic': '/camera/color/image_raw',
            'depth_topic': '/camera/aligned_depth_to_color/image_raw',
            'camera_info_topic': '/camera/color/camera_info',
            'frame_id': 'camera_link',
            'approx_sync': 'true',
            'qos': '2',
        }.items(),
    )

    rtabmap_launch_delayed = TimerAction(
        period=LaunchConfiguration('rtabmap_start_delay'),
        actions=[rtabmap_launch],
    )

    return LaunchDescription([
        realsense_params_arg,
        rtabmap_delay_arg,
        realsense_launch,
        rtabmap_launch_delayed,
    ])
