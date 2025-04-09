# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from datetime import datetime

import httpx

from ...types import usage_query_params, usage_submit_params, usage_get_failed_ingest_download_url_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
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
from ..._base_client import make_request_options
from .file_uploads.file_uploads import (
    FileUploadsResource,
    AsyncFileUploadsResource,
    FileUploadsResourceWithRawResponse,
    AsyncFileUploadsResourceWithRawResponse,
    FileUploadsResourceWithStreamingResponse,
    AsyncFileUploadsResourceWithStreamingResponse,
)
from ...types.usage_query_response import UsageQueryResponse
from ...types.download_url_response import DownloadURLResponse
from ...types.submit_measurements_response import SubmitMeasurementsResponse

__all__ = ["UsageResource", "AsyncUsageResource"]


class UsageResource(SyncAPIResource):
    @cached_property
    def file_uploads(self) -> FileUploadsResource:
        return FileUploadsResource(self._client)

    @cached_property
    def with_raw_response(self) -> UsageResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#accessing-raw-response-data-eg-headers
        """
        return UsageResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsageResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#with_streaming_response
        """
        return UsageResourceWithStreamingResponse(self)

    def get_failed_ingest_download_url(
        self,
        *,
        org_id: str | None = None,
        file: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DownloadURLResponse:
        """
        Returns a presigned download URL for failed ingest file download based on the
        file path provided.

        If a usage data ingest measurement you submit to the m3ter platform fails, an
        `ingest.validation.failure` Event is generated. Use this call to obtain a
        download URL which you can then use to download a file containing details of
        what went wrong with the attempted usage data measurement ingest, and allowing
        you to follow-up and resolve the issue.

        To obtain the `file` query parameter:

        - Use the
          [List Events](https://www.m3ter.com/docs/api#tag/Events/operation/ListEventFields)
          call with the `ingest.validation.failure` for the `eventName` query parameter.
        - The response contains a `getDownloadUrl` response parameter and this contains
          the file path you can use to obtain the failed ingest file download URL.

        **Notes:**

        - The presigned Url returned to use for failed ingest file download is
          time-bound and expires after 5 minutes.
        - If you make a List Events call for `ingest.validation.failure` Events in your
          Organization, then you can perform this **GET** call using the full URL
          returned for any ingest failure Event to obtain a failed ingest file download
          URL for the Event.

        Args:
          file: The file path

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return self._get(
            f"/organizations/{org_id}/measurements/failedIngest/getDownloadUrl",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"file": file}, usage_get_failed_ingest_download_url_params.UsageGetFailedIngestDownloadURLParams
                ),
            ),
            cast_to=DownloadURLResponse,
        )

    def query(
        self,
        *,
        org_id: str | None = None,
        end_date: Union[str, datetime],
        start_date: Union[str, datetime],
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregations: Iterable[usage_query_params.Aggregation] | NotGiven = NOT_GIVEN,
        dimension_filters: Iterable[usage_query_params.DimensionFilter] | NotGiven = NOT_GIVEN,
        groups: Iterable[usage_query_params.Group] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UsageQueryResponse:
        """
        Query and filter usage data

        Args:
          end_date: ISO 8601 formatted end date to filter by.

          start_date: ISO 8601 formatted start date to filter by.

          account_ids

          aggregations

          dimension_filters

          groups

          limit

          meter_ids

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return self._post(
            f"/organizations/{org_id}/usage/query",
            body=maybe_transform(
                {
                    "end_date": end_date,
                    "start_date": start_date,
                    "account_ids": account_ids,
                    "aggregations": aggregations,
                    "dimension_filters": dimension_filters,
                    "groups": groups,
                    "limit": limit,
                    "meter_ids": meter_ids,
                },
                usage_query_params.UsageQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UsageQueryResponse,
        )

    def submit(
        self,
        *,
        org_id: str | None = None,
        measurements: Iterable[usage_submit_params.Measurement],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubmitMeasurementsResponse:
        """Submit a measurement or multiple measurements to the m3ter platform.

        The maximum
        size of the payload needs to be less than 512,000 bytes.

        **NOTES:**

        - **Non-existent Accounts.** The `account` request parameter is required.
          However, if you want to submit a usage data measurement for an Account which
          does not yet exist in your Organization, you can use an `account` code for a
          non-existent Account. A new skeleton Account will be automatically created.
          The usage data measurement is accepted and ingested as data belonging to the
          new auto-created Account. At a later date, you can edit the Account's
          Code,??Name, and??e-mail address. For more details, see
          [Submittting Usage Data for Non-Existent Accounts](https://www.m3ter.com/docs/guides/billing-and-usage-data/submitting-usage-data/submitting-usage-data-for-non-existent-accounts)
          in our main documentation.
        - **Usage Data Adjustments.** If you need to make corrections for billing
          retrospectively against an Account, you can use date/time values in the past
          for the `ts` (timestamp) request parameter to submit positive or negative
          usage data amounts to correct and reconcile earlier billing anomalies. For
          more details, see
          [Submittting Usage Data Adjustments Using Timestamp](https://www.m3ter.com/docs/guides/billing-and-usage-data/submitting-usage-data/submitting-usage-data-adjustments-using-timestamp)
          in our main documentation.
        - **Ingest Validation Failure Events.** After the intial submission of a usage
          data measurement to the Ingest API, a data enrichment stage is performed to
          check for any errors in the usage data measurement, such as a missing field.
          If an error is identified, this might result in the submission being rejected.
          In these cases, an _ingest validation failure_ Event is generated, which you
          can review on the
          [Ingest Events](https://www.m3ter.com/docs/guides/billing-and-usage-data/submitting-usage-data/reviewing-and-resolving-ingest-events)
          page in the Console. See also the
          [Events](https://www.m3ter.com/docs/api#tag/Events) section in this API
          Reference.

        **IMPORTANT! - Use of PII:** The use of any of your end-customers' Personally
        Identifiable Information (PII) in m3ter is restricted to a few fields on the
        **Account** entity. Please ensure that any measurements you submit do not
        contain any end-customer PII data. See the
        [Introduction section](https://www.m3ter.com/docs/api#section/Introduction)
        above for more details.

        Args:
          measurements: Request containing the usage data measurements for submission.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return self._post(
            f"/organizations/{org_id}/measurements",
            body=maybe_transform({"measurements": measurements}, usage_submit_params.UsageSubmitParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubmitMeasurementsResponse,
        )


class AsyncUsageResource(AsyncAPIResource):
    @cached_property
    def file_uploads(self) -> AsyncFileUploadsResource:
        return AsyncFileUploadsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncUsageResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUsageResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsageResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#with_streaming_response
        """
        return AsyncUsageResourceWithStreamingResponse(self)

    async def get_failed_ingest_download_url(
        self,
        *,
        org_id: str | None = None,
        file: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DownloadURLResponse:
        """
        Returns a presigned download URL for failed ingest file download based on the
        file path provided.

        If a usage data ingest measurement you submit to the m3ter platform fails, an
        `ingest.validation.failure` Event is generated. Use this call to obtain a
        download URL which you can then use to download a file containing details of
        what went wrong with the attempted usage data measurement ingest, and allowing
        you to follow-up and resolve the issue.

        To obtain the `file` query parameter:

        - Use the
          [List Events](https://www.m3ter.com/docs/api#tag/Events/operation/ListEventFields)
          call with the `ingest.validation.failure` for the `eventName` query parameter.
        - The response contains a `getDownloadUrl` response parameter and this contains
          the file path you can use to obtain the failed ingest file download URL.

        **Notes:**

        - The presigned Url returned to use for failed ingest file download is
          time-bound and expires after 5 minutes.
        - If you make a List Events call for `ingest.validation.failure` Events in your
          Organization, then you can perform this **GET** call using the full URL
          returned for any ingest failure Event to obtain a failed ingest file download
          URL for the Event.

        Args:
          file: The file path

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return await self._get(
            f"/organizations/{org_id}/measurements/failedIngest/getDownloadUrl",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"file": file}, usage_get_failed_ingest_download_url_params.UsageGetFailedIngestDownloadURLParams
                ),
            ),
            cast_to=DownloadURLResponse,
        )

    async def query(
        self,
        *,
        org_id: str | None = None,
        end_date: Union[str, datetime],
        start_date: Union[str, datetime],
        account_ids: List[str] | NotGiven = NOT_GIVEN,
        aggregations: Iterable[usage_query_params.Aggregation] | NotGiven = NOT_GIVEN,
        dimension_filters: Iterable[usage_query_params.DimensionFilter] | NotGiven = NOT_GIVEN,
        groups: Iterable[usage_query_params.Group] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        meter_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UsageQueryResponse:
        """
        Query and filter usage data

        Args:
          end_date: ISO 8601 formatted end date to filter by.

          start_date: ISO 8601 formatted start date to filter by.

          account_ids

          aggregations

          dimension_filters

          groups

          limit

          meter_ids

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return await self._post(
            f"/organizations/{org_id}/usage/query",
            body=await async_maybe_transform(
                {
                    "end_date": end_date,
                    "start_date": start_date,
                    "account_ids": account_ids,
                    "aggregations": aggregations,
                    "dimension_filters": dimension_filters,
                    "groups": groups,
                    "limit": limit,
                    "meter_ids": meter_ids,
                },
                usage_query_params.UsageQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UsageQueryResponse,
        )

    async def submit(
        self,
        *,
        org_id: str | None = None,
        measurements: Iterable[usage_submit_params.Measurement],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SubmitMeasurementsResponse:
        """Submit a measurement or multiple measurements to the m3ter platform.

        The maximum
        size of the payload needs to be less than 512,000 bytes.

        **NOTES:**

        - **Non-existent Accounts.** The `account` request parameter is required.
          However, if you want to submit a usage data measurement for an Account which
          does not yet exist in your Organization, you can use an `account` code for a
          non-existent Account. A new skeleton Account will be automatically created.
          The usage data measurement is accepted and ingested as data belonging to the
          new auto-created Account. At a later date, you can edit the Account's
          Code,??Name, and??e-mail address. For more details, see
          [Submittting Usage Data for Non-Existent Accounts](https://www.m3ter.com/docs/guides/billing-and-usage-data/submitting-usage-data/submitting-usage-data-for-non-existent-accounts)
          in our main documentation.
        - **Usage Data Adjustments.** If you need to make corrections for billing
          retrospectively against an Account, you can use date/time values in the past
          for the `ts` (timestamp) request parameter to submit positive or negative
          usage data amounts to correct and reconcile earlier billing anomalies. For
          more details, see
          [Submittting Usage Data Adjustments Using Timestamp](https://www.m3ter.com/docs/guides/billing-and-usage-data/submitting-usage-data/submitting-usage-data-adjustments-using-timestamp)
          in our main documentation.
        - **Ingest Validation Failure Events.** After the intial submission of a usage
          data measurement to the Ingest API, a data enrichment stage is performed to
          check for any errors in the usage data measurement, such as a missing field.
          If an error is identified, this might result in the submission being rejected.
          In these cases, an _ingest validation failure_ Event is generated, which you
          can review on the
          [Ingest Events](https://www.m3ter.com/docs/guides/billing-and-usage-data/submitting-usage-data/reviewing-and-resolving-ingest-events)
          page in the Console. See also the
          [Events](https://www.m3ter.com/docs/api#tag/Events) section in this API
          Reference.

        **IMPORTANT! - Use of PII:** The use of any of your end-customers' Personally
        Identifiable Information (PII) in m3ter is restricted to a few fields on the
        **Account** entity. Please ensure that any measurements you submit do not
        contain any end-customer PII data. See the
        [Introduction section](https://www.m3ter.com/docs/api#section/Introduction)
        above for more details.

        Args:
          measurements: Request containing the usage data measurements for submission.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return await self._post(
            f"/organizations/{org_id}/measurements",
            body=await async_maybe_transform({"measurements": measurements}, usage_submit_params.UsageSubmitParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SubmitMeasurementsResponse,
        )


class UsageResourceWithRawResponse:
    def __init__(self, usage: UsageResource) -> None:
        self._usage = usage

        self.get_failed_ingest_download_url = to_raw_response_wrapper(
            usage.get_failed_ingest_download_url,
        )
        self.query = to_raw_response_wrapper(
            usage.query,
        )
        self.submit = to_raw_response_wrapper(
            usage.submit,
        )

    @cached_property
    def file_uploads(self) -> FileUploadsResourceWithRawResponse:
        return FileUploadsResourceWithRawResponse(self._usage.file_uploads)


class AsyncUsageResourceWithRawResponse:
    def __init__(self, usage: AsyncUsageResource) -> None:
        self._usage = usage

        self.get_failed_ingest_download_url = async_to_raw_response_wrapper(
            usage.get_failed_ingest_download_url,
        )
        self.query = async_to_raw_response_wrapper(
            usage.query,
        )
        self.submit = async_to_raw_response_wrapper(
            usage.submit,
        )

    @cached_property
    def file_uploads(self) -> AsyncFileUploadsResourceWithRawResponse:
        return AsyncFileUploadsResourceWithRawResponse(self._usage.file_uploads)


class UsageResourceWithStreamingResponse:
    def __init__(self, usage: UsageResource) -> None:
        self._usage = usage

        self.get_failed_ingest_download_url = to_streamed_response_wrapper(
            usage.get_failed_ingest_download_url,
        )
        self.query = to_streamed_response_wrapper(
            usage.query,
        )
        self.submit = to_streamed_response_wrapper(
            usage.submit,
        )

    @cached_property
    def file_uploads(self) -> FileUploadsResourceWithStreamingResponse:
        return FileUploadsResourceWithStreamingResponse(self._usage.file_uploads)


class AsyncUsageResourceWithStreamingResponse:
    def __init__(self, usage: AsyncUsageResource) -> None:
        self._usage = usage

        self.get_failed_ingest_download_url = async_to_streamed_response_wrapper(
            usage.get_failed_ingest_download_url,
        )
        self.query = async_to_streamed_response_wrapper(
            usage.query,
        )
        self.submit = async_to_streamed_response_wrapper(
            usage.submit,
        )

    @cached_property
    def file_uploads(self) -> AsyncFileUploadsResourceWithStreamingResponse:
        return AsyncFileUploadsResourceWithStreamingResponse(self._usage.file_uploads)
