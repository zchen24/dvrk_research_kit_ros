/* -*- Mode: C++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*-    */
/* ex: set filetype=cpp softtabstop=4 shiftwidth=4 tabstop=4 cindent expandtab: */

/*
  Author(s):  Anton Deguet
  Created on: 2020-01-13

  (C) Copyright 2020 Johns Hopkins University (JHU), All Rights Reserved.

--- begin cisst license - do not edit ---

This software is provided "as is" under an open source license, with
no warranty.  The complete license can be found in license.txt and
http://www.cisst.org/cisst/license.txt.

--- end cisst license ---
*/

#include <cisst_ros_crtk/mtsCISSTToROS.h>
#include <cisst_ros_crtk/mtsROSToCISST.h>

#include <dvrk_arm_from_ros.h>

CMN_IMPLEMENT_SERVICES_DERIVED_ONEARG(dvrk_arm_from_ros,
                                      mtsROSBridge,
                                      mtsTaskPeriodicConstructorArg);

dvrk_arm_from_ros::dvrk_arm_from_ros(const std::string & componentName,
                                     const double periodInSeconds)
    : mtsROSBridge(componentName, periodInSeconds)
{
    Init();
}

dvrk_arm_from_ros::dvrk_arm_from_ros(const mtsTaskPeriodicConstructorArg & arg)
    : mtsROSBridge(arg.Name, arg.Period)
{
    Init();
}

void dvrk_arm_from_ros::Init(void)
{
    std::string ros_namespace = this->GetName();
    std::string interface_provided = this->GetName();

    AddPublisherFromCommandWrite<std::string, crtk_msgs::StringStamped>
        (interface_provided,
         "state_command",
         ros_namespace + "/state_command");

    AddPublisherFromCommandVoid
        (interface_provided,
         "Freeze",
         ros_namespace + "/freeze");

    AddPublisherFromCommandWrite<prmPositionCartesianSet, geometry_msgs::TransformStamped>
        (interface_provided,
         "servo_cp",
         ros_namespace + "/servo_cp");

    AddSubscriberToEventWrite<prmOperatingState, crtk_msgs::operating_state>
        (interface_provided, "operating_state",
         ros_namespace + "/operating_state");

    AddSubscriberToCommandRead<prmOperatingState, crtk_msgs::operating_state>
        (interface_provided, "operating_state",
         ros_namespace + "/operating_state");

    AddSubscriberToCommandRead<prmStateJoint, sensor_msgs::JointState>
        (interface_provided,
         "setpoint_js",
         ros_namespace + "/setpoint_js");

    AddSubscriberToCommandRead<prmPositionCartesianGet, geometry_msgs::TransformStamped>
        (interface_provided,
         "measured_cp",
         ros_namespace + "/measured_cp");

    AddSubscriberToCommandRead<mtsIntervalStatistics, cisst_msgs::mtsIntervalStatistics>
        (interface_provided,
         "period_statistics",
         ros_namespace + "/period_statistics");

    AddSubscriberToEventWrite<mtsMessage, std_msgs::String>
        (interface_provided, "error",
         ros_namespace + "/error");

    AddSubscriberToEventWrite<mtsMessage, std_msgs::String>
        (interface_provided, "warning",
         ros_namespace + "/warning");

    AddSubscriberToEventWrite<mtsMessage, std_msgs::String>
        (interface_provided, "status",
         ros_namespace + "/status");
}

// Configure is a virtual method, we can redefine it and have our own
// configuration
void dvrk_arm_from_ros::Configure(const std::string & CMN_UNUSED(filename))
{

}
