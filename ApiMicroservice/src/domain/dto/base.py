from dataclasses import asdict, dataclass


@dataclass(kw_only=True, frozen=True)
class BaseDto:
    def to_dict(self) -> dict:
        return asdict(self)
