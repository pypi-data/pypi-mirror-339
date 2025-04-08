# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal

import httpx

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
from ...pagination import SyncCursor, AsyncCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.data_exports import destination_list_params, destination_create_params, destination_update_params
from ...types.data_exports.destination_create_response import DestinationCreateResponse
from ...types.data_exports.destination_delete_response import DestinationDeleteResponse
from ...types.data_exports.destination_update_response import DestinationUpdateResponse
from ...types.data_exports.destination_retrieve_response import DestinationRetrieveResponse
from ...types.data_exports.data_export_destination_response import DataExportDestinationResponse

__all__ = ["DestinationsResource", "AsyncDestinationsResource"]


class DestinationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DestinationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DestinationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DestinationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#with_streaming_response
        """
        return DestinationsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        org_id: str | None = None,
        bucket_name: str,
        code: str,
        iam_role_arn: str,
        name: str,
        partition_order: Optional[Literal["TYPE_FIRST", "TIME_FIRST"]] | NotGiven = NOT_GIVEN,
        prefix: str | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DestinationCreateResponse:
        """
        Create a new Export Destination to use for your Data Export Schedules or Ad-Hoc
        Data Exports.

        **NOTE:** Currently, you can only create Export Destinations using an S3 bucket
        on your AWS Account.

        Args:
          bucket_name: Name of the S3 bucket for the Export Destination.

          code: The code of the Export Destination.

          iam_role_arn: To enable m3ter to upload a Data Exports to your S3 bucket, the service has to
              assume an IAM role with PutObject permission for the specified `bucketName`.
              Create a suitable IAM role in your AWS account and enter ARN:

              **Formatting Constraints:**

              - The IAM role ARN must begin with "arn:aws:iam".
              - The general format required is:
                "arn:aws:iam::<aws account id>:role/<role name>". For example:
                "arn:aws:iam::922609978421:role/IAMRole636".
              - If the `iamRoleArn` used doesn't comply with this format, then an error
                message will be returned.

              **More Details:** For more details and examples of the Permission and Trust
              Policies you can use to create the required IAM Role ARN, see
              [Creating Data Export Destinations](https://www.m3ter.com/docs/guides/data-exports/creating-data-export-destinations)
              in our main User documentation.

          name: The name of the Export Destination.

          partition_order: Specify how you want the file path to be structured in your bucket destination -
              by Time first (Default) or Type first.

              Type is dependent on whether the Export is for Usage data or Operational data:

              - **Usage.** Type is `measurements`.
              - **Operational.** Type is one of the entities for which operational data
                exports are available, such as `account`, `commitment`, `meter`, and so on.

              Example for Usage Data Export using .CSV format:

              - Time first:
                `{bucketName}/{prefix}/orgId={orgId}/date=2025-01-27/hour=10/type=measurements/b9a317a6-860a-40f9-9bf4-e65c44c72c94_measurements.csv.gz`
              - Type first:
                `{bucketName}/{prefix}/orgId={orgId}/type=measurements/date=2025-01-27/hour=10/b9a317a6-860a-40f9-9bf4-e65c44c72c94_measurements.csv.gz`

          prefix: Location in specified S3 bucket for the Export Destination. If you omit a
              `prefix`, then the root of the bucket will be used.

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
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return self._post(
            f"/organizations/{org_id}/dataexports/destinations",
            body=maybe_transform(
                {
                    "bucket_name": bucket_name,
                    "code": code,
                    "iam_role_arn": iam_role_arn,
                    "name": name,
                    "partition_order": partition_order,
                    "prefix": prefix,
                    "version": version,
                },
                destination_create_params.DestinationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationCreateResponse,
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
    ) -> DestinationRetrieveResponse:
        """
        Retrieve an Export Destination for the given UUID.

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
        return self._get(
            f"/organizations/{org_id}/dataexports/destinations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationRetrieveResponse,
        )

    def update(
        self,
        id: str,
        *,
        org_id: str | None = None,
        bucket_name: str,
        code: str,
        iam_role_arn: str,
        name: str,
        partition_order: Optional[Literal["TYPE_FIRST", "TIME_FIRST"]] | NotGiven = NOT_GIVEN,
        prefix: str | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DestinationUpdateResponse:
        """
        Update an Export Destination for the given UUID.

        **NOTE:** Currently, only Export Destinations using an S3 bucket on your AWS
        Account are supported.

        Args:
          bucket_name: Name of the S3 bucket for the Export Destination.

          code: The code of the Export Destination.

          iam_role_arn: To enable m3ter to upload a Data Exports to your S3 bucket, the service has to
              assume an IAM role with PutObject permission for the specified `bucketName`.
              Create a suitable IAM role in your AWS account and enter ARN:

              **Formatting Constraints:**

              - The IAM role ARN must begin with "arn:aws:iam".
              - The general format required is:
                "arn:aws:iam::<aws account id>:role/<role name>". For example:
                "arn:aws:iam::922609978421:role/IAMRole636".
              - If the `iamRoleArn` used doesn't comply with this format, then an error
                message will be returned.

              **More Details:** For more details and examples of the Permission and Trust
              Policies you can use to create the required IAM Role ARN, see
              [Creating Data Export Destinations](https://www.m3ter.com/docs/guides/data-exports/creating-data-export-destinations)
              in our main User documentation.

          name: The name of the Export Destination.

          partition_order: Specify how you want the file path to be structured in your bucket destination -
              by Time first (Default) or Type first.

              Type is dependent on whether the Export is for Usage data or Operational data:

              - **Usage.** Type is `measurements`.
              - **Operational.** Type is one of the entities for which operational data
                exports are available, such as `account`, `commitment`, `meter`, and so on.

              Example for Usage Data Export using .CSV format:

              - Time first:
                `{bucketName}/{prefix}/orgId={orgId}/date=2025-01-27/hour=10/type=measurements/b9a317a6-860a-40f9-9bf4-e65c44c72c94_measurements.csv.gz`
              - Type first:
                `{bucketName}/{prefix}/orgId={orgId}/type=measurements/date=2025-01-27/hour=10/b9a317a6-860a-40f9-9bf4-e65c44c72c94_measurements.csv.gz`

          prefix: Location in specified S3 bucket for the Export Destination. If you omit a
              `prefix`, then the root of the bucket will be used.

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
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._put(
            f"/organizations/{org_id}/dataexports/destinations/{id}",
            body=maybe_transform(
                {
                    "bucket_name": bucket_name,
                    "code": code,
                    "iam_role_arn": iam_role_arn,
                    "name": name,
                    "partition_order": partition_order,
                    "prefix": prefix,
                    "version": version,
                },
                destination_update_params.DestinationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationUpdateResponse,
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
    ) -> SyncCursor[DataExportDestinationResponse]:
        """Retrieve a list of Export Destination entities.

        You can filter the list of
        Destinations returned by UUID.

        Args:
          ids: List of Export Destination UUIDs to retrieve.

          next_token: nextToken for multi page retrievals

          page_size: Number of returned Export Destinations to list per page.

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
            f"/organizations/{org_id}/dataexports/destinations",
            page=SyncCursor[DataExportDestinationResponse],
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
                    destination_list_params.DestinationListParams,
                ),
            ),
            model=DataExportDestinationResponse,
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
    ) -> DestinationDeleteResponse:
        """
        Delete an Export Destination for the given UUID.

        **NOTE:** If you attempt to delete an Export Destination that is currently
        linked to a Data Export Schedule, an error message is returned and you won't be
        able to delete the Destination.

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
        return self._delete(
            f"/organizations/{org_id}/dataexports/destinations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationDeleteResponse,
        )


class AsyncDestinationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDestinationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDestinationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDestinationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/m3ter-com/m3ter-sdk-python#with_streaming_response
        """
        return AsyncDestinationsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        org_id: str | None = None,
        bucket_name: str,
        code: str,
        iam_role_arn: str,
        name: str,
        partition_order: Optional[Literal["TYPE_FIRST", "TIME_FIRST"]] | NotGiven = NOT_GIVEN,
        prefix: str | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DestinationCreateResponse:
        """
        Create a new Export Destination to use for your Data Export Schedules or Ad-Hoc
        Data Exports.

        **NOTE:** Currently, you can only create Export Destinations using an S3 bucket
        on your AWS Account.

        Args:
          bucket_name: Name of the S3 bucket for the Export Destination.

          code: The code of the Export Destination.

          iam_role_arn: To enable m3ter to upload a Data Exports to your S3 bucket, the service has to
              assume an IAM role with PutObject permission for the specified `bucketName`.
              Create a suitable IAM role in your AWS account and enter ARN:

              **Formatting Constraints:**

              - The IAM role ARN must begin with "arn:aws:iam".
              - The general format required is:
                "arn:aws:iam::<aws account id>:role/<role name>". For example:
                "arn:aws:iam::922609978421:role/IAMRole636".
              - If the `iamRoleArn` used doesn't comply with this format, then an error
                message will be returned.

              **More Details:** For more details and examples of the Permission and Trust
              Policies you can use to create the required IAM Role ARN, see
              [Creating Data Export Destinations](https://www.m3ter.com/docs/guides/data-exports/creating-data-export-destinations)
              in our main User documentation.

          name: The name of the Export Destination.

          partition_order: Specify how you want the file path to be structured in your bucket destination -
              by Time first (Default) or Type first.

              Type is dependent on whether the Export is for Usage data or Operational data:

              - **Usage.** Type is `measurements`.
              - **Operational.** Type is one of the entities for which operational data
                exports are available, such as `account`, `commitment`, `meter`, and so on.

              Example for Usage Data Export using .CSV format:

              - Time first:
                `{bucketName}/{prefix}/orgId={orgId}/date=2025-01-27/hour=10/type=measurements/b9a317a6-860a-40f9-9bf4-e65c44c72c94_measurements.csv.gz`
              - Type first:
                `{bucketName}/{prefix}/orgId={orgId}/type=measurements/date=2025-01-27/hour=10/b9a317a6-860a-40f9-9bf4-e65c44c72c94_measurements.csv.gz`

          prefix: Location in specified S3 bucket for the Export Destination. If you omit a
              `prefix`, then the root of the bucket will be used.

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
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        return await self._post(
            f"/organizations/{org_id}/dataexports/destinations",
            body=await async_maybe_transform(
                {
                    "bucket_name": bucket_name,
                    "code": code,
                    "iam_role_arn": iam_role_arn,
                    "name": name,
                    "partition_order": partition_order,
                    "prefix": prefix,
                    "version": version,
                },
                destination_create_params.DestinationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationCreateResponse,
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
    ) -> DestinationRetrieveResponse:
        """
        Retrieve an Export Destination for the given UUID.

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
        return await self._get(
            f"/organizations/{org_id}/dataexports/destinations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationRetrieveResponse,
        )

    async def update(
        self,
        id: str,
        *,
        org_id: str | None = None,
        bucket_name: str,
        code: str,
        iam_role_arn: str,
        name: str,
        partition_order: Optional[Literal["TYPE_FIRST", "TIME_FIRST"]] | NotGiven = NOT_GIVEN,
        prefix: str | NotGiven = NOT_GIVEN,
        version: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DestinationUpdateResponse:
        """
        Update an Export Destination for the given UUID.

        **NOTE:** Currently, only Export Destinations using an S3 bucket on your AWS
        Account are supported.

        Args:
          bucket_name: Name of the S3 bucket for the Export Destination.

          code: The code of the Export Destination.

          iam_role_arn: To enable m3ter to upload a Data Exports to your S3 bucket, the service has to
              assume an IAM role with PutObject permission for the specified `bucketName`.
              Create a suitable IAM role in your AWS account and enter ARN:

              **Formatting Constraints:**

              - The IAM role ARN must begin with "arn:aws:iam".
              - The general format required is:
                "arn:aws:iam::<aws account id>:role/<role name>". For example:
                "arn:aws:iam::922609978421:role/IAMRole636".
              - If the `iamRoleArn` used doesn't comply with this format, then an error
                message will be returned.

              **More Details:** For more details and examples of the Permission and Trust
              Policies you can use to create the required IAM Role ARN, see
              [Creating Data Export Destinations](https://www.m3ter.com/docs/guides/data-exports/creating-data-export-destinations)
              in our main User documentation.

          name: The name of the Export Destination.

          partition_order: Specify how you want the file path to be structured in your bucket destination -
              by Time first (Default) or Type first.

              Type is dependent on whether the Export is for Usage data or Operational data:

              - **Usage.** Type is `measurements`.
              - **Operational.** Type is one of the entities for which operational data
                exports are available, such as `account`, `commitment`, `meter`, and so on.

              Example for Usage Data Export using .CSV format:

              - Time first:
                `{bucketName}/{prefix}/orgId={orgId}/date=2025-01-27/hour=10/type=measurements/b9a317a6-860a-40f9-9bf4-e65c44c72c94_measurements.csv.gz`
              - Type first:
                `{bucketName}/{prefix}/orgId={orgId}/type=measurements/date=2025-01-27/hour=10/b9a317a6-860a-40f9-9bf4-e65c44c72c94_measurements.csv.gz`

          prefix: Location in specified S3 bucket for the Export Destination. If you omit a
              `prefix`, then the root of the bucket will be used.

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
        if org_id is None:
            org_id = self._client._get_org_id_path_param()
        if not org_id:
            raise ValueError(f"Expected a non-empty value for `org_id` but received {org_id!r}")
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._put(
            f"/organizations/{org_id}/dataexports/destinations/{id}",
            body=await async_maybe_transform(
                {
                    "bucket_name": bucket_name,
                    "code": code,
                    "iam_role_arn": iam_role_arn,
                    "name": name,
                    "partition_order": partition_order,
                    "prefix": prefix,
                    "version": version,
                },
                destination_update_params.DestinationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationUpdateResponse,
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
    ) -> AsyncPaginator[DataExportDestinationResponse, AsyncCursor[DataExportDestinationResponse]]:
        """Retrieve a list of Export Destination entities.

        You can filter the list of
        Destinations returned by UUID.

        Args:
          ids: List of Export Destination UUIDs to retrieve.

          next_token: nextToken for multi page retrievals

          page_size: Number of returned Export Destinations to list per page.

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
            f"/organizations/{org_id}/dataexports/destinations",
            page=AsyncCursor[DataExportDestinationResponse],
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
                    destination_list_params.DestinationListParams,
                ),
            ),
            model=DataExportDestinationResponse,
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
    ) -> DestinationDeleteResponse:
        """
        Delete an Export Destination for the given UUID.

        **NOTE:** If you attempt to delete an Export Destination that is currently
        linked to a Data Export Schedule, an error message is returned and you won't be
        able to delete the Destination.

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
        return await self._delete(
            f"/organizations/{org_id}/dataexports/destinations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DestinationDeleteResponse,
        )


class DestinationsResourceWithRawResponse:
    def __init__(self, destinations: DestinationsResource) -> None:
        self._destinations = destinations

        self.create = to_raw_response_wrapper(
            destinations.create,
        )
        self.retrieve = to_raw_response_wrapper(
            destinations.retrieve,
        )
        self.update = to_raw_response_wrapper(
            destinations.update,
        )
        self.list = to_raw_response_wrapper(
            destinations.list,
        )
        self.delete = to_raw_response_wrapper(
            destinations.delete,
        )


class AsyncDestinationsResourceWithRawResponse:
    def __init__(self, destinations: AsyncDestinationsResource) -> None:
        self._destinations = destinations

        self.create = async_to_raw_response_wrapper(
            destinations.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            destinations.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            destinations.update,
        )
        self.list = async_to_raw_response_wrapper(
            destinations.list,
        )
        self.delete = async_to_raw_response_wrapper(
            destinations.delete,
        )


class DestinationsResourceWithStreamingResponse:
    def __init__(self, destinations: DestinationsResource) -> None:
        self._destinations = destinations

        self.create = to_streamed_response_wrapper(
            destinations.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            destinations.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            destinations.update,
        )
        self.list = to_streamed_response_wrapper(
            destinations.list,
        )
        self.delete = to_streamed_response_wrapper(
            destinations.delete,
        )


class AsyncDestinationsResourceWithStreamingResponse:
    def __init__(self, destinations: AsyncDestinationsResource) -> None:
        self._destinations = destinations

        self.create = async_to_streamed_response_wrapper(
            destinations.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            destinations.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            destinations.update,
        )
        self.list = async_to_streamed_response_wrapper(
            destinations.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            destinations.delete,
        )
