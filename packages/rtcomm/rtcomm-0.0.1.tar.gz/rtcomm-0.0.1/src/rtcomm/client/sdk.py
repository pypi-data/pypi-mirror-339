import asyncio
import websockets
from rtcomm.protocol.messages import HubMessage

class RTCommClient:
    def __init__(self, uri: str, access_token: str):
        self.uri = f"{uri}?access_token={access_token}"
        self.connection = None
        self.handlers = {}
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5

    def on(self, message_type: int, handler):
        self.handlers[message_type] = handler

    async def connect(self):
        while self.reconnect_attempts < self.max_reconnect_attempts:
            try:
                self.connection = await websockets.connect(self.uri)
                self.reconnect_attempts = 0
                asyncio.create_task(self._listen())
                break
            except Exception as e:
                self.reconnect_attempts += 1
                print(f"Connect failed: {e}, attempt {self.reconnect_attempts}")
                await asyncio.sleep(2 ** self.reconnect_attempts)

    async def _listen(self):
        try:
            async for message in self.connection:
                try:
                    hub_msg = HubMessage.from_json(message)
                    handler = self.handlers.get(hub_msg.type)
                    if handler:
                        handler(hub_msg)
                except Exception as e:
                    print(f"[Client] Error handling message: {e}")
        except websockets.ConnectionClosed:
            print("[Client] Connection closed. Reconnecting...")
            await self.connect()

    async def send(self, message: HubMessage):
        if self.connection:
            await self.connection.send(message.to_json())

    async def close(self):
        if self.connection:
            await self.connection.close()