from pydantic import Field

from haproxy_fusion.models.base.base_model import BaseModel


class H1CaseAdjustItem(BaseModel):
    from_: str = Field(..., alias="from")
    to: str