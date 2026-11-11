import pytest
from pytest_mock import MockerFixture

from polar.integrations.tinybird.client import TinybirdClient


def _client_without_tokens() -> TinybirdClient:
    return TinybirdClient(
        api_url="http://127.0.0.1:1",
        clickhouse_url="http://127.0.0.1:1",
        api_token=None,
        read_token=None,
        clickhouse_username="default",
        clickhouse_token=None,
    )


@pytest.mark.anyio
class TestClientWithoutTokens:
    async def test_query_returns_no_rows_without_connecting(
        self, mocker: MockerFixture
    ) -> None:
        client = _client_without_tokens()
        get_client = mocker.patch.object(client, "_get_clickhouse_client")

        rows = await client.query("SELECT 1", db_statement="SELECT 1")

        assert rows == []
        get_client.assert_not_called()

    async def test_delete_succeeds(self) -> None:
        client = _client_without_tokens()

        assert await client.delete("events_by_ingested_at", "1 = 1") == {}
