from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from zmp_openapi_models.alerts import (
    AlertSortField,
    AlertStatus,
    Priority,
    RepeatedCountOperator,
    Sender,
    Severity,
)

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 500


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"
