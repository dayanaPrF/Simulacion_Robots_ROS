#No descomentar la siguiente linea
#python3 generate_default_values.py

#Comandos para compilar el proyecto entero
colcon build
source install/setup.bash

#Comando para visualizar solo el modelo en Rviz (Descomentar solo si se requiere)
#ros2 launch robot display.launch.py

#Comando para visualizar modelo en gazebo
ros2 launch robot gazebo.launch.py