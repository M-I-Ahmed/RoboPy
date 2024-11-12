# Client/robopy.py

from Core.factory import RobotHandlerFactory
from Core.command_dispatcher import CommandDispatcher

class RoboPy:
    def __init__(self, robot_type: str, host: str, port: int = 18735, **kwargs):
        """
        Initializes RoboPy with a specific robot type and connection details.

        Args:
            robot_type (str): The type of robot to connect to (e.g., "Fanuc").
            host (str): The IP address of the robot controller.
            port (int): The port number for the robot controller. Defaults to 18735.
            **kwargs: Additional arguments passed to the robot instance (e.g., socket_timeout).
        """
        # Use the factory to create the appropriate robot instance
        self.robot = RobotHandlerFactory.create_robot(robot_type, host=host, port=port, **kwargs)
        self.dispatcher = CommandDispatcher(self.robot)  # Dispatcher to handle command execution

    def connect(self):
        """Connects to the robot."""
        result = self.dispatcher.execute_command("connect")
        print(result)  # Prints (0, "Connected to Fanuc robot at ...") or (1, "Failed to connect ...")

    def disconnect(self):
        """Disconnects from the robot."""
        result = self.dispatcher.execute_command("disconnect")
        print(result)  # Prints (0, "Disconnected from Fanuc robot") or (1, "No connection to disconnect")

    def move_joint(self, position: list[float], speed: int = 100):
        """Moves the robot to a specified joint position."""
        result = self.dispatcher.execute_command("move_joint", position, speed)
        print(result)  # Expected output: (0, "Joint move successful") or (1, "Error message")

    def get_tcp_position(self):
        """Gets the current TCP position of the robot."""
        result = self.dispatcher.execute_command("tcp_position")
        print("TCP Position:", result)  # Expected output: TCP position as a list or an error message
