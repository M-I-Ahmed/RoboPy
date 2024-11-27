# Not implemented yet, To DO:
# Test ABB python APIs and compare them to each other
# Write this class definiton using these APIs as an influence

import socket
from typing import Optional, Literal
from Base import Robot
from Utils import ABBError, handle_response
from threading import Lock

class SocketComm():
    pass

class SocketComm:
    def __init__(self, host: str, port: int, socket_timeout: int = 60) -> None:
        self.host = host
        self.port = port
        self.sock_buff_sz = 1024
        self.socket_timeout = socket_timeout
        self.lock = Lock()

        with self._lock:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self._socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
            self._socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
            self._socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 2)

            self._socket.settimeout(self._timeout)
            try:
                self._socket.connect((self.host, self._port))
            except socket.timeout:
                raise ABBError(f"Failed to connect to {self._ip}:{self._port}.")

    def close(self) -> None:
        with self._lock:
            if self._socket:
                self._socket.close()

    def send_cmd(self, cmd: str) -> tuple[Literal[0, 1], str]:

        with self._lock:
            try:
                self._socket.sendall(cmd.encode('utf-8'))
                response = self._socket.recv(self.sock_buff_sz)
                return response.decode('utf-8')
            except (socket.error, socket.timeout) as e:
                raise ABBError(f"Error during communication: {e}")
            
            ##TODO : Improve error handling here
            


class ABB_Yumi(Robot):
    success_code = 0
    error_code =1

    JOINTS = 7

    def __init__(self, name: str, host: str, port: int =  5000, socket_timeout: int = 60 ):
        self.name = name # Robot Arm : {Left} or {Right}
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
    
    def handle_response(
        self, resp: str, continue_on_error: bool = False
     ) -> tuple[Literal[0, 1], str]:
        
        code_, msg = resp.split(":")
        code = int(code_)

        # Catch possible errors
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
            self.comm_sock = SocketComm(self, self.host, self.port)
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

    def send_command(self, cmd: str) -> tuple[Literal[0, 1], str]:
        if self.comm_sock is None:
            raise ABBError("Not connected.")
        
        print("Sending command ",cmd)
        self.comm_sock.sendall(cmd.encode())
        raw_response = self.comm_sock.recv(self.sock_buff_sz).decode()
        print(raw_response)
        return handle_response(raw_response, self.success_code, self.error_code)
    



    def tcp_position(self):
            '''
            Returns the current pose of the robot, in millimeters
            '''
            cmd = "curpos #"
            response_code, msg = self.send_cmd(cmd)
            print ("Response from robot (msg):", msg)
            vals = []
            if response_code == 0 and "=" in msg:
                vals = [float(val.split("=")[1]) for val in msg.split(",") if "=" in val]
            else:
                print(f"Unexpected response format or message: {msg}")
            
            return vals


    pass

##if port = left arm then send command to this port