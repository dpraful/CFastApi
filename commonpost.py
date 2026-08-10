from fastapi import FastAPI, Body
from database import get_connection, HOST, POSTPORT
import pyodbc
import json

app = FastAPI()


# ==========================================================
# ROOT URL
# ==========================================================

@app.get("/")
def root():
    return {
        "success": True,
        "httpstatus": 200,
        "message": f"POST API is running in {POSTPORT}",
        "data": {}
    }


# ==========================================================
# COMMON POST
# ==========================================================

@app.post("/commonpost")
def common_post(body: dict = Body(...)):

    try:
        json_data = json.dumps(body)

        with get_connection() as conn:

            cursor = conn.cursor()

            output_code = 0

            cursor.execute(
                "EXEC dbo.rnsave ?, ? OUTPUT",
                json_data,
                output_code
            )

            row = cursor.fetchone()

            conn.commit()

            data = json.loads(row[0]) if row and row[0] else {}

            return {
                "success": True,
                "httpstatus": 200,
                "message": "SUCCESS",
                "data": data
            }

    except pyodbc.Error as e:

        message = e.args[1] if len(e.args) > 1 else str(e)

        if "]" in message:
            message = message.split("]")[-1].strip()

        if ". (" in message:
            message = message.split(". (")[0] + "."

        return {
            "success": False,
            "httpstatus": 500,
            "message": message,
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
        port=POSTPORT,
        log_config=None,
        access_log=False,
    )