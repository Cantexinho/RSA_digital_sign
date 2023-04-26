import asyncio
import json
import websockets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import base64


def generate_cipher_keys() -> list:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


async def send_message(private_key: object, public_key: object):
    async with websockets.connect("ws://localhost:8080") as websocket:
        message = input("Enter the message to send: ")

        signature = private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        signature_base64 = base64.b64encode(signature).decode()

        data = {
            "message": message,
            "signature": signature_base64,
            "public_key": public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo
            ).decode()
        }

        await websocket.send(json.dumps(data))

        print("Message sent.")

if __name__ == "__main__":
    private_key, public_key = generate_cipher_keys()
    asyncio.get_event_loop().run_until_complete(send_message(private_key, public_key))
