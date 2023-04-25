import asyncio
import websockets

clients = []

async def handle_client(websocket, path):
    clients.append(websocket)
    print(f"Client connected. Total clients: {len(clients)}")

    if len(clients) == 2:
        sender = clients[0]
        receiver = clients[1]

        message_data = await sender.recv()
        print(message_data)
        await receiver.send(message_data)

        await sender.close()
        await receiver.close()

        clients.remove(sender)
        clients.remove(receiver)
        print("Clients disconnected.")
    else:
        print("Waiting for more clients...")

if __name__ == "__main__":
    start_server = websockets.serve(handle_client, "localhost", 8080)
    print("Server started")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()