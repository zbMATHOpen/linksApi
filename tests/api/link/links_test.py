from flask import url_for, request
from urllib.parse import urlencode
import os

from zb_links.api.link.helpers import target_helpers
from zb_links.db.models import Link, Source, db


def test_get_all_links_from_zbl(client):

    json = {"DE_number": "0171.38503"}
    param = urlencode(json)
    response = client.get(f"/links_api/link/?{param}")
    assert 200 == response.status_code
    first_data = response.json[0]
    assert first_data["Source"]["Identifier"]["ID"] == "11.14#I1.i1.p1"


def test_get_all_links_from_de(client):

    json = {"DE_number": "3273551"}
    param = urlencode(json)
    response = client.get(f"/links_api/link/?{param}")
    assert 200 == response.status_code
    first_data = response.json[0]
    assert first_data["Source"]["Identifier"]["ID"] == "11.14#I1.i1.p1"


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


def test_get_link_through_redirect(client):
    de_number = 2062129
    client.get(
        f"/links_api/link/item/{de_number}", follow_redirects=True
    )
    assert request.path == url_for("links_api.link_link_collection")


def test_get_link_item_zbl(client):
    test_id = "11.14#I1.i1.p1"
    json = {"DE number": "0171.38503",
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

    # add here created_by explicitly
    connection = db.engine.connect()
    data_row = """
    UPDATE document_external_ids
    SET created_by = 'api_user'
    WHERE document = '2062129'
    """
    connection.execute(data_row)

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


def test_post_link_with_zbl(client):
    zbl_id = "1234.98765"
    external_id = "11.14#I1.i1.p1"
    partner_name = "DLMF"

    de_val = target_helpers.get_de_from_input(zbl_id)

    link_query = Link.query.filter_by(document=de_val,
                                      external_id=external_id,
                                      type=partner_name,
                                      )
    link_to_add = link_query.all()

    assert len(link_to_add) == 0, "test link to create is not unique"

    json = {"DE number": de_val,
            "external id": external_id,
            "partner": partner_name}
    param = urlencode(json)
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    response = client.post(f"/links_api/link/item/?{param}",
                           headers=headers,
                           )
    assert response.status_code == 201

    # add here created_by explicitly
    connection = db.engine.connect()
    data_row = """
    UPDATE document_external_ids
    SET created_by = 'api_user'
    WHERE document = '2062129'
    """
    connection.execute(data_row)

    data = response.json
    assert data is None

    response = client.get(f"/links_api/link/item/?{param}")
    data = response.json
    source: dict = data.get("Source")
    assert source["Identifier"]["ID"] == external_id

    # delete test entry
    link_query = Link.query.filter_by(document=de_val,
                                      external_id=external_id,
                                      type=partner_name,
                                      )
    link_query.delete()

    db.session.commit()


def test_post_link_with_bad_zbl(client):
    zbl_id = "2062.129"
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


def test_patch_link_with_de(client):
    doc_id = 3273551
    external_id = "11.14#I1.i1.p1"
    partner_name = "DLMF"

    de_val = target_helpers.get_de_from_input(doc_id)

    link_query = Link.query.filter_by(document=de_val,
                                      external_id=external_id,
                                      type=partner_name,
                                      )
    link_to_edit = link_query.all()

    assert len(link_to_edit) > 0, "test link is not in database"

    new_doc_id = 2062129
    json_base = {"DE number": de_val,
                 "external id": external_id,
                 "partner": partner_name}
    json_edit = json_base.copy()
    json_edit["new_DE_number"] = new_doc_id
    param_edit = urlencode(json_edit)
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    response = client.patch(f"/links_api/link/item/?{param_edit}",
                            headers=headers,
                            )
    assert response.status_code == 204

    json_base["DE number"] = new_doc_id
    param_base = urlencode(json_base)
    response = client.get(f"/links_api/link/item/?{param_base}")
    data = response.json
    source: dict = data.get("Source")
    assert source["Identifier"]["ID"] == external_id

    # change back
    json_base["new_DE_number"] = doc_id
    param_base = urlencode(json_base)
    response = client.patch(f"/links_api/link/item/?{param_base}",
                            headers=headers,
                            )
    assert response.status_code == 204


def test_patch_link_with_new_source(client):
    doc_id = 3273551
    external_id = "11.14#I1.i1.p1"
    partner_name = "DLMF"

    de_val = target_helpers.get_de_from_input(doc_id)

    link_query = Link.query.filter_by(document=de_val,
                                      external_id=external_id,
                                      type=partner_name,
                                      )
    link_to_edit = link_query.all()

    assert len(link_to_edit) > 0, "test link is not in database"

    new_external_id = "26.8#vii.p4"

    json_base = {"DE number": doc_id,
                 "external id": external_id,
                 "partner": partner_name}
    json_edit = json_base.copy()
    json_edit["new_external_id"] = new_external_id
    param_edit = urlencode(json_edit)
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    response = client.patch(f"/links_api/link/item/?{param_edit}",
                            headers=headers,
                            )
    assert response.status_code == 204

    json_base["external id"] = new_external_id
    param_base = urlencode(json_base)
    response = client.get(f"/links_api/link/item/?{param_base}")
    data = response.json
    source: dict = data.get("Source")
    assert source["Identifier"]["ID"] == new_external_id

    # change link back
    json_base["new_external_id"] = external_id
    param_base = urlencode(json_base)
    response = client.patch(f"/links_api/link/item/?{param_base}",
                            headers=headers,
                            )
    assert response.status_code == 204

    # delete new source entry
    new_source = Source.query.filter_by(id=new_external_id)
    new_source.delete()
    db.session.commit()


def test_post_then_delete_link(client):
    document = 2062129
    external_id = "11.14#I1.i1.p1"
    partner_name = "DLMF"

    link_query = Link.query.filter_by(document=document,
                                      external_id=external_id,
                                      type=partner_name,
                                      )
    link = link_query.all()

    assert len(link) == 0, "test link to create is not unique"

    json = {"DE number": document,
            "external id": external_id,
            "partner": partner_name}
    param = urlencode(json)
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    response = client.post(f"/links_api/link/item/?{param}",
                           headers=headers,
                           )
    assert response.status_code == 201

    # delete test entry
    response = client.delete(f"/links_api/link/item/?{param}",
                             headers=headers,
                             )

def test_post_existing_link(client):
    document = 3273551
    external_id = "11.14#I1.i1.p1"
    partner_name = "DLMF"

    link_query = Link.query.filter_by(document=document,
                                      external_id=external_id,
                                      type=partner_name,
                                      )
    link = link_query.all()

    orig_number = len(link)
    assert orig_number > 0, "need to test against existing link"


    json = {"DE number": document,
            "external id": external_id,
            "partner": partner_name}
    param = urlencode(json)
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    response = client.post(f"/links_api/link/item/?{param}",
                           headers=headers,
                           )
    assert response.status_code == 422

    link = link_query.all()
    assert len(link) == orig_number


def test_empty_patch(client):
    document = 3273551
    external_id = "11.14#I1.i1.p1"
    partner_name = "DLMF"

    link_query = Link.query.filter_by(document=document,
                                      external_id=external_id,
                                      type=partner_name,
                                      )
    link = link_query.all()

    orig_number = len(link)
    assert orig_number > 0, "need to test against existing link"


    json = {"DE number": document,
            "external id": external_id,
            "partner": partner_name}
    param = urlencode(json)
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}
    response = client.patch(f"/links_api/link/item/?{param}",
                            headers=headers,
                            )
    assert response.status_code == 422

    link = link_query.all()
    assert len(link) == orig_number
