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
    def start_program(self, program_name: str = None,) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def stop_program(self, program_name: str = None,) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def is_program_running(self)-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    # Get I/O states # 
    def get_Din(self, digital_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def get_Dout(self, digital_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def get_Ain(self, analog_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")
    
    def get_Aout(self, analog_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def get_Gin(self, group_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def get_Gout(self, group_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    # Set I/O states #
    def set_Din(self, digital_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def set_Dout(self, digital_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def set_Ain(self, analog_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")
    
    def set_Aout(self, analog_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def set_Gin(self, group_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    def set_Gout(self, group_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("This method should be implemented by any subclasses")

    # Reset methods



    # Return to home
    # Clear program






