from urllib.parse import urlencode
import os

from zb_links.db.models import Link, db


def test_get_link_item(client):
    test_id = "11.14#I1.i1.p1"
    json = {"DE number": 3273551,
            "external id": test_id,
            "partner": "DLMF"}
    param = urlencode(json)
    response = client.get(f"/links_api/link/item/?{param}")
    assert 200 == response.status_code
    data = response.json
    assert data["Source"]["Identifier"]["ID"] == test_id


def test_get_link_msc(client):
    json = {"MSC code": "33-00"}
    param = urlencode(json)
    response = client.get(f"/links_api/link/?{param}")
    data = response.json
    assert len(data) > 0
    assert not data[0]["RelationshipType"]


def test_post_link(client):
    document = 2062129
    external_id = "11.14#I1.i1.p1"
    partner_name = "DLMF"

    link_query = Link.query.filter_by(document=document,
                                      external_id=external_id,
                                      type=partner_name,
                                      )
    link_to_add = link_query.all()

    assert len(link_to_add) == 0, "test link to create is not unique"

    json = {"DE number": document,
            "external id": external_id,
            "partner": partner_name}
    param = urlencode(json)
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    response = client.post(f"/links_api/link/item/?{param}",
                          headers=headers,
                          )
    assert response.status_code == 201

    data = response.json
    assert data is None

    response = client.get(f"/links_api/link/item/?{param}")
    data = response.json
    source: dict = data.get("Source")
    assert source["Identifier"]["ID"] == external_id

    # delete test entry
    link_query = Link.query.filter_by(document=document,
                                      external_id=external_id,
                                      type=partner_name,
                                      )
    link_query.delete()

    db.session.commit()


def test_post_link_with_bad_zbl(client):
    zbl_id = '2062.129'
    external_id = "11.14#I1.i1.p1"
    partner_name = "DLMF"

    json = {"DE number": zbl_id,
            "external id": external_id,
            "partner": partner_name}
    param = urlencode(json)
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    response = client.post(f"/links_api/link/item/?{param}",
                          headers=headers,
                          )
    assert response.status_code == 422

    data = response.json
    assert data.get("message")
