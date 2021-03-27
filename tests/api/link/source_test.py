def test_source(client):
    response = client.get("/links_api/source/")
    data = response.json
    assert len(data) == 1
    assert "https" in data[0]

