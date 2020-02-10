// Generated by gencpp from file franka_gripper/MoveFeedback.msg
// DO NOT EDIT!


#ifndef FRANKA_GRIPPER_MESSAGE_MOVEFEEDBACK_H
#define FRANKA_GRIPPER_MESSAGE_MOVEFEEDBACK_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace franka_gripper
{
template <class ContainerAllocator>
struct MoveFeedback_
{
  typedef MoveFeedback_<ContainerAllocator> Type;

  MoveFeedback_()
    {
    }
  MoveFeedback_(const ContainerAllocator& _alloc)
    {
  (void)_alloc;
    }







  typedef boost::shared_ptr< ::franka_gripper::MoveFeedback_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::franka_gripper::MoveFeedback_<ContainerAllocator> const> ConstPtr;

}; // struct MoveFeedback_

typedef ::franka_gripper::MoveFeedback_<std::allocator<void> > MoveFeedback;

typedef boost::shared_ptr< ::franka_gripper::MoveFeedback > MoveFeedbackPtr;
typedef boost::shared_ptr< ::franka_gripper::MoveFeedback const> MoveFeedbackConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::franka_gripper::MoveFeedback_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::franka_gripper::MoveFeedback_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace franka_gripper

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'actionlib_msgs': ['/opt/ros/melodic/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'franka_gripper': ['/home/medad/RoboticsProject/catkin_ws/devel/share/franka_gripper/msg', '/home/medad/RoboticsProject/catkin_ws/src/franka_ros/franka_gripper/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::franka_gripper::MoveFeedback_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::franka_gripper::MoveFeedback_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::franka_gripper::MoveFeedback_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::franka_gripper::MoveFeedback_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::franka_gripper::MoveFeedback_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::franka_gripper::MoveFeedback_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::franka_gripper::MoveFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const ::franka_gripper::MoveFeedback_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd41d8cd98f00b204ULL;
  static const uint64_t static_value2 = 0xe9800998ecf8427eULL;
};

template<class ContainerAllocator>
struct DataType< ::franka_gripper::MoveFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "franka_gripper/MoveFeedback";
  }

  static const char* value(const ::franka_gripper::MoveFeedback_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::franka_gripper::MoveFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"\n"
;
  }

  static const char* value(const ::franka_gripper::MoveFeedback_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::franka_gripper::MoveFeedback_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream&, T)
    {}

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MoveFeedback_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::franka_gripper::MoveFeedback_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream&, const std::string&, const ::franka_gripper::MoveFeedback_<ContainerAllocator>&)
  {}
};

} // namespace message_operations
} // namespace ros

#endif // FRANKA_GRIPPER_MESSAGE_MOVEFEEDBACK_H
