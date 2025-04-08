# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ScheduleUpdateParams", "OperationalDataExportScheduleRequest", "UsageDataExportScheduleRequest"]


class OperationalDataExportScheduleRequest(TypedDict, total=False):
    org_id: Annotated[str, PropertyInfo(alias="orgId")]

    operational_data_types: Required[
        Annotated[
            List[
                Literal[
                    "BILLS",
                    "COMMITMENTS",
                    "ACCOUNTS",
                    "BALANCES",
                    "CONTRACTS",
                    "ACCOUNT_PLANS",
                    "AGGREGATIONS",
                    "PLANS",
                    "PRICING",
                    "PRICING_BANDS",
                    "BILL_LINE_ITEMS",
                    "METERS",
                    "PRODUCTS",
                    "COMPOUND_AGGREGATIONS",
                    "PLAN_GROUPS",
                    "PLAN_GROUP_LINKS",
                    "PLAN_TEMPLATES",
                    "BALANCE_TRANSACTIONS",
                ]
            ],
            PropertyInfo(alias="operationalDataTypes"),
        ]
    ]
    """A list of the entities whose operational data is included in the data export."""

    source_type: Required[Annotated[Literal["USAGE", "OPERATIONAL"], PropertyInfo(alias="sourceType")]]

    version: int
    """The version number of the entity:

    - **Create entity:** Not valid for initial insertion of new entity - _do not use
      for Create_. On initial Create, version is set at 1 and listed in the
      response.
    - **Update Entity:** On Update, version is required and must match the existing
      version because a check is performed to ensure sequential versioning is
      preserved. Version is incremented by 1 and listed in the response.
    """


class UsageDataExportScheduleRequest(TypedDict, total=False):
    org_id: Annotated[str, PropertyInfo(alias="orgId")]

    aggregation_frequency: Required[
        Annotated[Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"], PropertyInfo(alias="aggregationFrequency")]
    ]
    """
    Specifies the time period for the aggregation of usage data included each time
    the Data Export Schedule runs:

    - **ORIGINAL**. Usage data is _not aggregated_. If you select to not aggregate,
      then raw usage data measurements collected by all Data Field types and any
      Derived Fields on the selected Meters are included in the export. This is the
      _Default_.

    If you want to aggregate usage data for the Export Schedule you must define an
    `aggregationFrequency`:

    - **HOUR**. Aggregated hourly.
    - **DAY**. Aggregated daily.
    - **WEEK**. Aggregated weekly.
    - **MONTH**. Aggregated monthly.

    - If you select to aggregate usage data for a Export Schedule, then only the
      aggregated usage data collected by numeric Data Fields of type **MEASURE**,
      **INCOME**, or **COST** on selected Meters are included in the export.

    **NOTE**: If you define an `aggregationFrequency` other than **ORIGINAL** and do
    not define an `aggregation` method, then you'll receive and error.
    """

    source_type: Required[Annotated[Literal["USAGE", "OPERATIONAL"], PropertyInfo(alias="sourceType")]]

    time_period: Required[
        Annotated[
            Literal[
                "TODAY",
                "YESTERDAY",
                "WEEK_TO_DATE",
                "CURRENT_MONTH",
                "LAST_30_DAYS",
                "LAST_35_DAYS",
                "PREVIOUS_WEEK",
                "PREVIOUS_MONTH",
            ],
            PropertyInfo(alias="timePeriod"),
        ]
    ]
    """
    Define a time period to control the range of usage data you want the data export
    to contain when it runs:

    - **TODAY**. Data collected for the current day up until the time the export
      runs.
    - **YESTERDAY**. Data collected for the day before the export runs - that is,
      the 24 hour period from midnight to midnight of the day before.
    - **WEEK_TO_DATE**. Data collected for the period covering the current week to
      the date and time the export runs, and weeks run Monday to Monday.
    - **CURRENT_MONTH**. Data collected for the current month in which the export is
      ran up to and including the date and time the export runs.
    - **LAST_30_DAYS**. Data collected for the 30 days prior to the date the export
      is ran.
    - **LAST_35_DAYS**. Data collected for the 35 days prior to the date the export
      is ran.
    - **PREVIOUS_WEEK**. Data collected for the previous full week period, and weeks
      run Monday to Monday.
    - **PREVIOUS_MONTH**. Data collected for the previous full month period.

    For more details and examples, see the
    [Time Period](https://www.m3ter.com/docs/guides/data-exports/creating-export-schedules#time-period)
    section in our main User Documentation.
    """

    account_ids: Annotated[List[str], PropertyInfo(alias="accountIds")]
    """List of account IDs for which the usage data will be exported."""

    aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"]
    """
    Specifies the aggregation method applied to usage data collected in the numeric
    Data Fields of Meters included for the Data Export Schedule - that is, Data
    Fields of type **MEASURE**, **INCOME**, or **COST**:

    - **SUM**. Adds the values.
    - **MIN**. Uses the minimum value.
    - **MAX**. Uses the maximum value.
    - **COUNT**. Counts the number of values.
    - **LATEST**. Uses the most recent value. Note: Based on the timestamp `ts`
      value of usage data measurement submissions. If using this method, please
      ensure _distinct_ `ts` values are used for usage data measurement submissions.
    """

    meter_ids: Annotated[List[str], PropertyInfo(alias="meterIds")]
    """List of meter IDs for which the usage data will be exported."""

    version: int
    """The version number of the entity:

    - **Create entity:** Not valid for initial insertion of new entity - _do not use
      for Create_. On initial Create, version is set at 1 and listed in the
      response.
    - **Update Entity:** On Update, version is required and must match the existing
      version because a check is performed to ensure sequential versioning is
      preserved. Version is incremented by 1 and listed in the response.
    """


ScheduleUpdateParams: TypeAlias = Union[OperationalDataExportScheduleRequest, UsageDataExportScheduleRequest]
