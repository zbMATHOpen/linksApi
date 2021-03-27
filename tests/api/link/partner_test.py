import os
from urllib.parse import urlencode

import pytest


def test_get_partner(client):
    response = client.get("/links_api/partner/")
    data = response.json
    assert len(data) == 1
    entry: dict = data[0]
    assert len(entry.keys()) == 4
    url: dict = entry.get("url")
    assert "https" in url


# potentially destructive test
def test_put_partner(client):
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    test_name = "Test"
    json = {"partner id": 1, "partner name": test_name}
    param = urlencode(json)
    response = client.put(f"/links_api/partner/?{param}",
                          headers=headers,
                          )
    data = response.json
    assert response.status_code == 200
    assert data is None
    response = client.get("/links_api/partner/")
    data = response.json
    name: dict = data[0].get("name")
    assert test_name == name


@pytest.mark.skip(reason="currently json input is not supported")
def test_put_partner_via_json(client):
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    json = {"partner_id": 1, "partner_name": "Test name"}
    response = client.put(f"/links_api/partner/",
                          headers=headers,
                          json=json
                          )
    data = response.json
    assert data is None
