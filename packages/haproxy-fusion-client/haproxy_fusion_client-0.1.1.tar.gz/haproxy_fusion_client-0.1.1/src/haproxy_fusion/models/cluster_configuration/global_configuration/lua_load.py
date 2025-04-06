from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel


class LuaLoad(BaseModel):
    file: str = Field(pattern=r'^\S+$')