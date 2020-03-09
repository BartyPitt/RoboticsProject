// Generated by gencpp from file franka_control/SetLoad.msg
// DO NOT EDIT!


#ifndef FRANKA_CONTROL_MESSAGE_SETLOAD_H
#define FRANKA_CONTROL_MESSAGE_SETLOAD_H

#include <ros/service_traits.h>


#include <franka_control/SetLoadRequest.h>
#include <franka_control/SetLoadResponse.h>


namespace franka_control
{

struct SetLoad
{

typedef SetLoadRequest Request;
typedef SetLoadResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct SetLoad
} // namespace franka_control


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::franka_control::SetLoad > {
  static const char* value()
  {
    return "c9a8ec436164dd9cbc1e5e137d358e0b";
  }

  static const char* value(const ::franka_control::SetLoad&) { return value(); }
};

template<>
struct DataType< ::franka_control::SetLoad > {
  static const char* value()
  {
    return "franka_control/SetLoad";
  }

  static const char* value(const ::franka_control::SetLoad&) { return value(); }
};


// service_traits::MD5Sum< ::franka_control::SetLoadRequest> should match 
// service_traits::MD5Sum< ::franka_control::SetLoad > 
template<>
struct MD5Sum< ::franka_control::SetLoadRequest>
{
  static const char* value()
  {
    return MD5Sum< ::franka_control::SetLoad >::value();
  }
  static const char* value(const ::franka_control::SetLoadRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::franka_control::SetLoadRequest> should match 
// service_traits::DataType< ::franka_control::SetLoad > 
template<>
struct DataType< ::franka_control::SetLoadRequest>
{
  static const char* value()
  {
    return DataType< ::franka_control::SetLoad >::value();
  }
  static const char* value(const ::franka_control::SetLoadRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::franka_control::SetLoadResponse> should match 
// service_traits::MD5Sum< ::franka_control::SetLoad > 
template<>
struct MD5Sum< ::franka_control::SetLoadResponse>
{
  static const char* value()
  {
    return MD5Sum< ::franka_control::SetLoad >::value();
  }
  static const char* value(const ::franka_control::SetLoadResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::franka_control::SetLoadResponse> should match 
// service_traits::DataType< ::franka_control::SetLoad > 
template<>
struct DataType< ::franka_control::SetLoadResponse>
{
  static const char* value()
  {
    return DataType< ::franka_control::SetLoad >::value();
  }
  static const char* value(const ::franka_control::SetLoadResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // FRANKA_CONTROL_MESSAGE_SETLOAD_H