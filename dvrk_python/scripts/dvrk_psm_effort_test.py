#!/usr/bin/env python

# Author: Anton Deguet
# Date: 2015-02-22

# (C) Copyright 2015-2020 Johns Hopkins University (JHU), All Rights Reserved.

# --- begin cisst license - do not edit ---

# This software is provided "as is" under an open source license, with
# no warranty.  The complete license can be found in license.txt and
# http://www.cisst.org/cisst/license.txt.

# --- end cisst license ---

# Start a single arm using
# > rosrun dvrk_robot dvrk_console_json -j <console-file>

# To communicate with the arm using ROS topics, see the python based example dvrk_arm_test.py:
# > rosrun dvrk_python dvrk_arm_test.py <arm-name>

import dvrk
import math
import sys
import rospy
import numpy
import argparse

if sys.version_info.major < 3:
    input = raw_input

# print with node id
def print_id(message):
    print('%s -> %s' % (rospy.get_caller_id(), message))

# example of application using arm.py
class example_application:

    # configuration
    def configure(self, robot_name):
        print_id('configuring dvrk_psm_test for %s' % robot_name)
        self.arm = dvrk.psm(robot_name)

    # homing example
    def home(self):
        print_id('starting home')
        self.arm.home()
        # get current joints just to set size
        goal = numpy.copy(self.arm.get_current_joint_position())
        # go to zero position, except for insert joint so we can't break tool in cannula
        goal.fill(0.0)
        goal[2] = 0.12
        self.arm.move_joint(goal, interpolate = True)

    # utility to position tool/camera deep enough before cartesian examples
    def prepare_cartesian(self):
        # make sure the camera is past the cannula and tool vertical
        goal = numpy.copy(self.arm.get_current_joint_position())
        if ((self.arm.name() == 'PSM1') or (self.arm.name() == 'PSM2') or (self.arm.name() == 'PSM3') or (self.arm.name() == 'ECM')):
            # set in position joint mode
            goal[0] = 0.0
            goal[1] = 0.0
            goal[2] = 0.12
            self.arm.move_joint(goal, interpolate = True)

    # effort jaw control example
    def jaw_effort(self):
        print_id('starting jaw effort')
        # get current joint torques just to set size
        effort_joint = numpy.copy(self.arm.get_current_joint_effort())
        effort_joint.fill(0.0)

        print_id('the jaws will open using a constant effort, the arm will go limp')
        input("    Press Enter to continue...")
        self.arm.set_effort_joint(effort_joint)
        self.arm.set_effort_jaw(0.02)

        print_id('the jaws will close using a constant effort, you can place a small object between the jaws now')
        input("    Press Enter to continue...")
        self.arm.set_effort_jaw(-0.02)

        print_id('the jaws will be released')
        input("    Press Enter to continue...")
        self.arm.set_effort_jaw(0.0)

    # effort joint control example
    def joint_effort(self):
        print_id('starting joint effort')
        # get current joint torques just to set size
        effort_joint = numpy.copy(self.arm.get_current_joint_effort())
        effort_joint.fill(0.0)

        print_id('the jaws and arm will go limp')
        input("    Press Enter to continue...")
        self.arm.set_effort_joint(effort_joint)
        self.arm.set_effort_jaw(0.0)

        print_id('hold the arm from the top and keep an hand on the Enter key, the arm will push on the first joint')
        input("    Press Enter to continue...")
        effort_joint[0] = -0.5
        self.arm.set_effort_joint(effort_joint)

        print_id('arm will now push in opposite direction')
        input("    Press Enter to continue...")
        effort_joint[0] = 0.5
        self.arm.set_effort_joint(effort_joint)

        print_id('arm will now apply sine wave forces on first two joints')
        input("    Press Enter to continue...")
        duration = 10  # seconds
        rate = 200 # aiming for 200 Hz
        samples = duration * rate
        # create a new goal starting with current position
        for i in range(samples):
            effort_joint[0] = 1.0 *  math.sin(i * math.radians(360.0) / samples)
            effort_joint[1] = 1.0 *  math.sin(i * math.radians(360.0) / samples)
            rospy.sleep(1.0 / rate)
            self.arm.set_effort_joint(effort_joint)

        print_id('arm will now go limp')
        input("    Press Enter to continue...")
        effort_joint.fill(0.0)
        self.arm.set_effort_joint(effort_joint)

    # wrench and jaw effort control example
    def wrench_jaw_effort(self):
        print_id('starting wrench jaw effort')
        # get current joint torques just to set size
        effort_joint = numpy.copy(self.arm.get_current_joint_effort())
        effort_joint.fill(0.0)

        print_id('the jaws will open and arm will go limp')
        input("    Press Enter to continue...")
        self.arm.set_effort_joint(effort_joint)
        self.arm.set_effort_jaw(0.02)

        print_id('the jaws will close using a constant effort, you can place a small object between the jaws now')
        input("    Press Enter to continue...")
        self.arm.set_effort_jaw(-0.02)

        print_id('hold the arm close to the tool tip and keep an hand on the Enter key, the arm will push down (Z direction)')
        input("    Press Enter to continue...")
        self.arm.set_wrench_body_orientation_absolute(True)
        self.arm.set_wrench_body_force((0.0, 0.0, 2.0))

        print_id('the jaws will be released')
        input("    Press Enter to continue...")
        self.arm.set_effort_jaw(0.0)

        print_id('arm will now go limp')
        input("    Press Enter to continue...")
        self.arm.set_wrench_body_force((0.0, 0.0, 0.0))

    # main method
    def run(self):
        self.home()
        self.jaw_effort()
        self.joint_effort()
        self.wrench_jaw_effort()

if __name__ == '__main__':
    # ros init node so we can use default ros arguments (e.g. __ns:= for namespace)
    rospy.init_node('dvrk_arm_test')
    # strip ros arguments
    argv = rospy.myargv(argv=sys.argv)

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--arm', type=str, required=True,
                        choices=['PSM1', 'PSM2', 'PSM3'],
                        help = 'arm name corresponding to ROS topics without namespace.  Use __ns:= to specify the namespace')
    args = parser.parse_args(argv[1:]) # skip argv[0], script name

    application = example_application()
    application.configure(args.arm)
    application.run()
