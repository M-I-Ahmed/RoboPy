# Not implemented yet, To DO:
# Test ABB python APIs and compare them to each other
# Write this class definiton using these APIs as an influence

import socket
from typing import Optional, Literal
from Base import Robot
from Utils import ABBError, handle_response

class SocketComm():
    pass




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
            
        
        

    pass