from Robots.Fanuc_robot import Fanuc_robot  # Importing exactly as defined
#from Robots.ABB_robot import ABBRobot  # Assuming ABBRobot class is also defined in ABB_robot.py

class RobotHandlerFactory:
    @staticmethod
    def create_robot(robot_type: str, *args, **kwargs):
        """Creates and returns an instance of the specified robot type."""
        if robot_type == "Fanuc":
            return Fanuc_robot(*args, **kwargs)  # Instantiate Fanuc_robot as it is named
        #elif robot_type == "ABB":
            #return ABBRobot(*args, **kwargs)  # Instantiate ABBRobot if this is the correct class name
        else:
            raise ValueError(f"Unsupported robot type: {robot_type}")

