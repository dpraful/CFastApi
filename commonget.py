from fastapi import FastAPI
from database import get_connection, HOST, GETPORT
import pyodbc
import json

app = FastAPI()

@app.get("/")
def root():
    return {
        "success": True,
        "httpstatus": 200,
        "message": f"GET API is running in {GETPORT}",
        "data": {}
    }

def execute_sp(procedure: str):

    try:
        with get_connection() as conn:

            cursor = conn.cursor()
            cursor.execute(f"EXEC dbo.{procedure}")

            rows = cursor.fetchall()
            data = json.loads(rows[0][0]) if rows else { }

            return {
                "success": True,
                "httpstatus": 200,
                "message": "SUCCESS",
                "data": data
            }

    except pyodbc.Error as e:

        return {
            "success": False,
            "httpstatus": 500,
            "message": str(e),
            "data": {}
        }

@app.get("/commonget/{procedure}")
def common_get(procedure: str):
    return execute_sp(procedure)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=GETPORT,
        log_config=None,
        access_log=False
    )