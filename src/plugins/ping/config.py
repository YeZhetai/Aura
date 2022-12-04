from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    broadcast_channel: int