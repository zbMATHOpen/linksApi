arg_names = {
    "auth": "authors",
    "classification": "MSC code",
    "doc": "DE_number",  # TODO: this should be merged with next
    "document": "DE number",
    "link_ext_id": "external id",
    "link_partner": "partner",
    "edit_link_doc": "new_DE_number",
    "edit_link_ext_id": "new_external_id",
    "edit_link_partner": "new_partner",
}

descriptions = {
    arg_names[
        "auth"
    ]: "Ex: Abramowitz, M. (multiple inputs with ; as delimiter)",
    arg_names[
        "classification"
    ]: "Ex: 33-00 (multiple inputs with space as delimiter)",
    arg_names["doc"]: "Ex: 3273551 (DE number) or 0171.38503 (Zbl code)",
    arg_names[
        "link_ext_id"
    ]: "Ex (DLMF): 11.14#I1.i1.p1 (identifier of the link)",
    arg_names["link_partner"]: "Ex: DLMF, OEIS, etc.",
    # TODO: add the remaining descriptions
    arg_names["edit_link_doc"]: "",
    arg_names["edit_link_ext_id"]: "",
    arg_names["edit_link_partner"]: "",
}
