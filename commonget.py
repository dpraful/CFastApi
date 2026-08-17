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

            rows = cursor.fetchall()

            if not rows:
                data = {"data": []}

            elif len(rows) == 1:
                data = json.loads(rows[0][0]) if rows[0][0] else {"data": []}

            else:
                data = [
                    json.loads(row[0]) if row[0] else {}
                    for row in rows
                ]

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

    if "(" in procedure:
        procedure_name, args = procedure.split("(", 1)
        return execute_sp(procedure_name, args[:-1])

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