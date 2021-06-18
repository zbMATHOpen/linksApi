from zb_links.db.models import ZBTarget


def get_de_from_zbl_id(doc_id):
    """

    Parameters
    ----------
    doc_id : str or int (as string)
        represents the DE number (document) resp. the Zbl code (zbl_id)
        of a document in math_documents

    Returns
    -------
    de_val : int
        the DE number corresponding to the doc_id

    """
    de_val = None
    try:
        de_val = int(doc_id)
    except ValueError:
        zb_obj = ZBTarget.query.filter_by(zbl_id=doc_id).first()
        if zb_obj:
            de_val = zb_obj.id

    return de_val
