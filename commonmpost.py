from fastapi import FastAPI, UploadFile, File, HTTPException
from database import HOST, MEDIAPATH, MPOSTPORT
import os
import shutil
import uuid


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
        "message": f"MediaPostAPI is running in {MPOSTPORT}",
        "data": {}
    }


# ==========================================================
# MEDIA POST
# ==========================================================

@app.post("/commonmpost")
def media_post(
    file: UploadFile = File(...)
):

    try:

        # --------------------------------------------------
        # Check filename
        # --------------------------------------------------

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="File name is required"
            )

        # --------------------------------------------------
        # Create media folder if it doesn't exist
        # --------------------------------------------------

        os.makedirs(
            MEDIAPATH,
            exist_ok=True
        )

        # --------------------------------------------------
        # Get safe filename
        # --------------------------------------------------

        original_filename = os.path.basename(
            file.filename
        )

        # --------------------------------------------------
        # Generate unique filename
        # Prevent overwriting existing files
        # --------------------------------------------------

        extension = os.path.splitext(
            original_filename
        )[1].lower()

        filename = (
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        file_path = os.path.join(
            MEDIAPATH,
            filename
        )

        # --------------------------------------------------
        # Save file
        # --------------------------------------------------

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        return {
            "success": True,
            "httpstatus": 200,
            "message": "Media uploaded successfully",
            "data": {
                "filename": filename,
                "originalfilename": original_filename
            }
        }

    except HTTPException:
        raise

    except Exception as e:

        return {
            "success": False,
            "httpstatus": 500,
            "message": str(e),
            "data": {}
        }

    finally:

        file.file.close()


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=MPOSTPORT,
        log_config=None
    )
