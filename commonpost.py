from fastapi import FastAPI, Body
from database import get_connection, HOST, POSTPORT
import pyodbc
import json

app = FastAPI()

@app.get("/")
def root():

    return {
        "success": True,
        "httpstatus": 200,
        "message": f"POST API is running in {POSTPORT}",
        "data": {}
    }

@app.post("/commonpost")
def common_post(body: dict = Body(...)):

    try:

        json_data = json.dumps(body)

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                DECLARE @OutputCode INT = 0;

                EXEC dbo.rnsave
                    ?,
                    @OutputCode OUTPUT;

                SELECT @OutputCode AS OutputCode;
                """,
                json_data
            )

            rows = cursor.fetchall()

            raw_json = "".join(
                str(row[0])
                for row in rows
                if row and row[0] is not None
            )

            output_code = 0

            if cursor.nextset():

                output_row = cursor.fetchone()

                if output_row and output_row[0] is not None:
                    output_code = int(output_row[0])

            conn.commit()

            if raw_json:

                try:
                    data = json.loads(raw_json)

                except json.JSONDecodeError as e:

                    return {
                        "success": False,
                        "httpstatus": 500,
                        "message": f"Invalid JSON returned by stored procedure: {e}",
                        "data": {}
                    }

            else:

                data = {}

            if output_code != 0:

                return {
                    "success": False,
                    "httpstatus": 500,
                    "message": "Stored procedure returned an error.",
                    "data": data,
                    "outputcode": output_code
                }

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

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=POSTPORT,
        log_config=None,
        access_log=False,
    )
