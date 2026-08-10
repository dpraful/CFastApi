from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from database import HOST, WSCHATPORT
from typing import Dict


# ==========================================================
# FASTAPI
# ==========================================================

app = FastAPI()


# ==========================================================
# CONNECTION MANAGER
# ==========================================================

class ConnectionManager:

    def __init__(self):

        self.active_connections: Dict[str, WebSocket] = {}

    # ------------------------------------------------------
    # CONNECT USER
    # ------------------------------------------------------

    async def connect(
        self,
        user_id: str,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections[user_id] = websocket

        print(
            f"User {user_id} connected"
        )

    # ------------------------------------------------------
    # DISCONNECT USER
    # ------------------------------------------------------

    def disconnect(
        self,
        user_id: str
    ):

        if user_id in self.active_connections:

            del self.active_connections[user_id]

        print(
            f"User {user_id} disconnected"
        )

    # ------------------------------------------------------
    # SEND MESSAGE
    # ------------------------------------------------------

    async def send_message(
        self,
        user_id: str,
        message: dict
    ):

        websocket = self.active_connections.get(
            user_id
        )

        if websocket:

            await websocket.send_json(
                message
            )

            return True

        return False


manager = ConnectionManager()


# ==========================================================
# API STATUS
# ==========================================================

@app.get("/")
def api_status():

    return {
        "success": True,
        "httpstatus": 200,
        "message": f"ChatAPI is running in {WSCHATPORT}",
        "data": {}
    }


# ==========================================================
# ONLINE USERS
# ==========================================================

@app.get("/chat/online/{user_id}")
def check_online(
    user_id: str
):

    online = (
        user_id in manager.active_connections
    )

    return {
        "success": True,
        "httpstatus": 200,
        "message": "User status",
        "data": {
            "user_id": user_id,
            "online": online
        }
    }


# ==========================================================
# REALTIME CHAT
# ==========================================================

@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(
    websocket: WebSocket,
    user_id: str
):

    await manager.connect(
        user_id,
        websocket
    )

    try:

        while True:

            # --------------------------------------------------
            # RECEIVE MESSAGE
            # --------------------------------------------------

            data = await websocket.receive_json()

            receiver_id = data.get(
                "receiver_id"
            )

            message = data.get(
                "message"
            )

            # --------------------------------------------------
            # VALIDATION
            # --------------------------------------------------

            if not receiver_id:

                await websocket.send_json({
                    "success": False,
                    "httpstatus": 400,
                    "message": "receiver_id is required",
                    "data": {}
                })

                continue

            if not message:

                await websocket.send_json({
                    "success": False,
                    "httpstatus": 400,
                    "message": "message is required",
                    "data": {}
                })

                continue

            # --------------------------------------------------
            # MESSAGE DATA
            # --------------------------------------------------

            chat_message = {

                "type": "message",

                "sender_id": user_id,

                "receiver_id": receiver_id,

                "message": message
            }

            # --------------------------------------------------
            # SEND TO RECEIVER
            # --------------------------------------------------

            sent = await manager.send_message(
                receiver_id,
                chat_message
            )

            # --------------------------------------------------
            # SEND RESPONSE TO SENDER
            # --------------------------------------------------

            if sent:

                await websocket.send_json({

                    "success": True,

                    "httpstatus": 200,

                    "message": "Message sent",

                    "data": chat_message
                })

            else:

                await websocket.send_json({

                    "success": False,

                    "httpstatus": 404,

                    "message": "Receiver is offline",

                    "data": chat_message
                })

    except WebSocketDisconnect:

        manager.disconnect(
            user_id
        )


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=WSCHATPORT,
        log_config=None
    )