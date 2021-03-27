def test_get_statistics_msc(client):
    response = client.get("/links_api/statistics/msc/")
    data = response.json
    assert data == [["33", 1]]
