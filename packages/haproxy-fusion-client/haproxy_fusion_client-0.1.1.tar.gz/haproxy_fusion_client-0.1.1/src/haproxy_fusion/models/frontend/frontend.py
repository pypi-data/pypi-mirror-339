from haproxy_fusion.models.base.base_model import BaseModel
from haproxy_fusion.models.frontend.enum.frontend_mode import FrontendMode


class Frontend(BaseModel):
    name: str
    mode: FrontendMode
    fqdns: list


    def __hash__(self):
        return hash((self.name, frozenset(self.fqdns or [])))

    def __eq__(self, other):
        if isinstance(other, Frontend):
            return (
                    self.name == other.name and
                    set(self.fqdns or []) == set(other.fqdns or [])
            )
        return False
