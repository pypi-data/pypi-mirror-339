# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["UsageDataExportScheduleResponse"]


class UsageDataExportScheduleResponse(BaseModel):
    id: str
    """The id of the schedule"""

    version: int
    """The version number:

    - **Create:** On initial Create to insert a new entity, the version is set at 1
      in the response.
    - **Update:** On successful Update, the version is incremented by 1 in the
      response.
    """

    account_ids: Optional[List[str]] = FieldInfo(alias="accountIds", default=None)
    """List of account IDs for which the usage data will be exported."""

    aggregation: Optional[Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"]] = None
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

    aggregation_frequency: Optional[Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"]] = FieldInfo(
        alias="aggregationFrequency", default=None
    )
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

    meter_ids: Optional[List[str]] = FieldInfo(alias="meterIds", default=None)
    """List of meter IDs for which the usage data will be exported."""

    time_period: Optional[
        Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "CURRENT_MONTH",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
        ]
    ] = FieldInfo(alias="timePeriod", default=None)
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
