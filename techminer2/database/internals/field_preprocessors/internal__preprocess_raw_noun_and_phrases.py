# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements

from ...field_operators.operators__merge_fields import internal__merge_fields


def internal__preprocess_raw_noun_and_phrases(root_dir):

    internal__merge_fields(
        source=[
            "raw_document_title_nouns_and_phrases",
            "raw_abstract_nouns_and_phrases",
        ],
        dest="raw_nouns_and_phrases",
        root_dir=root_dir,
    )