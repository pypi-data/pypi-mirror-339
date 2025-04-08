# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, overload

import httpx

from .jobs import (
    JobsResource,
    AsyncJobsResource,
    JobsResourceWithRawResponse,
    AsyncJobsResourceWithRawResponse,
    JobsResourceWithStreamingResponse,
    AsyncJobsResourceWithStreamingResponse,
)
from ...types import data_export_create_adhoc_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    required_args,
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from .schedules import (
    SchedulesResource,
    AsyncSchedulesResource,
    SchedulesResourceWithRawResponse,
    AsyncSchedulesResourceWithRawResponse,
    SchedulesResourceWithStreamingResponse,
    AsyncSchedulesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .destinations import (
    DestinationsResource,
    AsyncDestinationsResource,
    DestinationsResourceWithRawResponse,
    AsyncDestinationsResourceWithRawResponse,
    DestinationsResourceWithStreamingResponse,
    AsyncDestinationsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from ...types.ad_hoc_response import AdHocResponse

__all__ = ["DataExportsResource", "AsyncDataExportsResource"]


class DataExportsResource(SyncAPIResource):
    @cached_property
    def destinations(self) -> DestinationsResource:
        return DestinationsResource(self._client)

    @cached_property
    def jobs(self) -> JobsResource:
        return JobsResource(self._client)

    @cached_property
    def schedules(self) -> SchedulesResource:
        return SchedulesResource(self._client)

    @cached_property
    def with_raw_response(self) -> DataExportsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DataExportsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DataExportsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#with_streaming_response
        """
        return DataExportsResourceWithStreamingResponse(self)

    @overload
    def create_adhoc(
        self,
        *,
        org_id: str | None = None,
        operational_data_types: List[
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
        source_type: Literal["USAGE", "OPERATIONAL"],
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdHocResponse:
        """Trigger an ad-hoc Data Export.

        Each ad-hoc Export can be configured for
        exporting _only one of_ either Usage or Operational data:

        **Operational Data Exports**.

        - **Entity Types**. Use the `operationalDataTypes` parameter to specify the
          entities whose operational data you want to include in the ad-hoc export.
        - **Export Files**. For each of the entity types you select, when the ad-hoc
          export runs a separate file is compiled containing the operational data for
          all entities of that type that exist in your Organization

        **Usage Data Exports**.

        - **Meters/Accounts**. Select the Meters and Accounts whose usage data you want
          to include in the ad-hoc export.
        - **Aggregated or non-aggregated data**:

        1. If you _don't want to aggregate_ the usage data collected by the selected
           Meters, use **ORIGINAL** for `aggregationFrequency`, which is the _default_.
           This means the raw usage data collected by any type of Data Fields and the
           values for any Derived Fields on the selected Meters will be included in the
           ad-hoc export.
        2. If you _do want to aggregate_ the usage data collected by the selected
           Meters, use one of the other options for `aggregationFrequency`: **HOUR**,
           **DAY**, **WEEK**, or **MONTH**. You _must_ then also specified an
           `aggregation` method to be used on the usage data before export. Importantly,
           if you do aggregate usage data, only the usage data collected by any numeric
           Data Fields on the selected Meters - those of type **MEASURE**, **INCOME**,
           or **COST** - will be included in the ad-hoc export.

        **Date Range for Operational Data Exports**. To restrict the operational data
        included in the export by a date/time range, use the `startDate` and `endDate`
        date/time request parameters to specify the period. Constraints:

        - `startDate` must be before `endDate`.
        - `startDate` with no `endDate` is valid.
        - No `startDate` with `endDate` is valid.
        - `endDate` must be before present date/time.
        - Both are optional and if neither is defined, the export includes all data for
          selected entities.

        **Date Range for Usage Data Exports**. To restrict the usage data included in
        the export by date/time range, use the `timePeriod` request parameter to define
        a set date range. Alternatively, define a custom date range using the
        `startDate` and `endDate` date/time parameters:

        - Both `startDate` and `endDate` are required.
        - You cannot use a `startDate` earlier than 35 days in the past.
        - The `endDate` is valid up to tomorrow at 00:00.
        - You must define a Date Range using **timePeriod** or **startDate/endDate**,
          but they are mutually exclusive and you cannot use them together.

        **NOTE:** You can use the ExportJob `id` returned to check the status of the
        triggered ad-hoc export. See the
        [ExportJob](https://www.m3ter.com/docs/api#tag/ExportJob) section of this API
        Reference.

        Args:
          operational_data_types: The list of the operational data types should be exported for.

          source_type

          version:
              The version number of the entity:

              - **Create entity:** Not valid for initial insertion of new entity - _do not use
                for Create_. On initial Create, version is set at 1 and listed in the
                response.
              - **Update Entity:** On Update, version is required and must match the existing
                version because a check is performed to ensure sequential versioning is
                preserved. Version is incremented by 1 and listed in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create_adhoc(
        self,
        *,
        org_id: str | None = None,
        aggregation_frequency: Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"],
        source_type: Literal["USAGE", "OPERATIONAL"],
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        time_period: Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "CURRENT_MONTH",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
        ]
        | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdHocResponse:
        """Trigger an ad-hoc Data Export.

        Each ad-hoc Export can be configured for
        exporting _only one of_ either Usage or Operational data:

        **Operational Data Exports**.

        - **Entity Types**. Use the `operationalDataTypes` parameter to specify the
          entities whose operational data you want to include in the ad-hoc export.
        - **Export Files**. For each of the entity types you select, when the ad-hoc
          export runs a separate file is compiled containing the operational data for
          all entities of that type that exist in your Organization

        **Usage Data Exports**.

        - **Meters/Accounts**. Select the Meters and Accounts whose usage data you want
          to include in the ad-hoc export.
        - **Aggregated or non-aggregated data**:

        1. If you _don't want to aggregate_ the usage data collected by the selected
           Meters, use **ORIGINAL** for `aggregationFrequency`, which is the _default_.
           This means the raw usage data collected by any type of Data Fields and the
           values for any Derived Fields on the selected Meters will be included in the
           ad-hoc export.
        2. If you _do want to aggregate_ the usage data collected by the selected
           Meters, use one of the other options for `aggregationFrequency`: **HOUR**,
           **DAY**, **WEEK**, or **MONTH**. You _must_ then also specified an
           `aggregation` method to be used on the usage data before export. Importantly,
           if you do aggregate usage data, only the usage data collected by any numeric
           Data Fields on the selected Meters - those of type **MEASURE**, **INCOME**,
           or **COST** - will be included in the ad-hoc export.

        **Date Range for Operational Data Exports**. To restrict the operational data
        included in the export by a date/time range, use the `startDate` and `endDate`
        date/time request parameters to specify the period. Constraints:

        - `startDate` must be before `endDate`.
        - `startDate` with no `endDate` is valid.
        - No `startDate` with `endDate` is valid.
        - `endDate` must be before present date/time.
        - Both are optional and if neither is defined, the export includes all data for
          selected entities.

        **Date Range for Usage Data Exports**. To restrict the usage data included in
        the export by date/time range, use the `timePeriod` request parameter to define
        a set date range. Alternatively, define a custom date range using the
        `startDate` and `endDate` date/time parameters:

        - Both `startDate` and `endDate` are required.
        - You cannot use a `startDate` earlier than 35 days in the past.
        - The `endDate` is valid up to tomorrow at 00:00.
        - You must define a Date Range using **timePeriod** or **startDate/endDate**,
          but they are mutually exclusive and you cannot use them together.

        **NOTE:** You can use the ExportJob `id` returned to check the status of the
        triggered ad-hoc export. See the
        [ExportJob](https://www.m3ter.com/docs/api#tag/ExportJob) section of this API
        Reference.

        Args:
          aggregation_frequency: Specifies the time period for the aggregation of usage data included each time
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

          source_type

          account_ids: List of account IDs for which the usage data will be exported.

          aggregation: Specifies the aggregation method applied to usage data collected in the numeric
              Data Fields of Meters included for the Data Export Schedule - that is, Data
              Fields of type **MEASURE**, **INCOME**, or **COST**:

              - **SUM**. Adds the values.
              - **MIN**. Uses the minimum value.
              - **MAX**. Uses the maximum value.
              - **COUNT**. Counts the number of values.
              - **LATEST**. Uses the most recent value. Note: Based on the timestamp `ts`
                value of usage data measurement submissions. If using this method, please
                ensure _distinct_ `ts` values are used for usage data measurement submissions.

          meter_ids: List of meter IDs for which the usage data will be exported.

          time_period: Define a time period to control the range of usage data you want the data export
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

          version:
              The version number of the entity:

              - **Create entity:** Not valid for initial insertion of new entity - _do not use
                for Create_. On initial Create, version is set at 1 and listed in the
                response.
              - **Update Entity:** On Update, version is required and must match the existing
                version because a check is performed to ensure sequential versioning is
                preserved. Version is incremented by 1 and listed in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["operational_data_types", "source_type"], ["aggregation_frequency", "source_type"])
    def create_adhoc(
        self,
        *,
        org_id: str | None = None,
        operational_data_types: List[
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
        ]
        | NotGiven = NOT_GIVEN,
        source_type: Literal["USAGE", "OPERATIONAL"],
        version: int | NotGiven = NOT_GIVEN,
        aggregation_frequency: Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"] | NotGiven = NOT_GIVEN,
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        time_period: Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "CURRENT_MONTH",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdHocResponse:
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return self._post(
            f"/organizations/{org_id}/dataexports/adhoc",
            body=maybe_transform(
                {
                    "operational_data_types": operational_data_types,
                    "source_type": source_type,
                    "version": version,
                    "aggregation_frequency": aggregation_frequency,
                    "account_ids": account_ids,
                    "aggregation": aggregation,
                    "meter_ids": meter_ids,
                    "time_period": time_period,
                },
                data_export_create_adhoc_params.DataExportCreateAdhocParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdHocResponse,
        )


class AsyncDataExportsResource(AsyncAPIResource):
    @cached_property
    def destinations(self) -> AsyncDestinationsResource:
        return AsyncDestinationsResource(self._client)

    @cached_property
    def jobs(self) -> AsyncJobsResource:
        return AsyncJobsResource(self._client)

    @cached_property
    def schedules(self) -> AsyncSchedulesResource:
        return AsyncSchedulesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDataExportsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDataExportsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDataExportsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#with_streaming_response
        """
        return AsyncDataExportsResourceWithStreamingResponse(self)

    @overload
    async def create_adhoc(
        self,
        *,
        org_id: str | None = None,
        operational_data_types: List[
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
        source_type: Literal["USAGE", "OPERATIONAL"],
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdHocResponse:
        """Trigger an ad-hoc Data Export.

        Each ad-hoc Export can be configured for
        exporting _only one of_ either Usage or Operational data:

        **Operational Data Exports**.

        - **Entity Types**. Use the `operationalDataTypes` parameter to specify the
          entities whose operational data you want to include in the ad-hoc export.
        - **Export Files**. For each of the entity types you select, when the ad-hoc
          export runs a separate file is compiled containing the operational data for
          all entities of that type that exist in your Organization

        **Usage Data Exports**.

        - **Meters/Accounts**. Select the Meters and Accounts whose usage data you want
          to include in the ad-hoc export.
        - **Aggregated or non-aggregated data**:

        1. If you _don't want to aggregate_ the usage data collected by the selected
           Meters, use **ORIGINAL** for `aggregationFrequency`, which is the _default_.
           This means the raw usage data collected by any type of Data Fields and the
           values for any Derived Fields on the selected Meters will be included in the
           ad-hoc export.
        2. If you _do want to aggregate_ the usage data collected by the selected
           Meters, use one of the other options for `aggregationFrequency`: **HOUR**,
           **DAY**, **WEEK**, or **MONTH**. You _must_ then also specified an
           `aggregation` method to be used on the usage data before export. Importantly,
           if you do aggregate usage data, only the usage data collected by any numeric
           Data Fields on the selected Meters - those of type **MEASURE**, **INCOME**,
           or **COST** - will be included in the ad-hoc export.

        **Date Range for Operational Data Exports**. To restrict the operational data
        included in the export by a date/time range, use the `startDate` and `endDate`
        date/time request parameters to specify the period. Constraints:

        - `startDate` must be before `endDate`.
        - `startDate` with no `endDate` is valid.
        - No `startDate` with `endDate` is valid.
        - `endDate` must be before present date/time.
        - Both are optional and if neither is defined, the export includes all data for
          selected entities.

        **Date Range for Usage Data Exports**. To restrict the usage data included in
        the export by date/time range, use the `timePeriod` request parameter to define
        a set date range. Alternatively, define a custom date range using the
        `startDate` and `endDate` date/time parameters:

        - Both `startDate` and `endDate` are required.
        - You cannot use a `startDate` earlier than 35 days in the past.
        - The `endDate` is valid up to tomorrow at 00:00.
        - You must define a Date Range using **timePeriod** or **startDate/endDate**,
          but they are mutually exclusive and you cannot use them together.

        **NOTE:** You can use the ExportJob `id` returned to check the status of the
        triggered ad-hoc export. See the
        [ExportJob](https://www.m3ter.com/docs/api#tag/ExportJob) section of this API
        Reference.

        Args:
          operational_data_types: The list of the operational data types should be exported for.

          source_type

          version:
              The version number of the entity:

              - **Create entity:** Not valid for initial insertion of new entity - _do not use
                for Create_. On initial Create, version is set at 1 and listed in the
                response.
              - **Update Entity:** On Update, version is required and must match the existing
                version because a check is performed to ensure sequential versioning is
                preserved. Version is incremented by 1 and listed in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create_adhoc(
        self,
        *,
        org_id: str | None = None,
        aggregation_frequency: Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"],
        source_type: Literal["USAGE", "OPERATIONAL"],
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        time_period: Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "CURRENT_MONTH",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
        ]
        | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdHocResponse:
        """Trigger an ad-hoc Data Export.

        Each ad-hoc Export can be configured for
        exporting _only one of_ either Usage or Operational data:

        **Operational Data Exports**.

        - **Entity Types**. Use the `operationalDataTypes` parameter to specify the
          entities whose operational data you want to include in the ad-hoc export.
        - **Export Files**. For each of the entity types you select, when the ad-hoc
          export runs a separate file is compiled containing the operational data for
          all entities of that type that exist in your Organization

        **Usage Data Exports**.

        - **Meters/Accounts**. Select the Meters and Accounts whose usage data you want
          to include in the ad-hoc export.
        - **Aggregated or non-aggregated data**:

        1. If you _don't want to aggregate_ the usage data collected by the selected
           Meters, use **ORIGINAL** for `aggregationFrequency`, which is the _default_.
           This means the raw usage data collected by any type of Data Fields and the
           values for any Derived Fields on the selected Meters will be included in the
           ad-hoc export.
        2. If you _do want to aggregate_ the usage data collected by the selected
           Meters, use one of the other options for `aggregationFrequency`: **HOUR**,
           **DAY**, **WEEK**, or **MONTH**. You _must_ then also specified an
           `aggregation` method to be used on the usage data before export. Importantly,
           if you do aggregate usage data, only the usage data collected by any numeric
           Data Fields on the selected Meters - those of type **MEASURE**, **INCOME**,
           or **COST** - will be included in the ad-hoc export.

        **Date Range for Operational Data Exports**. To restrict the operational data
        included in the export by a date/time range, use the `startDate` and `endDate`
        date/time request parameters to specify the period. Constraints:

        - `startDate` must be before `endDate`.
        - `startDate` with no `endDate` is valid.
        - No `startDate` with `endDate` is valid.
        - `endDate` must be before present date/time.
        - Both are optional and if neither is defined, the export includes all data for
          selected entities.

        **Date Range for Usage Data Exports**. To restrict the usage data included in
        the export by date/time range, use the `timePeriod` request parameter to define
        a set date range. Alternatively, define a custom date range using the
        `startDate` and `endDate` date/time parameters:

        - Both `startDate` and `endDate` are required.
        - You cannot use a `startDate` earlier than 35 days in the past.
        - The `endDate` is valid up to tomorrow at 00:00.
        - You must define a Date Range using **timePeriod** or **startDate/endDate**,
          but they are mutually exclusive and you cannot use them together.

        **NOTE:** You can use the ExportJob `id` returned to check the status of the
        triggered ad-hoc export. See the
        [ExportJob](https://www.m3ter.com/docs/api#tag/ExportJob) section of this API
        Reference.

        Args:
          aggregation_frequency: Specifies the time period for the aggregation of usage data included each time
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

          source_type

          account_ids: List of account IDs for which the usage data will be exported.

          aggregation: Specifies the aggregation method applied to usage data collected in the numeric
              Data Fields of Meters included for the Data Export Schedule - that is, Data
              Fields of type **MEASURE**, **INCOME**, or **COST**:

              - **SUM**. Adds the values.
              - **MIN**. Uses the minimum value.
              - **MAX**. Uses the maximum value.
              - **COUNT**. Counts the number of values.
              - **LATEST**. Uses the most recent value. Note: Based on the timestamp `ts`
                value of usage data measurement submissions. If using this method, please
                ensure _distinct_ `ts` values are used for usage data measurement submissions.

          meter_ids: List of meter IDs for which the usage data will be exported.

          time_period: Define a time period to control the range of usage data you want the data export
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

          version:
              The version number of the entity:

              - **Create entity:** Not valid for initial insertion of new entity - _do not use
                for Create_. On initial Create, version is set at 1 and listed in the
                response.
              - **Update Entity:** On Update, version is required and must match the existing
                version because a check is performed to ensure sequential versioning is
                preserved. Version is incremented by 1 and listed in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["operational_data_types", "source_type"], ["aggregation_frequency", "source_type"])
    async def create_adhoc(
        self,
        *,
        org_id: str | None = None,
        operational_data_types: List[
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
        ]
        | NotGiven = NOT_GIVEN,
        source_type: Literal["USAGE", "OPERATIONAL"],
        version: int | NotGiven = NOT_GIVEN,
        aggregation_frequency: Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"] | NotGiven = NOT_GIVEN,
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        time_period: Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "CURRENT_MONTH",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdHocResponse:
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return await self._post(
            f"/organizations/{org_id}/dataexports/adhoc",
            body=await async_maybe_transform(
                {
                    "operational_data_types": operational_data_types,
                    "source_type": source_type,
                    "version": version,
                    "aggregation_frequency": aggregation_frequency,
                    "account_ids": account_ids,
                    "aggregation": aggregation,
                    "meter_ids": meter_ids,
                    "time_period": time_period,
                },
                data_export_create_adhoc_params.DataExportCreateAdhocParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdHocResponse,
        )


class DataExportsResourceWithRawResponse:
    def __init__(self, data_exports: DataExportsResource) -> None:
        self._data_exports = data_exports

        self.create_adhoc = to_raw_response_wrapper(
            data_exports.create_adhoc,
        )

    @cached_property
    def destinations(self) -> DestinationsResourceWithRawResponse:
        return DestinationsResourceWithRawResponse(self._data_exports.destinations)

    @cached_property
    def jobs(self) -> JobsResourceWithRawResponse:
        return JobsResourceWithRawResponse(self._data_exports.jobs)

    @cached_property
    def schedules(self) -> SchedulesResourceWithRawResponse:
        return SchedulesResourceWithRawResponse(self._data_exports.schedules)


class AsyncDataExportsResourceWithRawResponse:
    def __init__(self, data_exports: AsyncDataExportsResource) -> None:
        self._data_exports = data_exports

        self.create_adhoc = async_to_raw_response_wrapper(
            data_exports.create_adhoc,
        )

    @cached_property
    def destinations(self) -> AsyncDestinationsResourceWithRawResponse:
        return AsyncDestinationsResourceWithRawResponse(self._data_exports.destinations)

    @cached_property
    def jobs(self) -> AsyncJobsResourceWithRawResponse:
        return AsyncJobsResourceWithRawResponse(self._data_exports.jobs)

    @cached_property
    def schedules(self) -> AsyncSchedulesResourceWithRawResponse:
        return AsyncSchedulesResourceWithRawResponse(self._data_exports.schedules)


class DataExportsResourceWithStreamingResponse:
    def __init__(self, data_exports: DataExportsResource) -> None:
        self._data_exports = data_exports

        self.create_adhoc = to_streamed_response_wrapper(
            data_exports.create_adhoc,
        )

    @cached_property
    def destinations(self) -> DestinationsResourceWithStreamingResponse:
        return DestinationsResourceWithStreamingResponse(self._data_exports.destinations)

    @cached_property
    def jobs(self) -> JobsResourceWithStreamingResponse:
        return JobsResourceWithStreamingResponse(self._data_exports.jobs)

    @cached_property
    def schedules(self) -> SchedulesResourceWithStreamingResponse:
        return SchedulesResourceWithStreamingResponse(self._data_exports.schedules)


class AsyncDataExportsResourceWithStreamingResponse:
    def __init__(self, data_exports: AsyncDataExportsResource) -> None:
        self._data_exports = data_exports

        self.create_adhoc = async_to_streamed_response_wrapper(
            data_exports.create_adhoc,
        )

    @cached_property
    def destinations(self) -> AsyncDestinationsResourceWithStreamingResponse:
        return AsyncDestinationsResourceWithStreamingResponse(self._data_exports.destinations)

    @cached_property
    def jobs(self) -> AsyncJobsResourceWithStreamingResponse:
        return AsyncJobsResourceWithStreamingResponse(self._data_exports.jobs)

    @cached_property
    def schedules(self) -> AsyncSchedulesResourceWithStreamingResponse:
        return AsyncSchedulesResourceWithStreamingResponse(self._data_exports.schedules)
