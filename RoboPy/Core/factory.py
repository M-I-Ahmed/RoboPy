# This script contains the method responsible for creating the robot instances as called in Client.robopy
# To add additional robot OEMs



from Robots import Fanuc_robot  # Importing exactly as defined
#from Robots.ABB_robot import ABBRobot  # Assuming ABBRobot class is also defined in ABB_robot.py

class RobotHandlerFactory:
    @staticmethod
    def create_robot(robot_type: str, *args, **kwargs):
        """Creates and returns an instance of the specified robot type."""
        if robot_type == "Fanuc":
            return Fanuc_robot(*args, **kwargs)  # Instantiate Fanuc_robot
        #elif robot_type == "ABB":
            #return ABBRobot(*args, **kwargs)  # Instantiate ABBRobot
        else:
            raise ValueError(f"Unsupported robot type: {robot_type}")

