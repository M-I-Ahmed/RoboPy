# Example usage to test the connection

from Client import RoboPy

# Initialize RoboPy for a Fanuc robot
robot = RoboPy(robot_type="Fanuc", host="127.0.0.1", port=18736)  # Replace with your robot's IP

# Connect to the robot
print("1")
robot.connect()
print("2")
robot.get_tcp_position()
print("Hello")


