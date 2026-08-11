from fastapi import FastAPI, HTTPException
from database import get_connection, HOST, GETPORT
import pyodbc
import json
import re

app = FastAPI()


# Root URL
@app.get("/")
def root():
    return {
        "success": True,
        "httpstatus": 200,
        "message": f"GET API is running in {GETPORT}",
        "data": {}
    }


def execute_sp(procedure_name: str):

    # Validate stored procedure name
    if not re.fullmatch(r"\w+", procedure_name):
        raise HTTPException(
            status_code=400,
            detail="Invalid procedure name"
        )

    try:
        with get_connection() as conn:

            cursor = conn.cursor()

            # Execute stored procedure
            cursor.execute(f"EXEC dbo.{procedure_name}")

            # FOR JSON PATH can return large JSON in multiple chunks
            rows = cursor.fetchall()

            # Combine all JSON chunks
            raw_json = "".join(
                str(row[0])
                for row in rows
                if row and row[0]
            )

            # No data returned
            if not raw_json:
                data = {
                    "data": []
                }

            else:
                try:
                    data = json.loads(raw_json)

                except json.JSONDecodeError as e:
                    return {
                        "success": False,
                        "httpstatus": 500,
                        "message": f"Invalid JSON returned by stored procedure: {e}",
                        "data": {}
                    }

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


@app.get("/commonget/{procedure_name}")
def common_get(procedure_name: str):
    return execute_sp(procedure_name)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=GETPORT,
        log_config=None,
        access_log=False,
    )
