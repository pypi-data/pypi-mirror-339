# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from m3ter import M3ter, AsyncM3ter
from m3ter.types import (
    UserResponse,
    UserMeResponse,
    ResourceGroupResponse,
    PermissionPolicyResponse,
)
from tests.utils import assert_matches_type
from m3ter._utils import parse_datetime
from m3ter.pagination import SyncCursor, AsyncCursor

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: M3ter) -> None:
        user = client.users.retrieve(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: M3ter) -> None:
        response = client.users.with_raw_response.retrieve(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: M3ter) -> None:
        with client.users.with_streaming_response.retrieve(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.users.with_raw_response.retrieve(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.users.with_raw_response.retrieve(
                id="",
                org_id="orgId",
            )

    @parametrize
    def test_method_update(self, client: M3ter) -> None:
        user = client.users.update(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: M3ter) -> None:
        user = client.users.update(
            id="id",
            org_id="orgId",
            dt_end_access=parse_datetime("2019-12-27T18:11:19.117Z"),
            permission_policy=[
                {
                    "action": ["ALL"],
                    "effect": "ALLOW",
                    "resource": ["string"],
                }
            ],
            version=0,
        )
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: M3ter) -> None:
        response = client.users.with_raw_response.update(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: M3ter) -> None:
        with client.users.with_streaming_response.update(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.users.with_raw_response.update(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.users.with_raw_response.update(
                id="",
                org_id="orgId",
            )

    @parametrize
    def test_method_list(self, client: M3ter) -> None:
        user = client.users.list(
            org_id="orgId",
        )
        assert_matches_type(SyncCursor[UserResponse], user, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: M3ter) -> None:
        user = client.users.list(
            org_id="orgId",
            ids=["string"],
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(SyncCursor[UserResponse], user, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: M3ter) -> None:
        response = client.users.with_raw_response.list(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(SyncCursor[UserResponse], user, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: M3ter) -> None:
        with client.users.with_streaming_response.list(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(SyncCursor[UserResponse], user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.users.with_raw_response.list(
                org_id="",
            )

    @parametrize
    def test_method_get_permissions(self, client: M3ter) -> None:
        user = client.users.get_permissions(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(PermissionPolicyResponse, user, path=["response"])

    @parametrize
    def test_method_get_permissions_with_all_params(self, client: M3ter) -> None:
        user = client.users.get_permissions(
            id="id",
            org_id="orgId",
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(PermissionPolicyResponse, user, path=["response"])

    @parametrize
    def test_raw_response_get_permissions(self, client: M3ter) -> None:
        response = client.users.with_raw_response.get_permissions(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(PermissionPolicyResponse, user, path=["response"])

    @parametrize
    def test_streaming_response_get_permissions(self, client: M3ter) -> None:
        with client.users.with_streaming_response.get_permissions(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(PermissionPolicyResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get_permissions(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.users.with_raw_response.get_permissions(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.users.with_raw_response.get_permissions(
                id="",
                org_id="orgId",
            )

    @parametrize
    def test_method_get_user_groups(self, client: M3ter) -> None:
        user = client.users.get_user_groups(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(ResourceGroupResponse, user, path=["response"])

    @parametrize
    def test_method_get_user_groups_with_all_params(self, client: M3ter) -> None:
        user = client.users.get_user_groups(
            id="id",
            org_id="orgId",
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(ResourceGroupResponse, user, path=["response"])

    @parametrize
    def test_raw_response_get_user_groups(self, client: M3ter) -> None:
        response = client.users.with_raw_response.get_user_groups(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(ResourceGroupResponse, user, path=["response"])

    @parametrize
    def test_streaming_response_get_user_groups(self, client: M3ter) -> None:
        with client.users.with_streaming_response.get_user_groups(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(ResourceGroupResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get_user_groups(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.users.with_raw_response.get_user_groups(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.users.with_raw_response.get_user_groups(
                id="",
                org_id="orgId",
            )

    @parametrize
    def test_method_me(self, client: M3ter) -> None:
        user = client.users.me(
            org_id="orgId",
        )
        assert_matches_type(UserMeResponse, user, path=["response"])

    @parametrize
    def test_raw_response_me(self, client: M3ter) -> None:
        response = client.users.with_raw_response.me(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserMeResponse, user, path=["response"])

    @parametrize
    def test_streaming_response_me(self, client: M3ter) -> None:
        with client.users.with_streaming_response.me(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserMeResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_me(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.users.with_raw_response.me(
                org_id="",
            )

    @parametrize
    def test_method_resend_password(self, client: M3ter) -> None:
        user = client.users.resend_password(
            id="id",
            org_id="orgId",
        )
        assert user is None

    @parametrize
    def test_raw_response_resend_password(self, client: M3ter) -> None:
        response = client.users.with_raw_response.resend_password(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert user is None

    @parametrize
    def test_streaming_response_resend_password(self, client: M3ter) -> None:
        with client.users.with_streaming_response.resend_password(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert user is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_resend_password(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.users.with_raw_response.resend_password(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.users.with_raw_response.resend_password(
                id="",
                org_id="orgId",
            )


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.retrieve(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncM3ter) -> None:
        response = await async_client.users.with_raw_response.retrieve(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncM3ter) -> None:
        async with async_client.users.with_streaming_response.retrieve(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.users.with_raw_response.retrieve(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.users.with_raw_response.retrieve(
                id="",
                org_id="orgId",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.update(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.update(
            id="id",
            org_id="orgId",
            dt_end_access=parse_datetime("2019-12-27T18:11:19.117Z"),
            permission_policy=[
                {
                    "action": ["ALL"],
                    "effect": "ALLOW",
                    "resource": ["string"],
                }
            ],
            version=0,
        )
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncM3ter) -> None:
        response = await async_client.users.with_raw_response.update(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserResponse, user, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncM3ter) -> None:
        async with async_client.users.with_streaming_response.update(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.users.with_raw_response.update(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.users.with_raw_response.update(
                id="",
                org_id="orgId",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.list(
            org_id="orgId",
        )
        assert_matches_type(AsyncCursor[UserResponse], user, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.list(
            org_id="orgId",
            ids=["string"],
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(AsyncCursor[UserResponse], user, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncM3ter) -> None:
        response = await async_client.users.with_raw_response.list(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(AsyncCursor[UserResponse], user, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncM3ter) -> None:
        async with async_client.users.with_streaming_response.list(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(AsyncCursor[UserResponse], user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.users.with_raw_response.list(
                org_id="",
            )

    @parametrize
    async def test_method_get_permissions(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.get_permissions(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(PermissionPolicyResponse, user, path=["response"])

    @parametrize
    async def test_method_get_permissions_with_all_params(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.get_permissions(
            id="id",
            org_id="orgId",
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(PermissionPolicyResponse, user, path=["response"])

    @parametrize
    async def test_raw_response_get_permissions(self, async_client: AsyncM3ter) -> None:
        response = await async_client.users.with_raw_response.get_permissions(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(PermissionPolicyResponse, user, path=["response"])

    @parametrize
    async def test_streaming_response_get_permissions(self, async_client: AsyncM3ter) -> None:
        async with async_client.users.with_streaming_response.get_permissions(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(PermissionPolicyResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get_permissions(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.users.with_raw_response.get_permissions(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.users.with_raw_response.get_permissions(
                id="",
                org_id="orgId",
            )

    @parametrize
    async def test_method_get_user_groups(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.get_user_groups(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(ResourceGroupResponse, user, path=["response"])

    @parametrize
    async def test_method_get_user_groups_with_all_params(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.get_user_groups(
            id="id",
            org_id="orgId",
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(ResourceGroupResponse, user, path=["response"])

    @parametrize
    async def test_raw_response_get_user_groups(self, async_client: AsyncM3ter) -> None:
        response = await async_client.users.with_raw_response.get_user_groups(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(ResourceGroupResponse, user, path=["response"])

    @parametrize
    async def test_streaming_response_get_user_groups(self, async_client: AsyncM3ter) -> None:
        async with async_client.users.with_streaming_response.get_user_groups(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(ResourceGroupResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get_user_groups(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.users.with_raw_response.get_user_groups(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.users.with_raw_response.get_user_groups(
                id="",
                org_id="orgId",
            )

    @parametrize
    async def test_method_me(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.me(
            org_id="orgId",
        )
        assert_matches_type(UserMeResponse, user, path=["response"])

    @parametrize
    async def test_raw_response_me(self, async_client: AsyncM3ter) -> None:
        response = await async_client.users.with_raw_response.me(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserMeResponse, user, path=["response"])

    @parametrize
    async def test_streaming_response_me(self, async_client: AsyncM3ter) -> None:
        async with async_client.users.with_streaming_response.me(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserMeResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_me(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.users.with_raw_response.me(
                org_id="",
            )

    @parametrize
    async def test_method_resend_password(self, async_client: AsyncM3ter) -> None:
        user = await async_client.users.resend_password(
            id="id",
            org_id="orgId",
        )
        assert user is None

    @parametrize
    async def test_raw_response_resend_password(self, async_client: AsyncM3ter) -> None:
        response = await async_client.users.with_raw_response.resend_password(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert user is None

    @parametrize
    async def test_streaming_response_resend_password(self, async_client: AsyncM3ter) -> None:
        async with async_client.users.with_streaming_response.resend_password(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert user is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_resend_password(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.users.with_raw_response.resend_password(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.users.with_raw_response.resend_password(
                id="",
                org_id="orgId",
            )
