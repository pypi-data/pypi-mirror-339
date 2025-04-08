# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["UsageQueryResponse"]


class UsageQueryResponse(BaseModel):
    data: Optional[List[Dict[str, object]]] = None

    has_more_data: Optional[bool] = FieldInfo(alias="hasMoreData", default=None)
    """Flag to know if there are more data available than the one returned"""
