from urllib.parse import urlencode


def test_get_link_item(client):
    test_id = "11.14#I1.i1.p1"
    json = {"zbl code": "0171.38503",
            "source identifier": test_id,
            "partner name": "DLMF"}
    param = urlencode(json)
    response = client.get(f"/links_api/link/item/?{param}")
    assert 200 == response.status_code
    data = response.json
    assert data["Source"]["Identifier"]["ID"] == test_id


def test_get_link_msc(client):
    json = {"msc classification code": "33-00"}
    param = urlencode(json)
    response = client.get(f"/links_api/link/?{param}")
    data = response.json
    assert len(data)==1
    assert "equation" in data[0]["RelationshipType"]
