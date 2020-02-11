from enum import Enum


class QualityType(Enum):
    HQ = 0
    MQ = 1
    LQ = 2

    @classmethod
    def get_quality_type(cls, qual: str) -> "QualityType":
        if qual == "hq":
            return cls.HQ
        elif qual == "mq":
            return cls.MQ
        elif qual == "lq":
            return cls.LQ
        else:
            raise ValueError(f"Invalid QualityType: {qual}")
