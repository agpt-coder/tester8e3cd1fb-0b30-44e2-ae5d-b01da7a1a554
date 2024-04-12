import logging
from contextlib import asynccontextmanager

import project.authenticate_user_service
import project.echo_text_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="tester",
    lifespan=lifespan,
    description="Based on the user's request for an API tester feature that echoes back any input text, combined with the information gathered from the searches on API testing best practices and the creation of an echo API with FastAPI, the following detailed project plan is proposed:\n\n**Project Overview:**\nThe goal is to develop a user-friendly API tester feature capable of echoing back any text input by the user. The feature will serve as a valuable tool for developers to test and debug their APIs by checking the handling of request data and ensuring the API's response mechanisms are functioning as expected.\n\n**Technical Stack:**\n- **Programming Language:** Python\n- **API Framework:** FastAPI\n- **Database:** PostgreSQL\n- **ORM:** Prisma\n\n**Implementation Steps:**\n1. Set up the development environment by installing Python, FastAPI, and necessary libraries including Uvicorn for running the ASGI server.\n2. Utilizing FastAPI, create a simple API that contains an endpoint to echo texts. The endpoint `/echo/{text}` will accept text inputs via HTTP GET requests and return a JSON response containing the echoed text.\n3. Ensure the API handles different data types and special characters in the input text properly, without errors.\n4. Integrate PostgreSQL using Prisma ORM to potentially log requests and responses for further analysis and debugging purposes, although the primary function of this API will not involve database operations.\n5. Conduct thorough testing following best practices, covering various API request combinations, and validating all possible responses. Include security and performance tests to ensure the API is robust against common vulnerabilities and can handle expected loads.\n6. Document the API, detailing its usage, endpoint descriptions, expected request formats, and example responses. Provide guidance on setting up the local development environment for testing purposes.\n7. Deploy the API on a test server and set up continuous integration and deployment pipelines for automatic testing and deployments on code changes.\n\n**Testing and Validation:**\nTo ensure the API tester feature meets quality standards, perform unit tests and integration tests, testing all possible input scenarios and monitoring the responses. Utilize automation tools to streamline this process.\n\n**Conclusion:**\nThe API tester feature will immensely aid in the development and testing of APIs, offering a simple yet effective tool for echoing back input text. This tool will not only facilitate testing for response handling but also provide insights into potential improvements in API design and functionality.",
)


@app.get("/echo/{text}", response_model=project.echo_text_service.EchoTextOutput)
async def api_get_echo_text(
    text: str,
) -> project.echo_text_service.EchoTextOutput | Response:
    """
    Echoes back the text received in the request path parameter.
    """
    try:
        res = project.echo_text_service.echo_text(text)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/authenticate",
    response_model=project.authenticate_user_service.AuthenticateUserResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserResponse | Response:
    """
    Authenticates the user and provides an API key for endpoint access.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
