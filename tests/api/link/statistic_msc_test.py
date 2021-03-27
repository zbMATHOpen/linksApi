def test_get_display_all(client):
    response = client.get("/links_api/statistics/msc/")
    data = response.json
    assert data == [["33", 1]]
