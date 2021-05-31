from urllib.parse import urlencode

def test_get_statistics_year(client):   
    json = {"partner": "DLMF"}
    param = urlencode(json)
    response = client.get(f"/links_api/statistics/years/?{param}")
    data = response.json
    assert len(data[0]) == 2

