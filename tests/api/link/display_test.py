def test_get_display_all(client):
    response = client.get("/links_api/link/")
    data = response.json
    assert len(data) > 0
    entry: dict = data[0]
    assert len(entry.keys()) == 5
    src: dict = entry.get("Source")
    assert len(src) == 4
