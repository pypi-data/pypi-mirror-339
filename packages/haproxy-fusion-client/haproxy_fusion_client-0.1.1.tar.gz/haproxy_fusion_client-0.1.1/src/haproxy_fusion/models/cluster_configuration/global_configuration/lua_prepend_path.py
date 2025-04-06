from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel


class LuaPrependPath(BaseModel):
    path: str = Field(pattern=r'^\S+$')
    type: str | None = None