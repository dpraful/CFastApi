from fastapi import FastAPI, Request, Response
from database import HOST, PORT
import os
import httpx


# ==========================================================
# LOAD ROUTES
# ==========================================================
#
# Format:
#
# ROUTE_NAME=/GATEWAY_PREFIX|BACKEND_URL
#
# Example:
#
# ROUTE_PIXAGET=/pixaget|http://localhost:8001
# ROUTE_PIXAPOST=/pixapost|http://localhost:8002
#
# ==========================================================

def load_routes():

    routes = []

    for key, value in os.environ.items():

        if not key.startswith("ROUTE_"):
            continue

        parts = value.split("|", 1)

        if len(parts) != 2:
            continue

        gateway_path = parts[0].strip().rstrip("/")
        backend_url = parts[1].strip().rstrip("/")

        routes.append({
            "name": key,
            "gateway_path": gateway_path,
            "backend_url": backend_url
        })

    # Longest prefix first
    routes.sort(
        key=lambda x: len(x["gateway_path"]),
        reverse=True
    )

    return routes


ROUTES = load_routes()


# ==========================================================
# FASTAPI
# ==========================================================

app = FastAPI()


# ==========================================================
# API STATUS
# ==========================================================

@app.get("/")
def api_status():

    return {
        "success": True,
        "httpstatus": 200,
        "message": f"GatewayAPI is running on port {PORT}",
        "data": {}
    }


# ==========================================================
# GATEWAY
# ==========================================================

@app.api_route(
    "/{full_path:path}",
    methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
        "OPTIONS",
        "HEAD"
    ]
)
async def gateway(
    full_path: str,
    request: Request
):

    request_path = "/" + full_path

    # ------------------------------------------------------
    # FIND ROUTE
    # ------------------------------------------------------

    matched_route = None

    for route in ROUTES:

        gateway_path = route["gateway_path"]

        if (
            request_path == gateway_path
            or request_path.startswith(gateway_path + "/")
        ):
            matched_route = route
            break

    # ------------------------------------------------------
    # ROUTE NOT FOUND
    # ------------------------------------------------------

    if matched_route is None:

        return {
            "success": False,
            "httpstatus": 404,
            "message": "Gateway route not found",
            "data": {}
        }

    # ------------------------------------------------------
    # REMOVE GATEWAY PREFIX
    # ------------------------------------------------------

    gateway_path = matched_route["gateway_path"]
    backend_url = matched_route["backend_url"]

    remaining_path = request_path[len(gateway_path):]

    if not remaining_path:
        remaining_path = "/"

    # ------------------------------------------------------
    # BUILD BACKEND URL
    # ------------------------------------------------------

    target_url = backend_url + remaining_path

    # ------------------------------------------------------
    # READ BODY
    # ------------------------------------------------------

    body = await request.body()

    # ------------------------------------------------------
    # FORWARD HEADERS
    # ------------------------------------------------------

    headers = {}

    for key, value in request.headers.items():

        if key.lower() == "host":
            continue

        headers[key] = value

    # ------------------------------------------------------
    # FORWARD REQUEST
    # ------------------------------------------------------

    try:

        async with httpx.AsyncClient(
            timeout=60.0
        ) as client:

            response = await client.request(
                method=request.method,
                url=target_url,
                content=body,
                params=request.query_params,
                headers=headers
            )

        # --------------------------------------------------
        # RETURN BACKEND RESPONSE
        # --------------------------------------------------

        response_headers = {}

        for key, value in response.headers.items():

            if key.lower() not in [
                "content-length",
                "transfer-encoding",
                "connection"
            ]:
                response_headers[key] = value

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=response_headers
        )

    except httpx.RequestError as e:

        return {
            "success": False,
            "httpstatus": 503,
            "message": f"Backend service unavailable: {str(e)}",
            "data": {}
        }


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_config=None
    )
