import asyncio
import json
import websockets


# ==========================================================
# USER 1
# ==========================================================

async def user1():

    url = "ws://127.0.0.1:8005/ws/chat/101"

    async with websockets.connect(url) as websocket:

        print("User 101 connected")

        # --------------------------------------------------
        # Send message to User 102
        # --------------------------------------------------

        await websocket.send(json.dumps({
            "receiver_id": "102",
            "message": "Hello User 102!"
        }))

        print("User 101 sent message")

        # --------------------------------------------------
        # Receive response
        # --------------------------------------------------

        response = await websocket.recv()

        print("User 101 received:")
        print(response)


# ==========================================================
# USER 2
# ==========================================================

async def user2():

    url = "ws://127.0.0.1:8005/ws/chat/102"

    async with websockets.connect(url) as websocket:

        print("User 102 connected")

        # --------------------------------------------------
        # Wait for message
        # --------------------------------------------------

        response = await websocket.recv()

        print("User 102 received:")
        print(response)


# ==========================================================
# MAIN
# ==========================================================

async def main():

    # Connect User 102 first
    user2_task = asyncio.create_task(
        user2()
    )

    # Give User 102 time to connect
    await asyncio.sleep(1)

    # Connect User 101 and send message
    user1_task = asyncio.create_task(
        user1()
    )

    await asyncio.gather(
        user1_task,
        user2_task
    )


# ==========================================================
# START TEST
# ==========================================================

if __name__ == "__main__":

    asyncio.run(main())