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

        # --------------------------------------------------
        # Convert request body to JSON
        # --------------------------------------------------

        json_data = json.dumps(body)

        with get_connection() as conn:

            cursor = conn.cursor()

            # --------------------------------------------------
            # Execute rnsave with SQL OUTPUT variable
            # --------------------------------------------------

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

            # --------------------------------------------------
            # First result set:
            # JSON returned by the procedure called by rnsave
            # --------------------------------------------------

            rows = cursor.fetchall()

            raw_json = "".join(
                str(row[0])
                for row in rows
                if row and row[0] is not None
            )

            # --------------------------------------------------
            # Move to next result set
            # --------------------------------------------------

            output_code = 0

            if cursor.nextset():

                output_row = cursor.fetchone()

                if output_row and output_row[0] is not None:
                    output_code = int(output_row[0])

            # --------------------------------------------------
            # Commit transaction
            # --------------------------------------------------

            conn.commit()

            # --------------------------------------------------
            # Parse returned JSON
            # --------------------------------------------------

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

            # --------------------------------------------------
            # Output code handling
            # --------------------------------------------------

            if output_code != 0:

                return {
                    "success": False,
                    "httpstatus": 500,
                    "message": "Stored procedure returned an error.",
                    "data": data,
                    "outputcode": output_code
                }

            # --------------------------------------------------
            # Success
            # --------------------------------------------------

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
