# Example usage to test the connection

from Client import RoboPy

# Initialize RoboPy for a Fanuc robot
robot = RoboPy(robot_type="Fanuc", host="127.0.0.1", port=18736)  # Creating a robot instance

# Connect to the robot
robot.connect()

#Retrieve Robots position
robot.get_tcp_position()


