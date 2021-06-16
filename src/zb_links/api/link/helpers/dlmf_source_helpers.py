import re

import requests
from bs4 import BeautifulSoup


def get_page_title(soup):
    """

    Parameters
    ----------
    soup : BeautifulSoup object
        soup of the dlmf page.

    Returns
    -------
    title : str
        title of the html page.

    """
    title_with_prefix = soup.find("title")
    title = title_with_prefix.text.split(" ", 1)[1]
    return title.strip("/n").strip()


def roman(source_id):
    """

    Parameters
    ----------
    source_id : str
        identifier for entry in source table

    Returns
    -------
    bool
        True if the identifier points to a subsection.
    str
        title of subsection, if exists, else blank.

    """

    split_source = source_id.split("#")
    try:
        after_section = split_source[1]
        possible_roman = after_section.split(".")[0]
        romain_regex = (
            r"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
        )
        if re.search(romain_regex, possible_roman, flags=re.IGNORECASE):
            return True, possible_roman
        return False, ""
    except IndexError:
        return False, ""


def get_title(source_id):
    """

    Parameters
    ----------
    source_id : str
        identifier for entry in source table

    Returns
    -------
    title: str
        gives the title corresponding to the source_id
        returns None if id is invalid

    """

    title = None

    source_page = requests.get("https://dlmf.nist.gov/" + source_id)
    html_text = source_page.text
    soup = BeautifulSoup(html_text, "html.parser")

    subsection_results = roman(source_id)
    subsection_given = subsection_results[0]
    if subsection_given:
        subsection = subsection_results[1]
        section = soup.find("section", id=subsection)
        title = section.find(class_="ltx_title ltx_title_subsection")
    else:
        title = soup.find(class_="ltx_title ltx_title_section")
        if not title:
            prefix = ""
            if "about" in source_id:
                prefix = "Profile "
            return prefix + get_page_title(soup)

    for child in title.find_all("span"):
        child.decompose()

    return title.text.strip("/n").strip()
