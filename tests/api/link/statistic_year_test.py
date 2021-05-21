def test_get_statistics_year(client):
    response = client.get("/links_api/statistics/years/")
    data = response.json
    assert data == [["1964", 1]]
