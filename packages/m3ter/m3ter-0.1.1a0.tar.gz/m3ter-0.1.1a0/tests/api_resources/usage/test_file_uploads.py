# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from m3ter import M3ter, AsyncM3ter
from tests.utils import assert_matches_type
from m3ter.types.usage import FileUploadGenerateUploadURLResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFileUploads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_generate_upload_url(self, client: M3ter) -> None:
        file_upload = client.usage.file_uploads.generate_upload_url(
            org_id="orgId",
            content_type="x",
            file_name="x",
        )
        assert_matches_type(FileUploadGenerateUploadURLResponse, file_upload, path=["response"])

    @parametrize
    def test_method_generate_upload_url_with_all_params(self, client: M3ter) -> None:
        file_upload = client.usage.file_uploads.generate_upload_url(
            org_id="orgId",
            content_type="x",
            file_name="x",
            content_length=1,
        )
        assert_matches_type(FileUploadGenerateUploadURLResponse, file_upload, path=["response"])

    @parametrize
    def test_raw_response_generate_upload_url(self, client: M3ter) -> None:
        response = client.usage.file_uploads.with_raw_response.generate_upload_url(
            org_id="orgId",
            content_type="x",
            file_name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file_upload = response.parse()
        assert_matches_type(FileUploadGenerateUploadURLResponse, file_upload, path=["response"])

    @parametrize
    def test_streaming_response_generate_upload_url(self, client: M3ter) -> None:
        with client.usage.file_uploads.with_streaming_response.generate_upload_url(
            org_id="orgId",
            content_type="x",
            file_name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file_upload = response.parse()
            assert_matches_type(FileUploadGenerateUploadURLResponse, file_upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_generate_upload_url(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.usage.file_uploads.with_raw_response.generate_upload_url(
                org_id="",
                content_type="x",
                file_name="x",
            )


class TestAsyncFileUploads:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_generate_upload_url(self, async_client: AsyncM3ter) -> None:
        file_upload = await async_client.usage.file_uploads.generate_upload_url(
            org_id="orgId",
            content_type="x",
            file_name="x",
        )
        assert_matches_type(FileUploadGenerateUploadURLResponse, file_upload, path=["response"])

    @parametrize
    async def test_method_generate_upload_url_with_all_params(self, async_client: AsyncM3ter) -> None:
        file_upload = await async_client.usage.file_uploads.generate_upload_url(
            org_id="orgId",
            content_type="x",
            file_name="x",
            content_length=1,
        )
        assert_matches_type(FileUploadGenerateUploadURLResponse, file_upload, path=["response"])

    @parametrize
    async def test_raw_response_generate_upload_url(self, async_client: AsyncM3ter) -> None:
        response = await async_client.usage.file_uploads.with_raw_response.generate_upload_url(
            org_id="orgId",
            content_type="x",
            file_name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file_upload = await response.parse()
        assert_matches_type(FileUploadGenerateUploadURLResponse, file_upload, path=["response"])

    @parametrize
    async def test_streaming_response_generate_upload_url(self, async_client: AsyncM3ter) -> None:
        async with async_client.usage.file_uploads.with_streaming_response.generate_upload_url(
            org_id="orgId",
            content_type="x",
            file_name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file_upload = await response.parse()
            assert_matches_type(FileUploadGenerateUploadURLResponse, file_upload, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_generate_upload_url(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.usage.file_uploads.with_raw_response.generate_upload_url(
                org_id="",
                content_type="x",
                file_name="x",
            )
