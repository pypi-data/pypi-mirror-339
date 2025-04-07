
from battkit.logging_config import logger
from battkit.dataset.test_schema.base import TestSchema
from battkit.dataset.test_schema.time_series import TimeSeriesSchema
from battkit.dataset.test_schema.frequency import FrequencySchema

TEST_SCHEMAS = [TimeSeriesSchema, FrequencySchema]


# Hides non-specified functions from auto-import
__all__ = [
    "TEST_SCHEMAS", "TestSchema"
]
