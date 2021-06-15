
from zb_links.api.link.helpers.dlmf_source_helpers import get_title


def test_with_subsection():
    title = get_title("26.8#vii.p4")
    assert title == "Asymptotic Approximations"


def test_without_subsection():
    title = get_title("27.3")
    assert title == "Multiplicative Properties"


def test_figure():
    title = get_title("18.4.F2.mag")
    print(title)
    assert title == "18.4.2 Jacobi polynomials P_n^{(1.25,0.75)}⁡(x), n=7,8."


def test_bio():
    title = get_title("about/bio/GWolf#p2")
    assert title == "Profile Gerhard Wolf"
