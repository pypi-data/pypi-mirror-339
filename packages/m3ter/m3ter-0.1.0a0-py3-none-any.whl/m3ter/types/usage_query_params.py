# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "UsageQueryParams",
    "Aggregation",
    "DimensionFilter",
    "Group",
    "GroupDataExplorerAccountGroup",
    "GroupDataExplorerDimensionGroup",
    "GroupDataExplorerTimeGroup",
]


class UsageQueryParams(TypedDict, total=False):
    org_id: Annotated[str, PropertyInfo(alias="orgId")]

    end_date: Required[Annotated[Union[str, datetime], PropertyInfo(alias="endDate", format="iso8601")]]
    """ISO 8601 formatted end date to filter by."""

    start_date: Required[Annotated[Union[str, datetime], PropertyInfo(alias="startDate", format="iso8601")]]
    """ISO 8601 formatted start date to filter by."""

    account_ids: Annotated[List[str], PropertyInfo(alias="accountIds")]

    aggregations: Iterable[Aggregation]

    dimension_filters: Annotated[Iterable[DimensionFilter], PropertyInfo(alias="dimensionFilters")]

    groups: Iterable[Group]

    limit: int

    meter_ids: Annotated[List[str], PropertyInfo(alias="meterIds")]


class Aggregation(TypedDict, total=False):
    field_code: Required[Annotated[str, PropertyInfo(alias="fieldCode")]]
    """Field code"""

    field_type: Required[Annotated[Literal["DIMENSION", "MEASURE"], PropertyInfo(alias="fieldType")]]
    """Type of field"""

    function: Required[Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN", "UNIQUE"]]
    """Aggregation function"""

    meter_id: Required[Annotated[str, PropertyInfo(alias="meterId")]]
    """Meter ID"""


class DimensionFilter(TypedDict, total=False):
    field_code: Required[Annotated[str, PropertyInfo(alias="fieldCode")]]
    """Field code"""

    meter_id: Required[Annotated[str, PropertyInfo(alias="meterId")]]
    """Meter ID"""

    values: Required[List[str]]
    """Values to filter by"""


class GroupDataExplorerAccountGroup(TypedDict, total=False):
    group_type: Annotated[Literal["ACCOUNT", "DIMENSION", "TIME"], PropertyInfo(alias="groupType")]


class GroupDataExplorerDimensionGroup(TypedDict, total=False):
    field_code: Required[Annotated[str, PropertyInfo(alias="fieldCode")]]
    """Field code to group by"""

    meter_id: Required[Annotated[str, PropertyInfo(alias="meterId")]]
    """Meter ID to group by"""

    group_type: Annotated[Literal["ACCOUNT", "DIMENSION", "TIME"], PropertyInfo(alias="groupType")]


class GroupDataExplorerTimeGroup(TypedDict, total=False):
    frequency: Required[Literal["DAY", "HOUR", "WEEK", "MONTH", "QUARTER"]]
    """Frequency of usage data"""

    group_type: Annotated[Literal["ACCOUNT", "DIMENSION", "TIME"], PropertyInfo(alias="groupType")]


Group: TypeAlias = Union[GroupDataExplorerAccountGroup, GroupDataExplorerDimensionGroup, GroupDataExplorerTimeGroup]
