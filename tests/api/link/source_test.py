from urllib.parse import urlencode

def test_source(client):
    json = {"partner": "DLMF"}
    param = urlencode(json)
    response = client.get(f"/links_api/source/?{param}")
    data = response.json
    assert len(data) > 0
    assert "https" in data[0]

