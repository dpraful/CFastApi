from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from database import HOST, MEDIAPATH, MGETPORT
import os
import mimetypes


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
        "message": f"MediaGetAPI is running in {MGETPORT}",
        "data": {}
    }


# ==========================================================
# MEDIA GET
# ==========================================================

@app.get("/commonmget/{file_path:path}")
def media_get(file_path: str):

    # ------------------------------------------------------
    # Build media root
    # ------------------------------------------------------

    media_root = os.path.realpath(MEDIAPATH)

    # ------------------------------------------------------
    # Build requested file path
    # ------------------------------------------------------

    requested_file = os.path.realpath(
        os.path.join(media_root, file_path)
    )

    # ------------------------------------------------------
    # Security check
    # Prevent access outside MEDIAPATH
    # ------------------------------------------------------

    if not (
        requested_file == media_root
        or requested_file.startswith(
            media_root + os.sep
        )
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    # ------------------------------------------------------
    # Check file
    # ------------------------------------------------------

    if not os.path.isfile(requested_file):

        raise HTTPException(
            status_code=404,
            detail="Media file not found"
        )

    # ------------------------------------------------------
    # Detect MIME type
    # ------------------------------------------------------

    media_type, _ = mimetypes.guess_type(
        requested_file
    )

    if media_type is None:
        media_type = "application/octet-stream"

    # ------------------------------------------------------
    # Return media
    # ------------------------------------------------------

    return FileResponse(
        path=requested_file,
        media_type=media_type
    )


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=MGETPORT,
        log_config=None
    )
