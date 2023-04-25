import asyncio
import json
import websockets


async def send_message():
    async with websockets.connect("ws://localhost:8080") as websocket:
        message = input("Enter the message to send: ")

        await websocket.send(json.dumps({
            "message": message,
        }))

        print("Message sent.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_message())
