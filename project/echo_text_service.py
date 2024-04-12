from pydantic import BaseModel


class EchoTextOutput(BaseModel):
    """
    This model represents the output of the echo_text endpoint. It primarily includes the echoed text received from the user.
    """

    echoedText: str


def echo_text(text: str) -> EchoTextOutput:
    """
    Echoes back the text received in the request path parameter.

    Args:
        text (str): The text input by the user, which is to be echoed back. This should be a string that can include various characters and should be properly sanitized to prevent injection attacks.

    Returns:
        EchoTextOutput: This model represents the output of the echo_text endpoint. It primarily includes the echoed text received from the user.
    """
    return EchoTextOutput(echoedText=text)
