#!/bin/bash

CURRENT_PATH=$(cd $(dirname $0);pwd)
cd $CURRENT_PATH
sudo apt update
sudo apt install -y python3-vcstool
ls
vcs import depend < depend_packages.repos --recursive
cd ..
rosdep install -i -y --from-paths .
sudo apt update && rosdep update
rosdep install -i -y --from-paths .
sudo apt-get install python3-pip
colcon build
source install/setup.bash
cd src/depend
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
source install/local_setup.bash
cd ..
colcon build
source install/setup.bash
colcon build
source install/setup.bash