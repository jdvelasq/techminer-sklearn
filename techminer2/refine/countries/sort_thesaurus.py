# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
"""
Sort Thesaurus
===============================================================================


>>> from techminer2.refine.countries import sort_thesaurus
>>> sort_thesaurus(
...     #
...     # DATABASE PARAMS:
...     root_dir="data/regtech/",
... )
--INFO-- The file data/regtech/countries.txt has been sorted.

"""
from .._sort_thesaurus import _sort_thesaurus

THESAURUS_FILE = "countries.txt"


def sort_thesaurus(
    #
    # DATABASE PARAMS:
    root_dir="./",
):
    """
    :meta private:
    """

    _sort_thesaurus(
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        #
        # FILE PARAMS:
        thesaurus_file=THESAURUS_FILE,
    )