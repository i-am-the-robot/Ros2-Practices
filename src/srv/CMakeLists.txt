cmake_minimum_required(VERSION 3.8)
project(my_interfaces)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)

# Generate service interfaces
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/OddEvenCheck.srv"
  "srv/AnglePic.srv"
)

# Install Python nodes from src/ folder
install(DIRECTORY images/
  DESTINATION share/${PROJECT_NAME}/images
  )
install(PROGRAMS
  src/service_server.py
  src/service_client.py
  src/anglePicC lient.py
  src/anglePicServer.py


  DESTINATION lib/${PROJECT_NAME}
)

ament_package()