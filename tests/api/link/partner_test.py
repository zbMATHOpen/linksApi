def test_get_partner(client):
    response = client.get("/links_api/partner/")
    data = response.json
    assert len(data) == 1
    entry: dict = data[0]
    assert len(entry.keys()) == 4
    url: dict = entry.get("url")
    assert "https" in url
