# ------------------------------------------------------------------------------
# Display text in the API interface
# ------------------------------------------------------------------------------

from flask_restx import fields, marshal

from zb_links.api.restx import api
from zb_links.db.models import Provider, Source, ZBTarget

object_id_info = api.model(
    "identifier",
    {
        "ID": fields.String(
            readOnly=True, description="The unique identifier the object"
        ),
        "IDScheme": fields.String(
            required=True,
            description="Schematic used for the object identification",
        ),
        "IDURL": fields.String(description="web address of the object"),
    },
)

provider = api.model(
    "provider",
    {
        "provider_name": fields.String(
            required=True, description="name of the provider"
        ),
        "identifier": fields.Nested(object_id_info),
    },
)

name_model = api.model(
    "name",
    {
        "Name": fields.String(required=True),
        "Subtype": fields.String(required=True, description="MSC codes"),
    },
)

name_model_creator = api.model("name", {"Name": fields.String(required=True)})

publisher_model = api.model(
    "publisher",
    {
        "Name": fields.String(
            required=True, description="name of the zbMATH partner"
        ),
        "Identifier": fields.Nested(object_id_info),
    },
)

source = api.model(
    "source",
    {
        "Identifier": fields.Nested(object_id_info, required=True),
        "Type": fields.String(required=True, description="Type of link"),
        "Title": fields.String(
            required=False, description="Title of section where link arises"
        ),
        "Publisher": fields.Nested(publisher_model, required=True),
    },
)

target = api.model(
    "target",
    {
        "Identifier": fields.Nested(object_id_info),
        "Type": fields.Nested(name_model),
        "Title": fields.String(description="title of the publication"),
        "Creator": fields.List(fields.Nested(name_model_creator)),
        "PublicationDate": fields.Integer(description="year of publication"),
        "Publisher": fields.String(
            required=True,
            description="publisher of book or journal name of publication",
        ),
    },
)

link = api.model(
    "link to zbMATH",
    {
        "Source": fields.Nested(
            source, required=True, description="source of the link"
        ),
        "Target": fields.Nested(
            target,
            required=True,
            description="target (zbMATH object) of the link",
        ),
        "LinkPublicationDate": fields.DateTime(
            required=True, description="Date the link was established"
        ),
        "LinkProvider": fields.Nested(
            provider, required=True, description="provider of the link"
        ),
        "RelationshipType": fields.String(
            required=True,
            description="Type of relationship described by the link",
        ),
    },
)


# List of all links to zbMATH objects
def get_display(link_element):

    element_source = link_element.external_id
    element_target = link_element.document
    element_link_publication_date = link_element.created_at
    element_link_provider = link_element.created_by
    element_relationship_type = None

    source_publisher_url = ""
    source_publisher_id_scheme = ""
    partner = link_element.type
    if partner == "DLMF":
        source_publisher_url = "https://dlmf.nist.gov/"
        source_publisher_id_scheme = "name of partner"

    source_obj = Source.query.get(element_source)
    source_id_dict = {
        "ID": source_obj.id,
        "IDScheme": source_obj.id_scheme,
        "IDURL": source_obj.url,
    }
    source_name_dict = {"Name": source_obj.type}
    source_publisher_identifier_dict = {
        "ID": partner,
        "IDScheme": source_publisher_id_scheme,
        "IDURL": source_publisher_url,
    }
    source_publisher_dict = {
        "Name": partner,
        "Identifier": marshal(
            source_publisher_identifier_dict, object_id_info
        ),
    }
    source_dict = {
        "Identifier": marshal(source_id_dict, object_id_info),
        "Type": marshal(source_name_dict, name_model_creator),
        "Title": source_obj.title,
        "Publisher": marshal(source_publisher_dict, publisher_model),
    }

    target_obj = ZBTarget.query.get(element_target)
    target_id_dict = {
        "ID": target_obj.zbl_id,
        "IDScheme": "zbMATH scheme",
        "IDURL": "https://zbmath.org/",
    }

    target_name_msc_dict = {
        "Name": target_obj.type,
        "Subtype": target_obj.classification,
    }

    target_dict = {
        "Identifier": marshal(target_id_dict, object_id_info),
        "Type": marshal(target_name_msc_dict, name_model),
        "PublicationDate": target_obj.year,
    }

    # TODO: maybe want to erase provider.id;
    # the link is connected to provider through name
    # provider_obj = Provider.query.filter_by(name=element_link_provider).first()
    # TODO: replace next with the above
    provider_obj = Provider.query.filter_by(name="zbMATH").first()
    provider_id_dict = {
        "ID": provider_obj.name,
        "IDScheme": provider_obj.scheme,
        "IDURL": provider_obj.url,
    }
    provider_dict = {
        "identifier": marshal(provider_id_dict, object_id_info),
        "provider_name": provider_obj.name,
    }

    links_display_format = {
        "Source": marshal(source_dict, source),
        "Target": marshal(target_dict, target),
        "LinkPublicationDate": element_link_publication_date,
        "LinkProvider": marshal(provider_dict, provider),
        "RelationshipType": element_relationship_type,
    }

    return links_display_format
