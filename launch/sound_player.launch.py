from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    package_name: str = "sound_player"
    executable_name: str = "sound_player"

    sound_player = Node(
        package=package_name,
        executable=executable_name,
        name=executable_name,
        output="screen",
        parameters=[],
        arguments=["--ros-args", "--log-level", "debug"],
    )
    # create and return launch description object
    return LaunchDescription(
        [
            sound_player,
        ]
    )

