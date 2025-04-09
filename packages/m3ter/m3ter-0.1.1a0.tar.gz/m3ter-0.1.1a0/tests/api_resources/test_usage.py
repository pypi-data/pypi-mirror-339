# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from m3ter import M3ter, AsyncM3ter
from m3ter.types import (
    UsageQueryResponse,
    DownloadURLResponse,
    SubmitMeasurementsResponse,
)
from tests.utils import assert_matches_type
from m3ter._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsage:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_get_failed_ingest_download_url(self, client: M3ter) -> None:
        usage = client.usage.get_failed_ingest_download_url(
            org_id="orgId",
        )
        assert_matches_type(DownloadURLResponse, usage, path=["response"])

    @parametrize
    def test_method_get_failed_ingest_download_url_with_all_params(self, client: M3ter) -> None:
        usage = client.usage.get_failed_ingest_download_url(
            org_id="orgId",
            file="file",
        )
        assert_matches_type(DownloadURLResponse, usage, path=["response"])

    @parametrize
    def test_raw_response_get_failed_ingest_download_url(self, client: M3ter) -> None:
        response = client.usage.with_raw_response.get_failed_ingest_download_url(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage = response.parse()
        assert_matches_type(DownloadURLResponse, usage, path=["response"])

    @parametrize
    def test_streaming_response_get_failed_ingest_download_url(self, client: M3ter) -> None:
        with client.usage.with_streaming_response.get_failed_ingest_download_url(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage = response.parse()
            assert_matches_type(DownloadURLResponse, usage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get_failed_ingest_download_url(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.usage.with_raw_response.get_failed_ingest_download_url(
                org_id="",
            )

    @parametrize
    def test_method_query(self, client: M3ter) -> None:
        usage = client.usage.query(
            org_id="orgId",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(UsageQueryResponse, usage, path=["response"])

    @parametrize
    def test_method_query_with_all_params(self, client: M3ter) -> None:
        usage = client.usage.query(
            org_id="orgId",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            account_ids=["string"],
            aggregations=[
                {
                    "field_code": "x",
                    "field_type": "DIMENSION",
                    "function": "SUM",
                    "meter_id": "x",
                }
            ],
            dimension_filters=[
                {
                    "field_code": "x",
                    "meter_id": "x",
                    "values": ["string"],
                }
            ],
            groups=[{"group_type": "ACCOUNT"}],
            limit=1,
            meter_ids=["string"],
        )
        assert_matches_type(UsageQueryResponse, usage, path=["response"])

    @parametrize
    def test_raw_response_query(self, client: M3ter) -> None:
        response = client.usage.with_raw_response.query(
            org_id="orgId",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage = response.parse()
        assert_matches_type(UsageQueryResponse, usage, path=["response"])

    @parametrize
    def test_streaming_response_query(self, client: M3ter) -> None:
        with client.usage.with_streaming_response.query(
            org_id="orgId",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage = response.parse()
            assert_matches_type(UsageQueryResponse, usage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.usage.with_raw_response.query(
                org_id="",
                end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
                start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

    @parametrize
    def test_method_submit(self, client: M3ter) -> None:
        usage = client.usage.submit(
            org_id="orgId",
            measurements=[
                {
                    "account": "Acme Corp",
                    "meter": "string",
                    "ts": parse_datetime("2022-08-24T14:15:22Z"),
                }
            ],
        )
        assert_matches_type(SubmitMeasurementsResponse, usage, path=["response"])

    @parametrize
    def test_raw_response_submit(self, client: M3ter) -> None:
        response = client.usage.with_raw_response.submit(
            org_id="orgId",
            measurements=[
                {
                    "account": "Acme Corp",
                    "meter": "string",
                    "ts": parse_datetime("2022-08-24T14:15:22Z"),
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage = response.parse()
        assert_matches_type(SubmitMeasurementsResponse, usage, path=["response"])

    @parametrize
    def test_streaming_response_submit(self, client: M3ter) -> None:
        with client.usage.with_streaming_response.submit(
            org_id="orgId",
            measurements=[
                {
                    "account": "Acme Corp",
                    "meter": "string",
                    "ts": parse_datetime("2022-08-24T14:15:22Z"),
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage = response.parse()
            assert_matches_type(SubmitMeasurementsResponse, usage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_submit(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.usage.with_raw_response.submit(
                org_id="",
                measurements=[
                    {
                        "account": "Acme Corp",
                        "meter": "string",
                        "ts": parse_datetime("2022-08-24T14:15:22Z"),
                    }
                ],
            )


class TestAsyncUsage:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_get_failed_ingest_download_url(self, async_client: AsyncM3ter) -> None:
        usage = await async_client.usage.get_failed_ingest_download_url(
            org_id="orgId",
        )
        assert_matches_type(DownloadURLResponse, usage, path=["response"])

    @parametrize
    async def test_method_get_failed_ingest_download_url_with_all_params(self, async_client: AsyncM3ter) -> None:
        usage = await async_client.usage.get_failed_ingest_download_url(
            org_id="orgId",
            file="file",
        )
        assert_matches_type(DownloadURLResponse, usage, path=["response"])

    @parametrize
    async def test_raw_response_get_failed_ingest_download_url(self, async_client: AsyncM3ter) -> None:
        response = await async_client.usage.with_raw_response.get_failed_ingest_download_url(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage = await response.parse()
        assert_matches_type(DownloadURLResponse, usage, path=["response"])

    @parametrize
    async def test_streaming_response_get_failed_ingest_download_url(self, async_client: AsyncM3ter) -> None:
        async with async_client.usage.with_streaming_response.get_failed_ingest_download_url(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage = await response.parse()
            assert_matches_type(DownloadURLResponse, usage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get_failed_ingest_download_url(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.usage.with_raw_response.get_failed_ingest_download_url(
                org_id="",
            )

    @parametrize
    async def test_method_query(self, async_client: AsyncM3ter) -> None:
        usage = await async_client.usage.query(
            org_id="orgId",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(UsageQueryResponse, usage, path=["response"])

    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncM3ter) -> None:
        usage = await async_client.usage.query(
            org_id="orgId",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            account_ids=["string"],
            aggregations=[
                {
                    "field_code": "x",
                    "field_type": "DIMENSION",
                    "function": "SUM",
                    "meter_id": "x",
                }
            ],
            dimension_filters=[
                {
                    "field_code": "x",
                    "meter_id": "x",
                    "values": ["string"],
                }
            ],
            groups=[{"group_type": "ACCOUNT"}],
            limit=1,
            meter_ids=["string"],
        )
        assert_matches_type(UsageQueryResponse, usage, path=["response"])

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncM3ter) -> None:
        response = await async_client.usage.with_raw_response.query(
            org_id="orgId",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage = await response.parse()
        assert_matches_type(UsageQueryResponse, usage, path=["response"])

    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncM3ter) -> None:
        async with async_client.usage.with_streaming_response.query(
            org_id="orgId",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage = await response.parse()
            assert_matches_type(UsageQueryResponse, usage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.usage.with_raw_response.query(
                org_id="",
                end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
                start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

    @parametrize
    async def test_method_submit(self, async_client: AsyncM3ter) -> None:
        usage = await async_client.usage.submit(
            org_id="orgId",
            measurements=[
                {
                    "account": "Acme Corp",
                    "meter": "string",
                    "ts": parse_datetime("2022-08-24T14:15:22Z"),
                }
            ],
        )
        assert_matches_type(SubmitMeasurementsResponse, usage, path=["response"])

    @parametrize
    async def test_raw_response_submit(self, async_client: AsyncM3ter) -> None:
        response = await async_client.usage.with_raw_response.submit(
            org_id="orgId",
            measurements=[
                {
                    "account": "Acme Corp",
                    "meter": "string",
                    "ts": parse_datetime("2022-08-24T14:15:22Z"),
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        usage = await response.parse()
        assert_matches_type(SubmitMeasurementsResponse, usage, path=["response"])

    @parametrize
    async def test_streaming_response_submit(self, async_client: AsyncM3ter) -> None:
        async with async_client.usage.with_streaming_response.submit(
            org_id="orgId",
            measurements=[
                {
                    "account": "Acme Corp",
                    "meter": "string",
                    "ts": parse_datetime("2022-08-24T14:15:22Z"),
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            usage = await response.parse()
            assert_matches_type(SubmitMeasurementsResponse, usage, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_submit(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.usage.with_raw_response.submit(
                org_id="",
                measurements=[
                    {
                        "account": "Acme Corp",
                        "meter": "string",
                        "ts": parse_datetime("2022-08-24T14:15:22Z"),
                    }
                ],
            )
