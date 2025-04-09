# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, List, cast
from typing_extensions import Literal, overload

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    required_args,
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursor, AsyncCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.data_exports import schedule_list_params, schedule_create_params, schedule_update_params
from ...types.data_exports.schedule_list_response import ScheduleListResponse
from ...types.data_exports.schedule_create_response import ScheduleCreateResponse
from ...types.data_exports.schedule_delete_response import ScheduleDeleteResponse
from ...types.data_exports.schedule_update_response import ScheduleUpdateResponse
from ...types.data_exports.schedule_retrieve_response import ScheduleRetrieveResponse

__all__ = ["SchedulesResource", "AsyncSchedulesResource"]


class SchedulesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SchedulesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SchedulesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SchedulesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#with_streaming_response
        """
        return SchedulesResourceWithStreamingResponse(self)

    @overload
    def create(
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
    ) -> ScheduleCreateResponse:
        """Create a new Data Export Schedule.

        Each Schedule can be configured for exporting
        _only one_ of either Usage or Operational data:

        **Operational Data Exports**.

        - Use the `operationalDataTypes` parameter to specify the entities whose
          operational data you want to include in the export each time the Export
          Schedule runs.
        - For each of the entity types you select, each time the Export Schedule runs a
          separate file is compiled containing the operational data for all entities of
          that type that exist in your Organization

        **Usage Data Exports**.

        - Select the Meters and Accounts whose usage data you want to include in the
          export each time the Export Schedule runs.
        - If _don't want to aggregate_ the usage data collected by the selected Meters,
          use **ORIGINAL** for `aggregationFrequency`, which is the _default_. This
          means the raw usage data collected by any type of Data Fields and the values
          for any Derived Fields on the selected Meters will be included in the export.
        - If you _do want to aggregate_ the usage data collected by the selected Meters,
          use one of the other options for `aggregationFrequency`: **HOUR**, **DAY**,
          **WEEK**, or **MONTH**. You _must_ then also specified an `aggregation` method
          to be used on the usage data before export. Importantly, if you do aggregate
          usage data, only the usage data collected by any numeric Data Fields on the
          selected Meters - those of type **MEASURE**, **INCOME**, or **COST** - will be
          included in the export each time the Export Schedule runs.

        Args:
          operational_data_types: A list of the entities whose operational data is included in the data export.

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
    def create(
        self,
        *,
        org_id: str | None = None,
        aggregation_frequency: Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"],
        source_type: Literal["USAGE", "OPERATIONAL"],
        time_period: Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "CURRENT_MONTH",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
        ],
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleCreateResponse:
        """Create a new Data Export Schedule.

        Each Schedule can be configured for exporting
        _only one_ of either Usage or Operational data:

        **Operational Data Exports**.

        - Use the `operationalDataTypes` parameter to specify the entities whose
          operational data you want to include in the export each time the Export
          Schedule runs.
        - For each of the entity types you select, each time the Export Schedule runs a
          separate file is compiled containing the operational data for all entities of
          that type that exist in your Organization

        **Usage Data Exports**.

        - Select the Meters and Accounts whose usage data you want to include in the
          export each time the Export Schedule runs.
        - If _don't want to aggregate_ the usage data collected by the selected Meters,
          use **ORIGINAL** for `aggregationFrequency`, which is the _default_. This
          means the raw usage data collected by any type of Data Fields and the values
          for any Derived Fields on the selected Meters will be included in the export.
        - If you _do want to aggregate_ the usage data collected by the selected Meters,
          use one of the other options for `aggregationFrequency`: **HOUR**, **DAY**,
          **WEEK**, or **MONTH**. You _must_ then also specified an `aggregation` method
          to be used on the usage data before export. Importantly, if you do aggregate
          usage data, only the usage data collected by any numeric Data Fields on the
          selected Meters - those of type **MEASURE**, **INCOME**, or **COST** - will be
          included in the export each time the Export Schedule runs.

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

    @required_args(["operational_data_types", "source_type"], ["aggregation_frequency", "source_type", "time_period"])
    def create(
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
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleCreateResponse:
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return cast(
            ScheduleCreateResponse,
            self._post(
                f"/organizations/{org_id}/dataexports/schedules",
                body=maybe_transform(
                    {
                        "operational_data_types": operational_data_types,
                        "source_type": source_type,
                        "version": version,
                        "aggregation_frequency": aggregation_frequency,
                        "time_period": time_period,
                        "account_ids": account_ids,
                        "aggregation": aggregation,
                        "meter_ids": meter_ids,
                    },
                    schedule_create_params.ScheduleCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ScheduleCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        id: str,
        *,
        org_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleRetrieveResponse:
        """Retrieve a Data Export Schedule for the given UUID.

        Each Schedule can be
        configured for exporting _only one_ of either Usage or Operational data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ScheduleRetrieveResponse,
            self._get(
                f"/organizations/{org_id}/dataexports/schedules/{id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ScheduleRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    def update(
        self,
        id: str,
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
    ) -> ScheduleUpdateResponse:
        """Update a Data Export Schedule for the given UUID.

        Each Schedule can be
        configured for exporting _only one_ of either Usage or Operational data:

        **Operational Data Exports**.

        - Use the `operationalDataTypes` parameter to specify the entities whose
          operational data you want to include in the export each time the Export
          Schedule runs.
        - For each of the entity types you select, each time the Export Schedule runs a
          separate file is compiled containing the operational data for all entities of
          that type that exist in your Organization

        **Usage Data Exports**.

        - Select the Meters and Accounts whose usage data you want to include in the
          export each time the Export Schedule runs.
        - If _don't want to aggregate_ the usage data collected by the selected Meters,
          use **ORIGINAL** for `aggregationFrequency`, which is the _default_. This
          means the raw usage data collected by any type of Data Fields and the values
          for any Derived Fields on the selected Meters will be included in the export.
        - If you _do want to aggregate_ the usage data collected by the selected Meters,
          use one of the other options for `aggregationFrequency`: **HOUR**, **DAY**,
          **WEEK**, or **MONTH**. You _must_ then also specified an `aggregation` method
          to be used on the usage data before export. Importantly, if you do aggregate
          usage data, only the usage data collected by any numeric Data Fields on the
          selected Meters - those of type **MEASURE**, **INCOME**, or **COST** - will be
          included in the export each time the Export Schedule runs.

        Args:
          operational_data_types: A list of the entities whose operational data is included in the data export.

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
    def update(
        self,
        id: str,
        *,
        org_id: str | None = None,
        aggregation_frequency: Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"],
        source_type: Literal["USAGE", "OPERATIONAL"],
        time_period: Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "CURRENT_MONTH",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
        ],
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleUpdateResponse:
        """Update a Data Export Schedule for the given UUID.

        Each Schedule can be
        configured for exporting _only one_ of either Usage or Operational data:

        **Operational Data Exports**.

        - Use the `operationalDataTypes` parameter to specify the entities whose
          operational data you want to include in the export each time the Export
          Schedule runs.
        - For each of the entity types you select, each time the Export Schedule runs a
          separate file is compiled containing the operational data for all entities of
          that type that exist in your Organization

        **Usage Data Exports**.

        - Select the Meters and Accounts whose usage data you want to include in the
          export each time the Export Schedule runs.
        - If _don't want to aggregate_ the usage data collected by the selected Meters,
          use **ORIGINAL** for `aggregationFrequency`, which is the _default_. This
          means the raw usage data collected by any type of Data Fields and the values
          for any Derived Fields on the selected Meters will be included in the export.
        - If you _do want to aggregate_ the usage data collected by the selected Meters,
          use one of the other options for `aggregationFrequency`: **HOUR**, **DAY**,
          **WEEK**, or **MONTH**. You _must_ then also specified an `aggregation` method
          to be used on the usage data before export. Importantly, if you do aggregate
          usage data, only the usage data collected by any numeric Data Fields on the
          selected Meters - those of type **MEASURE**, **INCOME**, or **COST** - will be
          included in the export each time the Export Schedule runs.

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

    @required_args(["operational_data_types", "source_type"], ["aggregation_frequency", "source_type", "time_period"])
    def update(
        self,
        id: str,
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
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleUpdateResponse:
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ScheduleUpdateResponse,
            self._put(
                f"/organizations/{org_id}/dataexports/schedules/{id}",
                body=maybe_transform(
                    {
                        "operational_data_types": operational_data_types,
                        "source_type": source_type,
                        "version": version,
                        "aggregation_frequency": aggregation_frequency,
                        "time_period": time_period,
                        "account_ids": account_ids,
                        "aggregation": aggregation,
                        "meter_ids": meter_ids,
                    },
                    schedule_update_params.ScheduleUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ScheduleUpdateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        org_id: str | None = None,
        ids: List[str] | NotGiven = NOT_GIVEN,
        next_token: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursor[ScheduleListResponse]:
        """Retrieve a list of Data Export Schedules created for your Organization.

        You can
        filter the response by Schedules `ids`.

        The response will contain an array for both the operational and usage Data
        Export Schedules in your Organization.

        Args:
          ids: Data Export Schedule IDs to filter the returned list by.

          next_token: `nextToken` for multi page retrievals

          page_size: Number of schedules to retrieve per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return self._get_api_list(
            f"/organizations/{org_id}/dataexports/schedules",
            page=SyncCursor[ScheduleListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "next_token": next_token,
                        "page_size": page_size,
                    },
                    schedule_list_params.ScheduleListParams,
                ),
            ),
            model=ScheduleListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        org_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleDeleteResponse:
        """Delete the Data Export Schedule for the given UUID.

        Each Schedule can be
        configured for exporting _only one_ of either Usage or Operational data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ScheduleDeleteResponse,
            self._delete(
                f"/organizations/{org_id}/dataexports/schedules/{id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ScheduleDeleteResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncSchedulesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSchedulesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSchedulesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSchedulesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#with_streaming_response
        """
        return AsyncSchedulesResourceWithStreamingResponse(self)

    @overload
    async def create(
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
    ) -> ScheduleCreateResponse:
        """Create a new Data Export Schedule.

        Each Schedule can be configured for exporting
        _only one_ of either Usage or Operational data:

        **Operational Data Exports**.

        - Use the `operationalDataTypes` parameter to specify the entities whose
          operational data you want to include in the export each time the Export
          Schedule runs.
        - For each of the entity types you select, each time the Export Schedule runs a
          separate file is compiled containing the operational data for all entities of
          that type that exist in your Organization

        **Usage Data Exports**.

        - Select the Meters and Accounts whose usage data you want to include in the
          export each time the Export Schedule runs.
        - If _don't want to aggregate_ the usage data collected by the selected Meters,
          use **ORIGINAL** for `aggregationFrequency`, which is the _default_. This
          means the raw usage data collected by any type of Data Fields and the values
          for any Derived Fields on the selected Meters will be included in the export.
        - If you _do want to aggregate_ the usage data collected by the selected Meters,
          use one of the other options for `aggregationFrequency`: **HOUR**, **DAY**,
          **WEEK**, or **MONTH**. You _must_ then also specified an `aggregation` method
          to be used on the usage data before export. Importantly, if you do aggregate
          usage data, only the usage data collected by any numeric Data Fields on the
          selected Meters - those of type **MEASURE**, **INCOME**, or **COST** - will be
          included in the export each time the Export Schedule runs.

        Args:
          operational_data_types: A list of the entities whose operational data is included in the data export.

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
    async def create(
        self,
        *,
        org_id: str | None = None,
        aggregation_frequency: Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"],
        source_type: Literal["USAGE", "OPERATIONAL"],
        time_period: Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "CURRENT_MONTH",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
        ],
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleCreateResponse:
        """Create a new Data Export Schedule.

        Each Schedule can be configured for exporting
        _only one_ of either Usage or Operational data:

        **Operational Data Exports**.

        - Use the `operationalDataTypes` parameter to specify the entities whose
          operational data you want to include in the export each time the Export
          Schedule runs.
        - For each of the entity types you select, each time the Export Schedule runs a
          separate file is compiled containing the operational data for all entities of
          that type that exist in your Organization

        **Usage Data Exports**.

        - Select the Meters and Accounts whose usage data you want to include in the
          export each time the Export Schedule runs.
        - If _don't want to aggregate_ the usage data collected by the selected Meters,
          use **ORIGINAL** for `aggregationFrequency`, which is the _default_. This
          means the raw usage data collected by any type of Data Fields and the values
          for any Derived Fields on the selected Meters will be included in the export.
        - If you _do want to aggregate_ the usage data collected by the selected Meters,
          use one of the other options for `aggregationFrequency`: **HOUR**, **DAY**,
          **WEEK**, or **MONTH**. You _must_ then also specified an `aggregation` method
          to be used on the usage data before export. Importantly, if you do aggregate
          usage data, only the usage data collected by any numeric Data Fields on the
          selected Meters - those of type **MEASURE**, **INCOME**, or **COST** - will be
          included in the export each time the Export Schedule runs.

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

    @required_args(["operational_data_types", "source_type"], ["aggregation_frequency", "source_type", "time_period"])
    async def create(
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
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleCreateResponse:
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return cast(
            ScheduleCreateResponse,
            await self._post(
                f"/organizations/{org_id}/dataexports/schedules",
                body=await async_maybe_transform(
                    {
                        "operational_data_types": operational_data_types,
                        "source_type": source_type,
                        "version": version,
                        "aggregation_frequency": aggregation_frequency,
                        "time_period": time_period,
                        "account_ids": account_ids,
                        "aggregation": aggregation,
                        "meter_ids": meter_ids,
                    },
                    schedule_create_params.ScheduleCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ScheduleCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        id: str,
        *,
        org_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleRetrieveResponse:
        """Retrieve a Data Export Schedule for the given UUID.

        Each Schedule can be
        configured for exporting _only one_ of either Usage or Operational data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ScheduleRetrieveResponse,
            await self._get(
                f"/organizations/{org_id}/dataexports/schedules/{id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ScheduleRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    async def update(
        self,
        id: str,
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
    ) -> ScheduleUpdateResponse:
        """Update a Data Export Schedule for the given UUID.

        Each Schedule can be
        configured for exporting _only one_ of either Usage or Operational data:

        **Operational Data Exports**.

        - Use the `operationalDataTypes` parameter to specify the entities whose
          operational data you want to include in the export each time the Export
          Schedule runs.
        - For each of the entity types you select, each time the Export Schedule runs a
          separate file is compiled containing the operational data for all entities of
          that type that exist in your Organization

        **Usage Data Exports**.

        - Select the Meters and Accounts whose usage data you want to include in the
          export each time the Export Schedule runs.
        - If _don't want to aggregate_ the usage data collected by the selected Meters,
          use **ORIGINAL** for `aggregationFrequency`, which is the _default_. This
          means the raw usage data collected by any type of Data Fields and the values
          for any Derived Fields on the selected Meters will be included in the export.
        - If you _do want to aggregate_ the usage data collected by the selected Meters,
          use one of the other options for `aggregationFrequency`: **HOUR**, **DAY**,
          **WEEK**, or **MONTH**. You _must_ then also specified an `aggregation` method
          to be used on the usage data before export. Importantly, if you do aggregate
          usage data, only the usage data collected by any numeric Data Fields on the
          selected Meters - those of type **MEASURE**, **INCOME**, or **COST** - will be
          included in the export each time the Export Schedule runs.

        Args:
          operational_data_types: A list of the entities whose operational data is included in the data export.

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
    async def update(
        self,
        id: str,
        *,
        org_id: str | None = None,
        aggregation_frequency: Literal["ORIGINAL", "HOUR", "DAY", "WEEK", "MONTH"],
        source_type: Literal["USAGE", "OPERATIONAL"],
        time_period: Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "CURRENT_MONTH",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
        ],
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleUpdateResponse:
        """Update a Data Export Schedule for the given UUID.

        Each Schedule can be
        configured for exporting _only one_ of either Usage or Operational data:

        **Operational Data Exports**.

        - Use the `operationalDataTypes` parameter to specify the entities whose
          operational data you want to include in the export each time the Export
          Schedule runs.
        - For each of the entity types you select, each time the Export Schedule runs a
          separate file is compiled containing the operational data for all entities of
          that type that exist in your Organization

        **Usage Data Exports**.

        - Select the Meters and Accounts whose usage data you want to include in the
          export each time the Export Schedule runs.
        - If _don't want to aggregate_ the usage data collected by the selected Meters,
          use **ORIGINAL** for `aggregationFrequency`, which is the _default_. This
          means the raw usage data collected by any type of Data Fields and the values
          for any Derived Fields on the selected Meters will be included in the export.
        - If you _do want to aggregate_ the usage data collected by the selected Meters,
          use one of the other options for `aggregationFrequency`: **HOUR**, **DAY**,
          **WEEK**, or **MONTH**. You _must_ then also specified an `aggregation` method
          to be used on the usage data before export. Importantly, if you do aggregate
          usage data, only the usage data collected by any numeric Data Fields on the
          selected Meters - those of type **MEASURE**, **INCOME**, or **COST** - will be
          included in the export each time the Export Schedule runs.

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

    @required_args(["operational_data_types", "source_type"], ["aggregation_frequency", "source_type", "time_period"])
    async def update(
        self,
        id: str,
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
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregation: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN"] | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleUpdateResponse:
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ScheduleUpdateResponse,
            await self._put(
                f"/organizations/{org_id}/dataexports/schedules/{id}",
                body=await async_maybe_transform(
                    {
                        "operational_data_types": operational_data_types,
                        "source_type": source_type,
                        "version": version,
                        "aggregation_frequency": aggregation_frequency,
                        "time_period": time_period,
                        "account_ids": account_ids,
                        "aggregation": aggregation,
                        "meter_ids": meter_ids,
                    },
                    schedule_update_params.ScheduleUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ScheduleUpdateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        org_id: str | None = None,
        ids: List[str] | NotGiven = NOT_GIVEN,
        next_token: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[ScheduleListResponse, AsyncCursor[ScheduleListResponse]]:
        """Retrieve a list of Data Export Schedules created for your Organization.

        You can
        filter the response by Schedules `ids`.

        The response will contain an array for both the operational and usage Data
        Export Schedules in your Organization.

        Args:
          ids: Data Export Schedule IDs to filter the returned list by.

          next_token: `nextToken` for multi page retrievals

          page_size: Number of schedules to retrieve per page

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return self._get_api_list(
            f"/organizations/{org_id}/dataexports/schedules",
            page=AsyncCursor[ScheduleListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "next_token": next_token,
                        "page_size": page_size,
                    },
                    schedule_list_params.ScheduleListParams,
                ),
            ),
            model=ScheduleListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        org_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleDeleteResponse:
        """Delete the Data Export Schedule for the given UUID.

        Each Schedule can be
        configured for exporting _only one_ of either Usage or Operational data.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return cast(
            ScheduleDeleteResponse,
            await self._delete(
                f"/organizations/{org_id}/dataexports/schedules/{id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ScheduleDeleteResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class SchedulesResourceWithRawResponse:
    def __init__(self, schedules: SchedulesResource) -> None:
        self._schedules = schedules

        self.create = to_raw_response_wrapper(
            schedules.create,
        )
        self.retrieve = to_raw_response_wrapper(
            schedules.retrieve,
        )
        self.update = to_raw_response_wrapper(
            schedules.update,
        )
        self.list = to_raw_response_wrapper(
            schedules.list,
        )
        self.delete = to_raw_response_wrapper(
            schedules.delete,
        )


class AsyncSchedulesResourceWithRawResponse:
    def __init__(self, schedules: AsyncSchedulesResource) -> None:
        self._schedules = schedules

        self.create = async_to_raw_response_wrapper(
            schedules.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            schedules.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            schedules.update,
        )
        self.list = async_to_raw_response_wrapper(
            schedules.list,
        )
        self.delete = async_to_raw_response_wrapper(
            schedules.delete,
        )


class SchedulesResourceWithStreamingResponse:
    def __init__(self, schedules: SchedulesResource) -> None:
        self._schedules = schedules

        self.create = to_streamed_response_wrapper(
            schedules.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            schedules.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            schedules.update,
        )
        self.list = to_streamed_response_wrapper(
            schedules.list,
        )
        self.delete = to_streamed_response_wrapper(
            schedules.delete,
        )


class AsyncSchedulesResourceWithStreamingResponse:
    def __init__(self, schedules: AsyncSchedulesResource) -> None:
        self._schedules = schedules

        self.create = async_to_streamed_response_wrapper(
            schedules.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            schedules.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            schedules.update,
        )
        self.list = async_to_streamed_response_wrapper(
            schedules.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            schedules.delete,
        )
