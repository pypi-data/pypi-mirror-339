from abc import ABC, abstractmethod
from fastapi import WebSocket, WebSocketDisconnect, Depends
from rtcomm.hub.manager import ConnectionManager
from rtcomm.protocol.messages import HubMessage
import json

class RTCommHub(ABC):
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def __call__(self, websocket: WebSocket, access_token: str = Depends()):
        client_id = self.authenticate(access_token)
        if not client_id:
            await websocket.close(code=1008)
            return

        await self.manager.connect(client_id, websocket)
        await self.on_connect(client_id)

        try:
            while True:
                data = await websocket.receive_text()
                try:
                    message = HubMessage.from_json(data)
                    await self.handle_message(client_id, websocket, message)
                except Exception as e:
                    await websocket.send_text(json.dumps({"type": "error", "message": str(e)}))
        except WebSocketDisconnect:
            self.manager.disconnect(client_id)
            await self.on_disconnect(client_id)

    def authenticate(self, access_token: str) -> str:
        if access_token and access_token.startswith("token-"):
            return access_token.split("-", 1)[-1]
        return ""

    @abstractmethod
    async def on_connect(self, client_id: str):
        pass

    @abstractmethod
    async def on_disconnect(self, client_id: str):
        pass

    @abstractmethod
    async def handle_message(self, client_id: str, websocket: WebSocket, message: HubMessage):
        pass