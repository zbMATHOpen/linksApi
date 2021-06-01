from flask import jsonify


def make_message(status_code, message):
    """

    Parameters
    ----------
    status_code : int
        status code of the response.

    message: str or list of string
        message(s) to display

    Returns
    -------
    response : json obj
        response with a status code and an error message

    """

    response = jsonify({"status": status_code, "message": message})
    response.status_code = status_code
    return response


def get_provider():
    """
    Returns
    -------
    provider_name : str
        the currently logged in user who is providing the new link

    """

    provider_name = "Dariush, Matteo"
    return provider_name
