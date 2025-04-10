from typing import List

from fastapi import FastAPI
from fastapi.routing import APIRoute


def get_registered_routes(app: FastAPI) -> List[str]:
    """
    Retrieves a list of registered routes in the FastAPI application.

    Args:
    app (FastAPI): The FastAPI application instance.

    Returns:
    List[str]: A list of strings representing the registered routes.
    """
    registered_routes = ["Registered Routes:"]

    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = ", ".join(route.methods)
            registered_routes.append(f"\tPath: {route.path}, Method(s): {methods}")

    return registered_routes
