### This is the abstract class definition for the robot object ###
### This is the class that the robot specific classes will implement ### 
from abc import ABC, abstractmethod

class Robot(ABC):

    ### Properties ###
    @property
    @abstractmethod
    def is_connected(self) -> bool:
        raise NotImplementedError("This method should be implemented by any subclasses")
    
    @property
    @abstractmethod
    def robot_model(self) -> str:
        raise NotImplementedError("This method should be implemented by any subclasses")
    
    ### Methods ###
    @abstractmethod
    def tcp_position(self, arm: str = None) -> list[float]:
        raise NotImplementedError("This method should be implemented by any subclasses")
    
    @abstractmethod
    def joint_position (self, arm: str = None) -> list[float]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    # Connection Methods #
    @abstractmethod
    def connect(self) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    @abstractmethod
    def disconnect(self) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    # Movement Methods # 
    def move_joint(
        self,
        position: list[float],
        arm: str = None,
        velocity: int = None, 
    ) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def move_pose(
        self,
        position: list[float],
        velocity: int,
        linear: bool,
        arm: str = None,
    ) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    # Program Control # 





