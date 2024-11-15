class CommandDispatcher:
    def __init__(self, robot):
        self.robot = robot  # The robot instance (e.g., Fanuc_robot or ABBRobot)

    def execute_command(self, command_name: str, *args, **kwargs):
        """Dispatches a command to the appropriate method on the robot."""
        # Check if the robot instance has a method with the given command name
        if hasattr(self.robot, command_name):
            method = getattr(self.robot, command_name)  # Get the method by name
            if callable(method):
                return method(*args, **kwargs)  # Call the method with provided arguments
            else:
                raise AttributeError(f"{command_name} is not callable on the robot.")
        else:
            raise AttributeError(f"{command_name} command not found for this robot.")

