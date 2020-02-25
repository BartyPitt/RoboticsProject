// Generated by gencpp from file franka_gripper/GraspGoal.msg
// DO NOT EDIT!


#ifndef FRANKA_GRIPPER_MESSAGE_GRASPGOAL_H
#define FRANKA_GRIPPER_MESSAGE_GRASPGOAL_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <franka_gripper/GraspEpsilon.h>

namespace franka_gripper
{
template <class ContainerAllocator>
struct GraspGoal_
{
  typedef GraspGoal_<ContainerAllocator> Type;

  GraspGoal_()
    : width(0.0)
    , epsilon()
    , speed(0.0)
    , force(0.0)  {
    }
  GraspGoal_(const ContainerAllocator& _alloc)
    : width(0.0)
    , epsilon(_alloc)
    , speed(0.0)
    , force(0.0)  {
  (void)_alloc;
    }



   typedef double _width_type;
  _width_type width;

   typedef  ::franka_gripper::GraspEpsilon_<ContainerAllocator>  _epsilon_type;
  _epsilon_type epsilon;

   typedef double _speed_type;
  _speed_type speed;

   typedef double _force_type;
  _force_type force;





  typedef boost::shared_ptr< ::franka_gripper::GraspGoal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::franka_gripper::GraspGoal_<ContainerAllocator> const> ConstPtr;

}; // struct GraspGoal_

typedef ::franka_gripper::GraspGoal_<std::allocator<void> > GraspGoal;

typedef boost::shared_ptr< ::franka_gripper::GraspGoal > GraspGoalPtr;
typedef boost::shared_ptr< ::franka_gripper::GraspGoal const> GraspGoalConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::franka_gripper::GraspGoal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::franka_gripper::GraspGoal_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace franka_gripper

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'actionlib_msgs': ['/opt/ros/melodic/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg'], 'franka_gripper': ['/home/user/catkin_ws/devel/share/franka_gripper/msg', '/home/user/catkin_ws/src/franka_ros/franka_gripper/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::franka_gripper::GraspGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::franka_gripper::GraspGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::franka_gripper::GraspGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::franka_gripper::GraspGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::franka_gripper::GraspGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::franka_gripper::GraspGoal_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::franka_gripper::GraspGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "627a0f0b10ad0c919fbd62b0b3427e63";
  }

  static const char* value(const ::franka_gripper::GraspGoal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x627a0f0b10ad0c91ULL;
  static const uint64_t static_value2 = 0x9fbd62b0b3427e63ULL;
};

template<class ContainerAllocator>
struct DataType< ::franka_gripper::GraspGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "franka_gripper/GraspGoal";
  }

  static const char* value(const ::franka_gripper::GraspGoal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::franka_gripper::GraspGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n\
float64 width # [m]\n\
GraspEpsilon epsilon\n\
float64 speed # [m/s]\n\
float64 force # [N]\n\
\n\
================================================================================\n\
MSG: franka_gripper/GraspEpsilon\n\
float64 inner # [m]\n\
float64 outer # [m]\n\
";
  }

  static const char* value(const ::franka_gripper::GraspGoal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::franka_gripper::GraspGoal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.width);
      stream.next(m.epsilon);
      stream.next(m.speed);
      stream.next(m.force);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GraspGoal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::franka_gripper::GraspGoal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::franka_gripper::GraspGoal_<ContainerAllocator>& v)
  {
    s << indent << "width: ";
    Printer<double>::stream(s, indent + "  ", v.width);
    s << indent << "epsilon: ";
    s << std::endl;
    Printer< ::franka_gripper::GraspEpsilon_<ContainerAllocator> >::stream(s, indent + "  ", v.epsilon);
    s << indent << "speed: ";
    Printer<double>::stream(s, indent + "  ", v.speed);
    s << indent << "force: ";
    Printer<double>::stream(s, indent + "  ", v.force);
  }
};

} // namespace message_operations
} // namespace ros

#endif // FRANKA_GRIPPER_MESSAGE_GRASPGOAL_H
