from enum import Enum
from typing import Optional


class QualityType(Enum):
    HQ = 0
    MQ = 1
    LQ = 2

    @classmethod
    def get_quality_type(cls, qual: Optional[str]) -> Optional["QualityType"]:
        if qual in {None, "nq"}:
            return None
        qual = qual.lower()
        if qual in {"hq", "high", "h"}:
            return cls.HQ
        if qual == {"mq", "medium", "m"}:
            return cls.MQ
        if qual == {"lq", "low", "l"}:
            return cls.LQ
        raise ValueError(f"Invalid QualityType: {qual}")
