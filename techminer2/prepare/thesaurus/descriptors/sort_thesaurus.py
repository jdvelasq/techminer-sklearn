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


## >>> from techminer2.prepare.thesaurus.descriptors import sort_thesaurus
## >>> sort_thesaurus(
## ...     # 
## ...     # SORT OPTIONS:
## ...     order="alphabetical",
## ...     #
## ...     # DATABASE PARAMS:
## ...     root_dir="example/", 
## ... )
--INFO-- The file example/thesauri/descriptors.the.txt has been sorted.

"""
from ..internals.thesaurus__sort_on_disk import (
    thesaurus__sort_on_disk as core_sort_thesaurus,
)

THESAURUS_FILE = "thesauri/descriptors.the.txt"


def sort_thesaurus(
    #
    # SORT OPTIONS:
    order="alphabetical",
    #
    # DATABASE PARAMS:
    root_dir="./",
):
    """:meta private:"""

    core_sort_thesaurus(
        #
        # FILE PARAMS:
        thesaurus_file=THESAURUS_FILE,
        order=order,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
    )