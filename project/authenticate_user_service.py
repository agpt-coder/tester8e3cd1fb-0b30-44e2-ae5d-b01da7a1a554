import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class AuthenticateUserResponse(BaseModel):
    """
    This model represents the response returned to the user upon successful authentication, including the issued API key.
    """

    api_key: str
    message: str


async def authenticate_user(email: str, password: str) -> AuthenticateUserResponse:
    """
    Authenticates the user and provides an API key for endpoint access.

    This function checks the given user's email and password against the database. If the credentials match,
    it generates an API key, updates the user's API key in the database, and returns it along with a success message.
    If authentication fails, it returns a response with an appropriate message.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        AuthenticateUserResponse: This model represents the response returned to the user upon successful authentication, including the issued API key.

    Example:
        await authenticate_user("user@example.com", "password123")
        > AuthenticateUserResponse(api_key="new_generated_api_key", message="Authentication successful.")
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        new_api_key = bcrypt.gensalt().decode()
        await prisma.models.User.prisma().update(
            where={"email": email}, data={"apiKey": new_api_key}
        )
        return AuthenticateUserResponse(
            api_key=new_api_key, message="Authentication successful."
        )
    else:
        return AuthenticateUserResponse(
            api_key="", message="Authentication failed. Incorrect email or password."
        )
