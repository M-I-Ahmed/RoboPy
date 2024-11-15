
import socket
from typing import Optional, Literal
from Base import Robot
from Utils import FanucError, handle_response

class Fanuc_robot(Robot):
    success_code = 0
    error_code = 1

    def __init__(self, host: str, port: int = 18736, socket_timeout: int = 60): 
        self.host = host
        self.port = port
        self.sock_buff_sz = 1024
        self.socket_timeout = socket_timeout
        self.comm_sock = None
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected
    
    @property
    def robot_model(self) -> str:
        return "Fanuc"

    def handle_response(
        self, resp: str, continue_on_error: bool = False
    ) -> tuple[Literal[0, 1], str]:
        """Handles response from socket communication.

        Args:
            resp (str): Response string returned from socket.
            verbose (bool, optional): [description]. Defaults to False.

        Returns:
            tuple(int, str): Response code and response message.
        """
        code_, msg = resp.split(":")
        code = int(code_)

        # Catch possible errors
        if code == self.error_code and not continue_on_error:
            raise FanucError(msg)
        if code not in (self.success_code, self.error_code):
            raise FanucError(f"Unknown response code: {code} and message: {msg}")

        return code, msg  # type: ignore[return-value]
    
    # def connect(self) -> tuple[Literal[0, 1], str]:
    #     """Establishes a connection to the Fanuc robot."""
    #     try:
    #         self.comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         self.comm_sock.settimeout(self.socket_timeout)
    #         self.comm_sock.connect((self.host, self.port))
    #         self._connected = True
    #         return 0, f"Connected to Fanuc robot at {self.host}:{self.port}"
    #     except socket.error as e:
    #         self._connected = False
    #         return 1, f"Failed to connect to Fanuc robot. Error: {str(e)}"

    def connect(self) -> tuple[Literal[0, 1], str]:
        """Connects to the physical robot."""
        self.comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm_sock.settimeout(self.socket_timeout)
        self.comm_sock.connect((self.host, self.port))
        resp = self.comm_sock.recv(self.sock_buff_sz).decode()
        print(resp)
        self._connected = True
        return self.handle_response(resp)

    def disconnect(self) -> tuple[Literal[0, 1], str]:
        """Closes the connection to the Fanuc robot."""
        if self.comm_sock:
            self.comm_sock.close()
            self.comm_sock = None
            self._connected = False
            return 0, "Disconnected from Fanuc robot"
        else:
            return 1, "No connection to disconnect"

    def send_cmd(self, cmd: str, continue_on_error: bool = False) -> tuple[Literal[0, 1], str]:
        """Sends a command to the robot and handles the response.

        Args:
            cmd (str): The command string to send to the robot.
            continue_on_error (bool): Whether to continue on error.

        Returns:
            tuple: Response code and message.
        """
        if not self._connected or not self.comm_sock:
            return 1, "Not connected to the Fanuc robot."

        try:
            # Send command
            print("Sending Command" + cmd)
            cmd = cmd.strip() + "\n"
            self.comm_sock.sendall(cmd.encode())
            print("cmd sent")
            # Receive and handle response
            raw_response = self.comm_sock.recv(self.sock_buff_sz).decode()
            print(raw_response)
            return handle_response(raw_response, self.success_code, self.error_code, continue_on_error)
        except socket.error as e:
            return 1, f"Communication error with the Fanuc robot: {str(e)}"

    # def tcp_position(self, arm: str = None) -> list[float]:
    #     """Retrieves the current Cartesian position of the robot."""
    #     cmd = "curpos"
    #     _, msg = self.send_cmd(cmd)
    #     vals = [float(val.split("=")[1]) for val in msg.split(",")]
    #     return vals

    def tcp_position(self, arm: str = None) -> list[float]:
        """Retrieves the current Cartesian position of the robot."""
        # Send the position retrieval command
        cmd = "curpos"  # Replace with the correct command if "curpos" is incorrect
        print(cmd)
        response_code, msg = self.send_cmd(cmd)
        
        # Debugging print to check the response format
        print("Response from robot (msg):", msg)
        
        # Parse the response if it is in the expected "key=value" format
        vals = []
        if response_code == 0 and "=" in msg:
            vals = [float(val.split("=")[1]) for val in msg.split(",") if "=" in val]
        else:
            print(f"Unexpected response format or message: {msg}")
        
        return vals

    def cur_joint_position(self, arm: str = None) -> list[float]:
        """Retrieves the current joint position of the robot."""
        cmd = "curjpos"
        _, msg = self.send_cmd(cmd)
        vals = [float(val.split("=")[1]) for val in msg.split(",")]
        return vals

    def move_joint(
        self,
        position: list[float],
        velocity: int = 25,
        acceleration: int = 100,
        cnt_val: int = 0,
        linear: bool = False,
        continue_on_error: bool = False,
        arm: str = None,
    ) -> tuple[Literal[0, 1], str]:
        """Moves the robot to a specified joint position."""
        velocity_ = f"{int(velocity):04}"
        acceleration_ = f"{int(acceleration):04}"
        cnt_val_ = f"{int(cnt_val):03}"

        cmd = f"movej:{velocity_}:{acceleration_}:{cnt_val_}:{int(linear)}:{len(position)}"
        for val in position:
            cmd += f":{val:+013.6f}"

        return self.send_cmd(cmd, continue_on_error=continue_on_error)

    def move_pose(
        self,
        position: list[float],
        velocity: int = 25,
        acceleration: int = 100,
        cnt_val: int = 0,
        linear: bool = False,
        continue_on_error: bool = False,
        arm: str = None,
    ) -> tuple[Literal[0, 1], str]:
        """Moves the robot to a specified Cartesian position."""
        velocity_ = f"{int(velocity):04}"
        acceleration_ = f"{int(acceleration):04}"
        cnt_val_ = f"{int(cnt_val):03}"

        cmd = f"movep:{velocity_}:{acceleration_}:{cnt_val_}:{int(linear)}:{len(position)}"
        for val in position:
            cmd += f":{val:+013.6f}"

        return self.send_cmd(cmd, continue_on_error=continue_on_error)
    
    def gripper(self, value: bool, continue_on_error: bool = False) -> tuple[Literal[0, 1], str]:
        """Opens or closes the robot gripper."""
        if self.ee_DO_type is not None and self.ee_DO_num is not None:
            cmd = "setrdo" if self.ee_DO_type == "RDO" else "setdout"
            port = str(self.ee_DO_num).zfill(5)
            cmd = f"{cmd}:{port}:{str(value).lower()}"
            return self.send_cmd(cmd, continue_on_error=continue_on_error)
        else:
            return 1, "DO type or number is None!"

    def start_program(self, program_name: str) -> tuple[Literal[0, 1], str]:
        """Starts a specific program on the robot."""
        cmd = f"mappdkcall:{program_name}"
        return self.send_cmd(cmd)

    def get_dout(self, dout_num: int) -> int:
        """Retrieves the digital output (DOUT) value."""
        cmd = f"getdout:{str(dout_num).zfill(5)}"
        _, dout_value_ = self.send_cmd(cmd)
        return int(dout_value_)
