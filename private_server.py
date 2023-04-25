import asyncio
import json
import websockets

async def receive_message(websocket, path):
    data = await websocket.recv()
    message_data = json.loads(data)

    print(message_data)


async def forward_message(websocket, path):
    return


if __name__ == "__main__":
    start_server = websockets.serve(receive_message, "localhost", 8080)
    print("Server running")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
