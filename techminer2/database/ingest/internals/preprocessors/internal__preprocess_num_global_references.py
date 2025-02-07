# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements

from ..operators.internal__count_terms_per_record import (
    internal__count_terms_per_record,
)


def internal__preprocess_num_global_references(root_dir):
    """Run importer."""

    internal__count_terms_per_record(
        source="global_references",
        dest="num_global_references",
        root_dir=root_dir,
    )
