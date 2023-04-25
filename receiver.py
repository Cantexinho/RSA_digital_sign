import asyncio
import json
import websockets

async def receive_message():
    async with websockets.connect("ws://localhost:8080") as websocket:
        data = await websocket.recv()
        message_data = json.loads(data)

        print(message_data)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(receive_message())
