from haproxy_fusion.models.base.base_model import BaseModel


class FiftyOneDegreesOptions(BaseModel):
    cache_size: int | None = None
    data_file: str | None = None
    property_name_list: str | None = None
    property_separator: str | None = None
