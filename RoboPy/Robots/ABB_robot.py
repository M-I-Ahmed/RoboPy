# Not implemented yet, To DO:
# Test ABB python APIs and compare them to each other
# Write this class definiton using these APIs as an influence

import socket
from typing import Optional, Literal
from Base import Robot
from Utils import ABBError, handle_response
from threading import Lock



class SocketComm():
    def __init__(self, host: str, port: int, socket_timeout: int = 60) -> None:
        self.host = host
        self.port = port
        self.sock_buff_sz = 1024
        self.socket_timeout = socket_timeout
        self.lock = Lock()

        with self.lock:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self._socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
            self._socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
            self._socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 2)

            self._socket.settimeout(self.socket_timeout)
            try:
                self._socket.connect((self.host, self.port))
            except socket.timeout:
                raise ABBError(f"Failed to connect to {self.host}:{self.port}.")

    def close(self) -> None:
        with self.lock:
            if self._socket:
                self._socket.close()

    def send_cmd(self, cmd: str) -> tuple[Literal[0, 1], str]:
        with self.lock:
            try:
                self._socket.sendall(cmd.encode())
                response = self._socket.recv(self.sock_buff_sz)
                return response.decode('utf-8')
            except (socket.error, socket.timeout) as e:
                raise ABBError(f"Error during communication: {e}")
            
            ##TODO : Improve error handling here
            
            


class ABB_YuMi(Robot):
    success_code = 1
    error_code =0

    JOINTS = 7

    def __init__(self, host: str, port: int =  5000, socket_timeout: int = 60 ):
        #self.name = name # Robot Arm : {Left} or {Right}
        self.host = host # Robot IP
        self.port = port # 
        self.sock_buff_sz = 1024
        self.socket_timeout = socket_timeout
        self.comm_sock = None
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def robot_model(self) -> str:
        return "ABB-Yumi"
    
    # def handle_response(
    #     self, resp: str, continue_on_error: bool = False
    #  ) -> tuple[Literal[0, 1], str]:
    #     print(resp)
    #     code_, msg = resp.split(":")
    #     code = int(code_)

    #     # Catch possible errors
    #     if code == self.error_code and not continue_on_error:
    #         raise ABBError(msg)
    #     if code not in (self.success_code, self.error_code):
    #         raise ABBError(f"Unknown response code: {code} and message: {msg}")

    #     return code, msg 
    def handle_response(
        self, resp: str, continue_on_error: bool = False
    ) -> tuple[Literal[0, 1], str]:
        print(resp)

        # Check if the response contains a colon
        # if ":" not in resp:
        #     print("Warning: Malformed response received. No colon found.")
        #     return self.error_code, resp  # Assume an error code and return the raw response for debugging

        # Split the response into code and message, with a limit of 1 split
        instr_code, code_, msg = resp.split(" ", 2)
        
        # Ensure the response code is an integer
        try:
            code = int(code_)
        except ValueError:
            raise ABBError(f"Invalid response code format: '{code_}'")

        # Handle error cases
        if code == self.error_code and not continue_on_error:
            raise ABBError(msg)
        if code not in (self.success_code, self.error_code):
            raise ABBError(f"Unknown response code: {code} and message: {msg}")

        return code, msg

        
    
        
    def connect(self) -> tuple[Literal[0, 1], str]:
        if self.comm_sock is not None:
            print("Connection already exists.")
            return
        
        print("Connecting to Yumi at", self.host, self.port, ".") 
        try:
            self.comm_sock = SocketComm(self.host, self.port)
            self._connected = True
            
            print("Connection successful!")
        except ABBError as e:
            print("Failed to connect to Yumi")

    def disconnect(self) -> tuple[Literal[0, 1], str]:
        if self._connected == True:
            print("Disconnecting from YuMI...")
            self.comm_sock.close()
            self.comm_sock = None
            print("Disconnected.")
        else:
            print("Not connected.")

    # def send_cmd(self, cmd: str) -> tuple[Literal[0, 1], str]:
    #     if self.comm_sock is None:
    #         raise ABBError("Not connected.")
        
    #     print("Sending command ",cmd)
    #     self.comm_sock.sendall(cmd.encode())
    #     raw_response = self.comm_sock.recv(self.sock_buff_sz).decode()
    #     print(raw_response)
    #     return handle_response(raw_response, self.success_code, self.error_code)
    
    def send_cmd(self, cmd: str) -> tuple[Literal[0, 1], str]:
        # if self.comm_sock is None:
        #     raise ABBError("Not connected.")
        
        print("Sending command ", cmd)
        response = self.comm_sock.send_cmd(cmd)  # Use `SocketComm.send_cmd` method
        print(response)
        return self.handle_response(response)




    # def tcp_position(self):
    #         '''
    #         Returns the current pose of the robot, in millimeters
    #         '''
    #         cmd = "3"
    #         response_code, msg = self.send_cmd(cmd)
    #         print ("Response from robot (msg):", msg)
    #         vals = []
    #         if response_code == 0 and "=" in msg:
    #             vals = [float(val.split("=")[1]) for val in msg.split(",") if "=" in val]
    #         else:
    #             print(f"Unexpected response format or message: {msg}")
            
    #         return vals

    def tcp_position(self):
        """
        Returns the current pose of the robot, in millimeters
        """
        cmd = "3 #"
        response_code, msg = self.send_cmd(cmd)
        print("Response from robot (msg):", msg)
        vals = []
        
        if response_code == 1:
            # Parse space-separated values if the message is malformed
            try:
                vals = [float(x) for x in msg.split()]
            except ValueError:
                print(f"Error parsing position: {msg}")
        else:
            print(f"Unexpected response format or message: {msg}")
        
        return vals
    
    def cur_joint_position(self, arm = None):
        "Returns the position of the robot joints"

        cmd = "4 #"
        response_code, msg = self.send_cmd(cmd)
        print("Response from robot (msg): ", msg)
        vals = []

        if response_code == 1:
            # Parse space-separated values if the message is malformed
            try:
                vals = [float(x) for x in msg.split()]
            except ValueError:
                print(f"Error parsing position: {msg}")
        else:
            print(f"Unexpected response format or message: {msg}")

        return vals

    def gripper(self):
        cmd = "26 #"
        response_code, msg = self.send_cmd(cmd)
        print("Response from robot (msg): ", msg)
        gripper_width = msg
        print("Width =" , gripper_width)

        return gripper_width
    



##if port = left arm then send command to this port