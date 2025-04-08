# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from m3ter import M3ter, AsyncM3ter
from m3ter.types import (
    AccountResponse,
    AccountSearchResponse,
    AccountEndDateBillingEntitiesResponse,
)
from tests.utils import assert_matches_type
from m3ter._utils import parse_date, parse_datetime
from m3ter.pagination import SyncCursor, AsyncCursor

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAccounts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: M3ter) -> None:
        account = client.accounts.create(
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: M3ter) -> None:
        account = client.accounts.create(
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
            address={
                "address_line1": "addressLine1",
                "address_line2": "addressLine2",
                "address_line3": "addressLine3",
                "address_line4": "addressLine4",
                "country": "country",
                "locality": "locality",
                "post_code": "postCode",
                "region": "region",
            },
            auto_generate_statement_mode="NONE",
            bill_epoch=parse_date("2019-12-27"),
            config_data={"foo": "bar"},
            credit_application_order=["PREPAYMENT"],
            currency="USD",
            custom_fields={"foo": "string"},
            days_before_bill_due=1,
            parent_account_id="parentAccountId",
            purchase_order_number="purchaseOrderNumber",
            statement_definition_id="statementDefinitionId",
            version=0,
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: M3ter) -> None:
        response = client.accounts.with_raw_response.create(
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: M3ter) -> None:
        with client.accounts.with_streaming_response.create(
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.accounts.with_raw_response.create(
                org_id="",
                code="JS!?Q0]r] ]$]",
                email_address="dev@stainless.com",
                name="x",
            )

    @parametrize
    def test_method_retrieve(self, client: M3ter) -> None:
        account = client.accounts.retrieve(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: M3ter) -> None:
        response = client.accounts.with_raw_response.retrieve(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: M3ter) -> None:
        with client.accounts.with_streaming_response.retrieve(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.accounts.with_raw_response.retrieve(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.accounts.with_raw_response.retrieve(
                id="",
                org_id="orgId",
            )

    @parametrize
    def test_method_update(self, client: M3ter) -> None:
        account = client.accounts.update(
            id="id",
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: M3ter) -> None:
        account = client.accounts.update(
            id="id",
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
            address={
                "address_line1": "addressLine1",
                "address_line2": "addressLine2",
                "address_line3": "addressLine3",
                "address_line4": "addressLine4",
                "country": "country",
                "locality": "locality",
                "post_code": "postCode",
                "region": "region",
            },
            auto_generate_statement_mode="NONE",
            bill_epoch=parse_date("2019-12-27"),
            config_data={"foo": "bar"},
            credit_application_order=["PREPAYMENT"],
            currency="USD",
            custom_fields={"foo": "string"},
            days_before_bill_due=1,
            parent_account_id="parentAccountId",
            purchase_order_number="purchaseOrderNumber",
            statement_definition_id="statementDefinitionId",
            version=0,
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: M3ter) -> None:
        response = client.accounts.with_raw_response.update(
            id="id",
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: M3ter) -> None:
        with client.accounts.with_streaming_response.update(
            id="id",
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.accounts.with_raw_response.update(
                id="id",
                org_id="",
                code="JS!?Q0]r] ]$]",
                email_address="dev@stainless.com",
                name="x",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.accounts.with_raw_response.update(
                id="",
                org_id="orgId",
                code="JS!?Q0]r] ]$]",
                email_address="dev@stainless.com",
                name="x",
            )

    @parametrize
    def test_method_list(self, client: M3ter) -> None:
        account = client.accounts.list(
            org_id="orgId",
        )
        assert_matches_type(SyncCursor[AccountResponse], account, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: M3ter) -> None:
        account = client.accounts.list(
            org_id="orgId",
            codes=["string"],
            ids=["string"],
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(SyncCursor[AccountResponse], account, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: M3ter) -> None:
        response = client.accounts.with_raw_response.list(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(SyncCursor[AccountResponse], account, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: M3ter) -> None:
        with client.accounts.with_streaming_response.list(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(SyncCursor[AccountResponse], account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.accounts.with_raw_response.list(
                org_id="",
            )

    @parametrize
    def test_method_delete(self, client: M3ter) -> None:
        account = client.accounts.delete(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: M3ter) -> None:
        response = client.accounts.with_raw_response.delete(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: M3ter) -> None:
        with client.accounts.with_streaming_response.delete(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.accounts.with_raw_response.delete(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.accounts.with_raw_response.delete(
                id="",
                org_id="orgId",
            )

    @parametrize
    def test_method_end_date_billing_entities(self, client: M3ter) -> None:
        account = client.accounts.end_date_billing_entities(
            id="id",
            org_id="orgId",
            billing_entities=["CONTRACT"],
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(AccountEndDateBillingEntitiesResponse, account, path=["response"])

    @parametrize
    def test_method_end_date_billing_entities_with_all_params(self, client: M3ter) -> None:
        account = client.accounts.end_date_billing_entities(
            id="id",
            org_id="orgId",
            billing_entities=["CONTRACT"],
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            apply_to_children=True,
        )
        assert_matches_type(AccountEndDateBillingEntitiesResponse, account, path=["response"])

    @parametrize
    def test_raw_response_end_date_billing_entities(self, client: M3ter) -> None:
        response = client.accounts.with_raw_response.end_date_billing_entities(
            id="id",
            org_id="orgId",
            billing_entities=["CONTRACT"],
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountEndDateBillingEntitiesResponse, account, path=["response"])

    @parametrize
    def test_streaming_response_end_date_billing_entities(self, client: M3ter) -> None:
        with client.accounts.with_streaming_response.end_date_billing_entities(
            id="id",
            org_id="orgId",
            billing_entities=["CONTRACT"],
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountEndDateBillingEntitiesResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_end_date_billing_entities(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.accounts.with_raw_response.end_date_billing_entities(
                id="id",
                org_id="",
                billing_entities=["CONTRACT"],
                end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.accounts.with_raw_response.end_date_billing_entities(
                id="",
                org_id="orgId",
                billing_entities=["CONTRACT"],
                end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

    @parametrize
    def test_method_get_children(self, client: M3ter) -> None:
        account = client.accounts.get_children(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_method_get_children_with_all_params(self, client: M3ter) -> None:
        account = client.accounts.get_children(
            id="id",
            org_id="orgId",
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_raw_response_get_children(self, client: M3ter) -> None:
        response = client.accounts.with_raw_response.get_children(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    def test_streaming_response_get_children(self, client: M3ter) -> None:
        with client.accounts.with_streaming_response.get_children(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get_children(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.accounts.with_raw_response.get_children(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.accounts.with_raw_response.get_children(
                id="",
                org_id="orgId",
            )

    @parametrize
    def test_method_search(self, client: M3ter) -> None:
        account = client.accounts.search(
            org_id="orgId",
        )
        assert_matches_type(AccountSearchResponse, account, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: M3ter) -> None:
        account = client.accounts.search(
            org_id="orgId",
            from_document=0,
            operator="AND",
            page_size=1,
            search_query="searchQuery",
            sort_by="sortBy",
            sort_order="ASC",
        )
        assert_matches_type(AccountSearchResponse, account, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: M3ter) -> None:
        response = client.accounts.with_raw_response.search(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountSearchResponse, account, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: M3ter) -> None:
        with client.accounts.with_streaming_response.search(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountSearchResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_search(self, client: M3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.accounts.with_raw_response.search(
                org_id="",
            )


class TestAsyncAccounts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.create(
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.create(
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
            address={
                "address_line1": "addressLine1",
                "address_line2": "addressLine2",
                "address_line3": "addressLine3",
                "address_line4": "addressLine4",
                "country": "country",
                "locality": "locality",
                "post_code": "postCode",
                "region": "region",
            },
            auto_generate_statement_mode="NONE",
            bill_epoch=parse_date("2019-12-27"),
            config_data={"foo": "bar"},
            credit_application_order=["PREPAYMENT"],
            currency="USD",
            custom_fields={"foo": "string"},
            days_before_bill_due=1,
            parent_account_id="parentAccountId",
            purchase_order_number="purchaseOrderNumber",
            statement_definition_id="statementDefinitionId",
            version=0,
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncM3ter) -> None:
        response = await async_client.accounts.with_raw_response.create(
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncM3ter) -> None:
        async with async_client.accounts.with_streaming_response.create(
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.accounts.with_raw_response.create(
                org_id="",
                code="JS!?Q0]r] ]$]",
                email_address="dev@stainless.com",
                name="x",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.retrieve(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncM3ter) -> None:
        response = await async_client.accounts.with_raw_response.retrieve(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncM3ter) -> None:
        async with async_client.accounts.with_streaming_response.retrieve(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.accounts.with_raw_response.retrieve(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.accounts.with_raw_response.retrieve(
                id="",
                org_id="orgId",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.update(
            id="id",
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.update(
            id="id",
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
            address={
                "address_line1": "addressLine1",
                "address_line2": "addressLine2",
                "address_line3": "addressLine3",
                "address_line4": "addressLine4",
                "country": "country",
                "locality": "locality",
                "post_code": "postCode",
                "region": "region",
            },
            auto_generate_statement_mode="NONE",
            bill_epoch=parse_date("2019-12-27"),
            config_data={"foo": "bar"},
            credit_application_order=["PREPAYMENT"],
            currency="USD",
            custom_fields={"foo": "string"},
            days_before_bill_due=1,
            parent_account_id="parentAccountId",
            purchase_order_number="purchaseOrderNumber",
            statement_definition_id="statementDefinitionId",
            version=0,
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncM3ter) -> None:
        response = await async_client.accounts.with_raw_response.update(
            id="id",
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncM3ter) -> None:
        async with async_client.accounts.with_streaming_response.update(
            id="id",
            org_id="orgId",
            code="JS!?Q0]r] ]$]",
            email_address="dev@stainless.com",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.accounts.with_raw_response.update(
                id="id",
                org_id="",
                code="JS!?Q0]r] ]$]",
                email_address="dev@stainless.com",
                name="x",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.accounts.with_raw_response.update(
                id="",
                org_id="orgId",
                code="JS!?Q0]r] ]$]",
                email_address="dev@stainless.com",
                name="x",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.list(
            org_id="orgId",
        )
        assert_matches_type(AsyncCursor[AccountResponse], account, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.list(
            org_id="orgId",
            codes=["string"],
            ids=["string"],
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(AsyncCursor[AccountResponse], account, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncM3ter) -> None:
        response = await async_client.accounts.with_raw_response.list(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AsyncCursor[AccountResponse], account, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncM3ter) -> None:
        async with async_client.accounts.with_streaming_response.list(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AsyncCursor[AccountResponse], account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.accounts.with_raw_response.list(
                org_id="",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.delete(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncM3ter) -> None:
        response = await async_client.accounts.with_raw_response.delete(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncM3ter) -> None:
        async with async_client.accounts.with_streaming_response.delete(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.accounts.with_raw_response.delete(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.accounts.with_raw_response.delete(
                id="",
                org_id="orgId",
            )

    @parametrize
    async def test_method_end_date_billing_entities(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.end_date_billing_entities(
            id="id",
            org_id="orgId",
            billing_entities=["CONTRACT"],
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(AccountEndDateBillingEntitiesResponse, account, path=["response"])

    @parametrize
    async def test_method_end_date_billing_entities_with_all_params(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.end_date_billing_entities(
            id="id",
            org_id="orgId",
            billing_entities=["CONTRACT"],
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            apply_to_children=True,
        )
        assert_matches_type(AccountEndDateBillingEntitiesResponse, account, path=["response"])

    @parametrize
    async def test_raw_response_end_date_billing_entities(self, async_client: AsyncM3ter) -> None:
        response = await async_client.accounts.with_raw_response.end_date_billing_entities(
            id="id",
            org_id="orgId",
            billing_entities=["CONTRACT"],
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountEndDateBillingEntitiesResponse, account, path=["response"])

    @parametrize
    async def test_streaming_response_end_date_billing_entities(self, async_client: AsyncM3ter) -> None:
        async with async_client.accounts.with_streaming_response.end_date_billing_entities(
            id="id",
            org_id="orgId",
            billing_entities=["CONTRACT"],
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountEndDateBillingEntitiesResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_end_date_billing_entities(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.accounts.with_raw_response.end_date_billing_entities(
                id="id",
                org_id="",
                billing_entities=["CONTRACT"],
                end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.accounts.with_raw_response.end_date_billing_entities(
                id="",
                org_id="orgId",
                billing_entities=["CONTRACT"],
                end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

    @parametrize
    async def test_method_get_children(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.get_children(
            id="id",
            org_id="orgId",
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_method_get_children_with_all_params(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.get_children(
            id="id",
            org_id="orgId",
            next_token="nextToken",
            page_size=1,
        )
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_raw_response_get_children(self, async_client: AsyncM3ter) -> None:
        response = await async_client.accounts.with_raw_response.get_children(
            id="id",
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountResponse, account, path=["response"])

    @parametrize
    async def test_streaming_response_get_children(self, async_client: AsyncM3ter) -> None:
        async with async_client.accounts.with_streaming_response.get_children(
            id="id",
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get_children(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.accounts.with_raw_response.get_children(
                id="id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.accounts.with_raw_response.get_children(
                id="",
                org_id="orgId",
            )

    @parametrize
    async def test_method_search(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.search(
            org_id="orgId",
        )
        assert_matches_type(AccountSearchResponse, account, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncM3ter) -> None:
        account = await async_client.accounts.search(
            org_id="orgId",
            from_document=0,
            operator="AND",
            page_size=1,
            search_query="searchQuery",
            sort_by="sortBy",
            sort_order="ASC",
        )
        assert_matches_type(AccountSearchResponse, account, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncM3ter) -> None:
        response = await async_client.accounts.with_raw_response.search(
            org_id="orgId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountSearchResponse, account, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncM3ter) -> None:
        async with async_client.accounts.with_streaming_response.search(
            org_id="orgId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountSearchResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_search(self, async_client: AsyncM3ter) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.accounts.with_raw_response.search(
                org_id="",
            )
