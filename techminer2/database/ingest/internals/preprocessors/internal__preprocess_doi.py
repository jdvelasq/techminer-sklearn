# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements

from ....field_operators.operators__transform_field import internal__transform_field


def _process_text(text):
    #
    #                                    10.7667/PSPC180358
    #                   10.7688/j.issn.1000-1646.2014.02.06
    #   https://doi.org/10.7688/j.issn.1000-1646.2014.02.06
    # http://dx.doi.org/10.7688/j.issn.1000-1646.2014.02.06
    #
    text = text.str.replace("https://doi.org/", "")
    text = text.str.replace("http://dx.doi.org/", "")
    text = text.str.upper()
    return text


def internal__preprocess_doi(root_dir):
    """Run authors importer."""

    internal__transform_field(
        source="doi",
        dest="doi",
        func=_process_text,
        root_dir=root_dir,
    )