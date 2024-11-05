import socket
from typing import Optional, Literal
from Base.AbstractRobot import Robot
from Utils.helpers import FanucError, handle_response


class Fanuc_robot(Robot):
    success_code = 0
    error_code = 1

    def __init__(
        self,
        host: str,
        port: int = 18735,
        socket_timeout: int = 60,
        ): 

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
        

    def connect(self) -> tuple[Literal[0, 1], str]:
        try:
            self.comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.comm_sock.settimeout(self.socket_timeout)
            self.comm_sock.connect((self.host, self.port))
            self._connected = True
            resp = self.comm_sock.recv(self.sock_buff_sz).decode()
            return self.handle_response(resp)
        except socket.error as e:
            self._connected = False
            resp = self.comm_sock.recv(self.sock_buff_sz).decode()
            return self.handle_response(resp)

    def disconnect(self) -> tuple[Literal[0, 1], str]:
        if self.comm_sock:
            self.comm_sock.close()
            self.comm_sock = None
            self._connected = False
            return 0, "Disconnected from Fanuc robot"
        else:
            return 1, "No connection to disconnect"

    def _send_command(self, command: str) -> tuple[Literal[0, 1], str]:
        """Send a command and handle the response using centralised response handling."""
        if not self._connected or not self.comm_sock:
            return 1, "Not connected to the Fanuc robot."

        try:
            self.comm_sock.sendall(command.encode())
            raw_response = self.comm_sock.recv(self.sock_buff_sz).decode()
            return handle_response(raw_response, self.SUCCESS_CODE, self.ERROR_CODE)
        except socket.error as e:
            return 1, f"Communication error with the Fanuc robot: {str(e)}"
        
    def cur_cart_position(self, arm: str = None) -> list[float]:
        cmd = "curpos"
        _, msg = self.send_cmd(cmd)
        vals = [float(val.split("=")[1]) for val in msg.split(",")]
        return vals
    
    def cur_joint_position (self, arm: str = None) -> list[float]:
        cmd =  "curjpos"
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
    ) -> tuple[Literal[0,1],str]:

        # prepare velocity. percentage or mm/s
        # format: aaaa, e.g.: 0001%, 0020%, 3000 mm/s
        velocity = int(velocity)
        velocity_ = f"{velocity:04}"

        # prepare acceleration. percentage or mm/s^2
        # format: aaaa, e.g.: 0001%, 0020%, 0100 mm/s^2
        acceleration = int(acceleration)
        acceleration_ = f"{acceleration:04}"

        # prepare CNT value
        # format: aaa, e.g.: 001, 020, 100
        cnt_val = int(cnt_val)
        if not (0 <= cnt_val <= 100):
            raise ValueError("Incorrect CNT value.")
        cnt_val_ = f"{cnt_val:03}"

        cmd = "movej"
      
        motion_type = int(linear)

        cmd += f":{velocity_}:{acceleration_}:{cnt_val_}:{motion_type}:{len(position)}"

        # prepare joint values
        for val in position:
            vs = f"{abs(val):013.6f}"
            if val >= 0:
                vs = "+" + vs
            else:
                vs = "-" + vs
            cmd += f":{vs}"

        # call send_cmd
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
    ) -> tuple[Literal[0,1],str]:

        # prepare velocity. percentage or mm/s
        # format: aaaa, e.g.: 0001%, 0020%, 3000 mm/s
        velocity = int(velocity)
        velocity_ = f"{velocity:04}"

        # prepare acceleration. percentage or mm/s^2
        # format: aaaa, e.g.: 0001%, 0020%, 0100 mm/s^2
        acceleration = int(acceleration)
        acceleration_ = f"{acceleration:04}"

        # prepare CNT value
        # format: aaa, e.g.: 001, 020, 100
        cnt_val = int(cnt_val)
        if not (0 <= cnt_val <= 100):
            raise ValueError("Incorrect CNT value.")
        cnt_val_ = f"{cnt_val:03}"

        cmd = "movep"
      
        motion_type = int(linear)

        cmd += f":{velocity_}:{acceleration_}:{cnt_val_}:{motion_type}:{len(position)}"

        # prepare joint values
        for val in position:
            vs = f"{abs(val):013.6f}"
            if val >= 0:
                vs = "+" + vs
            else:
                vs = "-" + vs
            cmd += f":{vs}"

        # call send_cmd
        return self.send_cmd(cmd, continue_on_error=continue_on_error)        
         
    def gripper(
        self,
        value: bool,
        continue_on_error: bool = False,
    ) -> tuple[Literal[0, 1], str]:
        """Opens/closes robot gripper.

        Args:
            value (bool): True or False
        """
        if (self.ee_DO_type is not None) and (self.ee_DO_num is not None):
            cmd = ""
            if self.ee_DO_type == "RDO":
                cmd = "setrdo"
                port = str(self.ee_DO_num)
            elif self.ee_DO_type == "DO":
                cmd = "setdout"
                port = str(self.ee_DO_num).zfill(5)
            else:
                raise ValueError("Wrong DO type!")

            cmd = cmd + f":{port}:{str(value).lower()}"
            return self.send_cmd(cmd, continue_on_error=continue_on_error)
        else:
            raise ValueError("DO type or number is None!")

    def start_program(self, program_name: str) -> tuple[Literal[0, 1], str]:
        """Calls external program name in a physical robot.

        Args:
            prog_name ([str]): External program name.
        """
        cmd = f"mappdkcall:{program_name}"
        return self.send_cmd(cmd)

    def get_dout(self, dout_num: int) -> int:
        """Get DOUT value.

        Args:
            dout_num (int): DOUT number.

        Returns:
            dout_value: DOUT value.
        """
        cmd = f"getdout:{str(dout_num).zfill(5)}"
        _, dout_value_ = self.send_cmd(cmd)
        dout_value = int(dout_value_)
        return dout_value
