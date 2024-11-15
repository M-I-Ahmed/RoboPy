from typing import Literal

class FanucError(Exception):
    """Exception for Fanuc robot communication errors."""
    pass

class ABBError(Exception):
    """Exception for ABB robot commuincation errors"""
    pass

def handle_response(
    resp: str,
    success_code: int = 0,
    error_code: int = 1,
    continue_on_error: bool = False
) -> tuple[Literal[0, 1], str]:
    """Handles response from robot communication.

    Args:
        resp (str): Response string returned from socket.
        success_code (int): The success code for the response.
        error_code (int): The error code for the response.
        continue_on_error (bool): Whether to continue on error.

    Returns:
        Tuple[Literal[0, 1], str]: A tuple with the response code and message.

    Raises:
        FanucError: If the response code is unexpected or indicates an error.
    """
    code_, msg = resp.split(":")
    code = int(code_)

    # Catch and handle known error conditions
    if code == error_code and not continue_on_error:
        raise FanucError(msg)
    elif code not in (success_code, error_code):
        raise FanucError(f"Unknown response code: {code} and message: {msg}")

    return code, msg