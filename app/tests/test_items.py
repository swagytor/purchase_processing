from unittest.mock import AsyncMock

import pytest

from routers import items


@pytest.mark.asyncio
async def test_read_items(client, monkeypatch):
    mocked_response = [{"id": 1, "title": "Тестовый продукт"}]

    monkeypatch.setattr(
        items, "get_items", AsyncMock(return_value=mocked_response)
    )

    response = await client.get("api/items/")

    assert response.status_code == 200
    assert response.json() == mocked_response


@pytest.mark.asyncio
async def test_read_item(client, monkeypatch):
    mocked_response = {
        "id": 1,
        "title": "Тестовый продукт",
        "description": "Тестовое описание",
        "stocks": [],
    }

    monkeypatch.setattr(
        items, "get_item_by_id", AsyncMock(return_value=mocked_response)
    )

    response = await client.get(f"api/items/{mocked_response['id']}/")

    assert response.status_code == 200
    assert response.json() == mocked_response
