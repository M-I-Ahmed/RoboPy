### The is The abstract class definition for The robot object ###
### The is The class that The robot specific classes will implement ### 
from abc import ABC, abstractmethod

class Robot(ABC):

    ### Properties ###
    @property
    @abstractmethod
    def is_connected(self) -> bool:
        raise NotImplementedError("The method, is_connected,should be implemented by any subclasses ")
    
    @property
    @abstractmethod
    def robot_model(self) -> str:
        raise NotImplementedError("The method, 'robot_model', should be implemented by any subclasses")
    
    ### Methods ###
    @abstractmethod
    def tcp_position(self, arm: str = None) -> list[float]:
        raise NotImplementedError("The method, 'tcp_position', should be implemented by any subclasses")
    
    @abstractmethod
    def joint_position (self, arm: str = None) -> list[float]:
        raise NotImplementedError("The method, 'joint_position', should be implemented by any subclasses")

    # Connection Methods #
    @abstractmethod
    def connect(self) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'connect', should be implemented by any subclasses")

    @abstractmethod
    def disconnect(self) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'disconnect', should be implemented by any subclasses")

    # Movement Methods # 
    def move_joint(
        self,
        position: list[float],
        arm: str = None,
        velocity: int = None, 
    ) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'move_joint', should be implemented by any subclasses")

    def move_pose(
        self,
        position: list[float],
        velocity: int,
        linear: bool,
        arm: str = None,
    ) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'move_pose', should be implemented by any subclasses")

    def gripper(self, value: bool,)-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'gripper', should be implemented by any subclasses")

    # Program Control # 
    def start_program(self, program_name: str = None,) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'start_program', should be implemented by any subclasses")

    def stop_program(self, program_name: str = None,) -> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'stop_program', should be implemented by any subclasses")

    def is_program_running(self)-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'is_program_running', should be implemented by any subclasses")

    # Get I/O states # 
    def get_Din(self, digital_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'get_Din', should be implemented by any subclasses")

    def get_Dout(self, digital_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'get_Dout', should be implemented by any subclasses")

    def get_Ain(self, analog_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'get_Ain', should be implemented by any subclasses")
    
    def get_Aout(self, analog_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'get_Aout', should be implemented by any subclasses")

    def get_Gin(self, group_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'get_Gin', should be implemented by any subclasses")

    def get_Gout(self, group_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'get_Gout', should be implemented by any subclasses")

    # Set I/O states #
    def set_Din(self, digital_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'set_Din', should be implemented by any subclasses")

    def set_Dout(self, digital_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'set_Dout', should be implemented by any subclasses")

    def set_Ain(self, analog_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'set_Ain', should be implemented by any subclasses")
    
    def set_Aout(self, analog_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'set_Aout', should be implemented by any subclasses")

    def set_Gin(self, group_input_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'set_Gin', should be implemented by any subclasses")

    def set_Gout(self, group_output_index: int, value: bool )-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'set_Gout', should be implemented by any subclasses")

    # Reset methods

    def clear_current_prg(self)-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'clear_current_prg', should be implemented by any subclasses")
    
    def return_home(self, arm: str = None)-> tuple[Literal[0,1],str]:
        raise NotImplementedError("The method, 'return_home', should be implemented by any subclasses")








