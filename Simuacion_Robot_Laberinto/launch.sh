#python3 generate_spawn_origin.py
colcon build
source install/setup.bash
ros2 launch modelo_robot gazebo.launch.py
