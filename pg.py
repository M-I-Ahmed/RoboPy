# Example usage to test the connection

from Client.robopy import RoboPy

# Initialize RoboPy for a Fanuc robot
robot = RoboPy(robot_type="Fanuc", host="127.0.0.1", port=18736)  # Replace with your robot's IP

# Connect to the robot
robot.connect()
print("Hello")


