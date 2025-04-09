# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from m3ter import M3ter, AsyncM3ter
from tests.utils import assert_matches_type
from m3ter.pagination import SyncCursor, AsyncCursor
from m3ter.types.data_exports import (
    DestinationCreateResponse,
    DestinationDeleteResponse,
    DestinationUpdateResponse,
    DestinationRetrieveResponse,
    DataExportDestinationResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDestinations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: M3ter) -> None:
        destination = client.data_exports.destinations.create(
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        )
        assert_matches_type(DestinationCreateResponse, destination, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: M3ter) -> None:
        destination = client.data_exports.destinations.create(
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
            partition_order="TYPE_FIRST",
            prefix="prefix",
            version=0,
        )
        assert_matches_type(DestinationCreateResponse, destination, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: M3ter) -> None:
        response = client.data_exports.destinations.with_raw_response.create(
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = response.parse()
        assert_matches_type(DestinationCreateResponse, destination, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: M3ter) -> None:
        with client.data_exports.destinations.with_streaming_response.create(
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = response.parse()
            assert_matches_type(DestinationCreateResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.data_exports.destinations.with_raw_response.create(
                org_id="",
                bucket_name="xxx",
                code="JS!?Q0]r] ]$]",
                iam_role_arn="arn:aws:iam::321669910225:role/z",
                name="x",
            )

    @parametrize
    def test_method_retrieve(self, client: M3ter) -> None:
        destination = client.data_exports.destinations.retrieve(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(DestinationRetrieveResponse, destination, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: M3ter) -> None:
        response = client.data_exports.destinations.with_raw_response.retrieve(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = response.parse()
        assert_matches_type(DestinationRetrieveResponse, destination, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: M3ter) -> None:
        with client.data_exports.destinations.with_streaming_response.retrieve(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = response.parse()
            assert_matches_type(DestinationRetrieveResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.data_exports.destinations.with_raw_response.retrieve(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.data_exports.destinations.with_raw_response.retrieve(
                id="",
                org_id="orgId",
            )

    @parametrize
    def test_method_update(self, client: M3ter) -> None:
        destination = client.data_exports.destinations.update(
            id="id",
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        )
        assert_matches_type(DestinationUpdateResponse, destination, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: M3ter) -> None:
        destination = client.data_exports.destinations.update(
            id="id",
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
            partition_order="TYPE_FIRST",
            prefix="prefix",
            version=0,
        )
        assert_matches_type(DestinationUpdateResponse, destination, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: M3ter) -> None:
        response = client.data_exports.destinations.with_raw_response.update(
            id="id",
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = response.parse()
        assert_matches_type(DestinationUpdateResponse, destination, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: M3ter) -> None:
        with client.data_exports.destinations.with_streaming_response.update(
            id="id",
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = response.parse()
            assert_matches_type(DestinationUpdateResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.data_exports.destinations.with_raw_response.update(
                id="id",
                org_id="",
                bucket_name="xxx",
                code="JS!?Q0]r] ]$]",
                iam_role_arn="arn:aws:iam::321669910225:role/z",
                name="x",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.data_exports.destinations.with_raw_response.update(
                id="",
                org_id="orgId",
                bucket_name="xxx",
                code="JS!?Q0]r] ]$]",
                iam_role_arn="arn:aws:iam::321669910225:role/z",
                name="x",
            )

    @parametrize
    def test_method_list(self, client: M3ter) -> None:
        destination = client.data_exports.destinations.list(
            org_id="orgId",
        )
        assert_matches_type(SyncCursor[DataExportDestinationResponse], destination, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: M3ter) -> None:
        destination = client.data_exports.destinations.list(
            org_id="orgId",
            ids=["string"],
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(SyncCursor[DataExportDestinationResponse], destination, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: M3ter) -> None:
        response = client.data_exports.destinations.with_raw_response.list(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = response.parse()
        assert_matches_type(SyncCursor[DataExportDestinationResponse], destination, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: M3ter) -> None:
        with client.data_exports.destinations.with_streaming_response.list(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = response.parse()
            assert_matches_type(SyncCursor[DataExportDestinationResponse], destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.data_exports.destinations.with_raw_response.list(
                org_id="",
            )

    @parametrize
    def test_method_delete(self, client: M3ter) -> None:
        destination = client.data_exports.destinations.delete(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(DestinationDeleteResponse, destination, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: M3ter) -> None:
        response = client.data_exports.destinations.with_raw_response.delete(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = response.parse()
        assert_matches_type(DestinationDeleteResponse, destination, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: M3ter) -> None:
        with client.data_exports.destinations.with_streaming_response.delete(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = response.parse()
            assert_matches_type(DestinationDeleteResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.data_exports.destinations.with_raw_response.delete(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.data_exports.destinations.with_raw_response.delete(
                id="",
                org_id="orgId",
            )


class TestAsyncDestinations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncM3ter) -> None:
        destination = await async_client.data_exports.destinations.create(
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        )
        assert_matches_type(DestinationCreateResponse, destination, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncM3ter) -> None:
        destination = await async_client.data_exports.destinations.create(
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
            partition_order="TYPE_FIRST",
            prefix="prefix",
            version=0,
        )
        assert_matches_type(DestinationCreateResponse, destination, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncM3ter) -> None:
        response = await async_client.data_exports.destinations.with_raw_response.create(
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = await response.parse()
        assert_matches_type(DestinationCreateResponse, destination, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncM3ter) -> None:
        async with async_client.data_exports.destinations.with_streaming_response.create(
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = await response.parse()
            assert_matches_type(DestinationCreateResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.data_exports.destinations.with_raw_response.create(
                org_id="",
                bucket_name="xxx",
                code="JS!?Q0]r] ]$]",
                iam_role_arn="arn:aws:iam::321669910225:role/z",
                name="x",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncM3ter) -> None:
        destination = await async_client.data_exports.destinations.retrieve(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(DestinationRetrieveResponse, destination, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncM3ter) -> None:
        response = await async_client.data_exports.destinations.with_raw_response.retrieve(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = await response.parse()
        assert_matches_type(DestinationRetrieveResponse, destination, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncM3ter) -> None:
        async with async_client.data_exports.destinations.with_streaming_response.retrieve(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = await response.parse()
            assert_matches_type(DestinationRetrieveResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.data_exports.destinations.with_raw_response.retrieve(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.data_exports.destinations.with_raw_response.retrieve(
                id="",
                org_id="orgId",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncM3ter) -> None:
        destination = await async_client.data_exports.destinations.update(
            id="id",
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        )
        assert_matches_type(DestinationUpdateResponse, destination, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncM3ter) -> None:
        destination = await async_client.data_exports.destinations.update(
            id="id",
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
            partition_order="TYPE_FIRST",
            prefix="prefix",
            version=0,
        )
        assert_matches_type(DestinationUpdateResponse, destination, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncM3ter) -> None:
        response = await async_client.data_exports.destinations.with_raw_response.update(
            id="id",
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = await response.parse()
        assert_matches_type(DestinationUpdateResponse, destination, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncM3ter) -> None:
        async with async_client.data_exports.destinations.with_streaming_response.update(
            id="id",
            org_id="orgId",
            bucket_name="xxx",
            code="JS!?Q0]r] ]$]",
            iam_role_arn="arn:aws:iam::321669910225:role/z",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = await response.parse()
            assert_matches_type(DestinationUpdateResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.data_exports.destinations.with_raw_response.update(
                id="id",
                org_id="",
                bucket_name="xxx",
                code="JS!?Q0]r] ]$]",
                iam_role_arn="arn:aws:iam::321669910225:role/z",
                name="x",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.data_exports.destinations.with_raw_response.update(
                id="",
                org_id="orgId",
                bucket_name="xxx",
                code="JS!?Q0]r] ]$]",
                iam_role_arn="arn:aws:iam::321669910225:role/z",
                name="x",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncM3ter) -> None:
        destination = await async_client.data_exports.destinations.list(
            org_id="orgId",
        )
        assert_matches_type(AsyncCursor[DataExportDestinationResponse], destination, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncM3ter) -> None:
        destination = await async_client.data_exports.destinations.list(
            org_id="orgId",
            ids=["string"],
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(AsyncCursor[DataExportDestinationResponse], destination, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncM3ter) -> None:
        response = await async_client.data_exports.destinations.with_raw_response.list(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = await response.parse()
        assert_matches_type(AsyncCursor[DataExportDestinationResponse], destination, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncM3ter) -> None:
        async with async_client.data_exports.destinations.with_streaming_response.list(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = await response.parse()
            assert_matches_type(AsyncCursor[DataExportDestinationResponse], destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.data_exports.destinations.with_raw_response.list(
                org_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncM3ter) -> None:
        destination = await async_client.data_exports.destinations.delete(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(DestinationDeleteResponse, destination, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncM3ter) -> None:
        response = await async_client.data_exports.destinations.with_raw_response.delete(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        destination = await response.parse()
        assert_matches_type(DestinationDeleteResponse, destination, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncM3ter) -> None:
        async with async_client.data_exports.destinations.with_streaming_response.delete(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            destination = await response.parse()
            assert_matches_type(DestinationDeleteResponse, destination, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.data_exports.destinations.with_raw_response.delete(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.data_exports.destinations.with_raw_response.delete(
                id="",
                org_id="orgId",
            )
