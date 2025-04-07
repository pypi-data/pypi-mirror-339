import json
from enum import IntEnum

class MessageType(IntEnum):
    INVOCATION = 1
    STREAM_ITEM = 2
    COMPLETION = 3
    STREAM_INVOCATION = 4
    CANCEL_INVOCATION = 5
    PING = 6
    CLOSE = 7
    ACK = 8
    SEQUENCE = 9

class HubMessage:
    def __init__(self, type: int):
        self.type = type

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"type": self.type}

    @classmethod
    def from_json(cls, data: str):
        obj = json.loads(data)
        msg_type = obj.get("type")
        if msg_type == MessageType.INVOCATION:
            return InvocationMessage.from_dict(obj)
        return HubMessage(type=msg_type)
    

class InvocationMessage(HubMessage):
    def __init__(self, invocation_id: str, target: str, arguments: list):
        super().__init__(MessageType.INVOCATION)
        self.invocation_id = invocation_id
        self.target = target
        self.arguments = arguments

    def to_dict(self):
        return {
            "type": self.type,
            "invocationId": self.invocation_id,
            "target": self.target,
            "arguments": self.arguments
        }

    @classmethod
    def from_dict(cls, obj: dict):
        return cls(
            invocation_id=obj.get("invocationId"),
            target=obj.get("target"),
            arguments=obj.get("arguments", [])
        )