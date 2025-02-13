# Example to test the connection

from Client import RoboPy

robot = RoboPy(robot_type="Fanuc", host="127.0.0.1", port=18736)  # Creating a robot instance

# Connect robot
robot.connect()

#Get TCP
robot.get_position()
robot.get_joint_pos()
