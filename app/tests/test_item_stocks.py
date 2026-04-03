from unittest.mock import AsyncMock

import pytest
from routers import item_stocks


@pytest.mark.asyncio
async def test_read_items(client, monkeypatch):
    mocked_response = [
        {
            "id": 1,
            "price": 100,
            "quantity": 1,
            "available_quantity": 1,
            "item_id": 1,
        },
    ]

    monkeypatch.setattr(
        item_stocks, "get_item_stocks", AsyncMock(return_value=mocked_response)
    )

    response = await client.get(
        f"api/item_stocks/?item_id={mocked_response[0]['item_id']}"
    )

    assert response.status_code == 200
    assert response.json() == mocked_response


@pytest.mark.asyncio
async def test_read_items_empty_list(client, monkeypatch):
    mocked_response = []

    monkeypatch.setattr(
        item_stocks, "get_item_stocks", AsyncMock(return_value=mocked_response)
    )

    response = await client.get("api/item_stocks/?item_id=0")

    assert response.status_code == 200
    assert response.json() == mocked_response
