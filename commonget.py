from fastapi import FastAPI, HTTPException
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


def execute_sp(procedure_name: str, args: str = ""):

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            sql = f"EXEC dbo.{procedure_name}"

            if args:
                sql += f" {args}"

            cursor.execute(sql)

            row = cursor.fetchone()

            data = json.loads(row[0]) if row and row[0] else {
                "data": []
            }

            return {
                "success": True,
                "httpstatus": 200,
                "message": "SUCCESS",
                "data": data
            }

    except pyodbc.Error as e:

        message = e.args[1] if len(e.args) > 1 else str(e)

        return {
            "success": False,
            "httpstatus": 500,
            "message": message,
            "data": {}
        }


@app.get("/commonget/{procedure}")
def common_get(procedure: str):

    if "(" in procedure and procedure.endswith(")"):
        procedure_name = procedure.split("(", 1)[0]
        args = procedure.split("(", 1)[1][:-1]

        return execute_sp(procedure_name, args)

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