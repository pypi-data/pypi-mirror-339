
from battkit.logging_config import logger
from .base import TestSchema
from .time_series import TimeSeriesSchema
from .frequency import FrequencySchema

TEST_SCHEMAS = [TimeSeriesSchema, FrequencySchema]


# Hides non-specified functions from auto-import
__all__ = [
    "TEST_SCHEMAS", "TestSchema"
]
