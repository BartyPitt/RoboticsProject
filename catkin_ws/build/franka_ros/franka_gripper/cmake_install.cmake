# Install script for directory: /home/user/catkin_ws/src/franka_ros/franka_gripper

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/user/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper/action" TYPE FILE FILES
    "/home/user/catkin_ws/src/franka_ros/franka_gripper/action/Grasp.action"
    "/home/user/catkin_ws/src/franka_ros/franka_gripper/action/Homing.action"
    "/home/user/catkin_ws/src/franka_ros/franka_gripper/action/Stop.action"
    "/home/user/catkin_ws/src/franka_ros/franka_gripper/action/Move.action"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper/msg" TYPE FILE FILES
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/GraspAction.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/GraspActionGoal.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/GraspActionResult.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/GraspActionFeedback.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/GraspGoal.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/GraspResult.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/GraspFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper/msg" TYPE FILE FILES
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/HomingAction.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/HomingActionGoal.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/HomingActionResult.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/HomingActionFeedback.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/HomingGoal.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/HomingResult.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/HomingFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper/msg" TYPE FILE FILES
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/StopAction.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/StopActionGoal.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/StopActionResult.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/StopActionFeedback.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/StopGoal.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/StopResult.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/StopFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper/msg" TYPE FILE FILES
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/MoveAction.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/MoveActionGoal.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/MoveActionResult.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/MoveActionFeedback.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/MoveGoal.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/MoveResult.msg"
    "/home/user/catkin_ws/devel/share/franka_gripper/msg/MoveFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper/msg" TYPE FILE FILES "/home/user/catkin_ws/src/franka_ros/franka_gripper/msg/GraspEpsilon.msg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper/cmake" TYPE FILE FILES "/home/user/catkin_ws/build/franka_ros/franka_gripper/catkin_generated/installspace/franka_gripper-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/user/catkin_ws/devel/include/franka_gripper")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/user/catkin_ws/devel/share/roseus/ros/franka_gripper")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/user/catkin_ws/devel/share/common-lisp/ros/franka_gripper")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/user/catkin_ws/devel/share/gennodejs/ros/franka_gripper")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/user/catkin_ws/devel/lib/python2.7/dist-packages/franka_gripper")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/user/catkin_ws/devel/lib/python2.7/dist-packages/franka_gripper")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/user/catkin_ws/build/franka_ros/franka_gripper/catkin_generated/installspace/franka_gripper.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper/cmake" TYPE FILE FILES "/home/user/catkin_ws/build/franka_ros/franka_gripper/catkin_generated/installspace/franka_gripper-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper/cmake" TYPE FILE FILES
    "/home/user/catkin_ws/build/franka_ros/franka_gripper/catkin_generated/installspace/franka_gripperConfig.cmake"
    "/home/user/catkin_ws/build/franka_ros/franka_gripper/catkin_generated/installspace/franka_gripperConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper" TYPE FILE FILES "/home/user/catkin_ws/src/franka_ros/franka_gripper/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfranka_gripper.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfranka_gripper.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfranka_gripper.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/user/catkin_ws/devel/lib/libfranka_gripper.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfranka_gripper.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfranka_gripper.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfranka_gripper.so"
         OLD_RPATH "/home/user/catkin_ws/src/libfranka/build:/opt/ros/melodic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfranka_gripper.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/franka_gripper/franka_gripper_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/franka_gripper/franka_gripper_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/franka_gripper/franka_gripper_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/franka_gripper" TYPE EXECUTABLE FILES "/home/user/catkin_ws/devel/lib/franka_gripper/franka_gripper_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/franka_gripper/franka_gripper_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/franka_gripper/franka_gripper_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/franka_gripper/franka_gripper_node"
         OLD_RPATH "/opt/ros/melodic/lib:/home/user/catkin_ws/devel/lib:/home/user/catkin_ws/src/libfranka/build:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/franka_gripper/franka_gripper_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/franka_gripper" TYPE DIRECTORY FILES "/home/user/catkin_ws/src/franka_ros/franka_gripper/include/franka_gripper/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper" TYPE DIRECTORY FILES "/home/user/catkin_ws/src/franka_ros/franka_gripper/launch")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/franka_gripper" TYPE DIRECTORY FILES "/home/user/catkin_ws/src/franka_ros/franka_gripper/config")
endif()

