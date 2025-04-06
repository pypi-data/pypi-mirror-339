from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel


class DefaultPath(BaseModel):
    path: str = Field(pattern=r'^\S+$')
    type: str
    description: str | None = None
