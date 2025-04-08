import os
from enum import Enum

RETRY_DELTA_TIME = int(os.environ.get('MERIT_MEDICINE_RETRY_DELTA_TIME', 10))

class AthenaQueryStatus(Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    