
import re

from zb_links.api.link.helpers.dlmf_source_helpers import get_title


def test_with_subsection():
    title = get_title("26.8#vii.p4")
    dlmf_title = """
        §26.8(vii) Asymptotic Approximations
        ‣ Properties ‣ Chapter 26 Combinatorial Analysis
    """
    dlmf_title = re.sub(" +", " ", dlmf_title)
    dlmf_title = dlmf_title.replace("\n", "").strip()
    assert title == dlmf_title


def test_without_subsection():
    title = get_title("27.3")
    assert title == "§27.3 Multiplicative Properties"


def test_figure():
    title = get_title("18.4.F2.mag")
    assert title == "18.4.2 Jacobi polynomials P_n^{(1.25,0.75)}⁡(x), n=7,8."


def test_bio():
    title = get_title("about/bio/GWolf#p2")
    assert title == "Profile Gerhard Wolf"
