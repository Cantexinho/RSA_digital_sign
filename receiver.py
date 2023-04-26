import asyncio
import json
import websockets
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key


async def receive_message() -> None:
    def _unpack_data(dataset: json) -> list:
        message_data = json.loads(dataset)
        return message_data["message"], message_data["signature"], message_data["public_key"]

    async with websockets.connect("ws://localhost:8080") as websocket:
        message, signature_base64, public_key_pem = _unpack_data(await websocket.recv())

        signature = base64.b64decode(signature_base64)
        public_key = load_pem_public_key(public_key_pem.encode())

        try:
            public_key.verify(
                signature,
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("Signature is valid!")
        except:
            print("Signature is invalid:")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(receive_message())
