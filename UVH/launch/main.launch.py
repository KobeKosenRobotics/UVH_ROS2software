from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # launchの構成を示すLaunchDescription型の変数の定義
    ld = LaunchDescription()

    # publisher nodeを、"talker_renamed1"という名前で定義
    UVH = Node(
        package='UVH',
        executable='UVH',
        output='screen',
        prefix="xterm -e"
    )

    # publisher nodeを、"talker_renamed2"という名前で定義
    micro_ros_agent = Node(
        package='micro_ros_agent',
        executable='micro_ros_agent',
        arguments = ['serial', '--dev', '/dev/ttyACM0'],
        output='screen',
        prefix="xterm -e"
    )

    # LaunchDescriptionに、起動したいノードを追加する
    ld.add_action(micro_ros_agent)
    ld.add_action(UVH)

    # launch構成を返すようにする
    return ld
