# Example to test the connection

from Client import RoboPy

robot = RoboPy(robot_type="ABB", host="127.0.0.1", port=5000)  # Creating a robot instance

# Connect robot
robot.connect()

#Get TCP
robot.get_position()
robot.get_joint_pos()
robot.gripper()
