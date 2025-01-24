# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Clean text
===============================================================================

>>> from techminer2.database.field_operators import CleanTextOperator
>>> (
...     CleanTextOperator()  # doctest: +SKIP 
...     .with_source_field("author_keywords")
...     .as_field("author_keywords_copy")
...     .where_directory_is("example/")
...     .build()
... )

"""
from ...internals.mixins import InputFunctionsMixin
from ..ingest.internals.operators.internal__clean_text import internal__clean_text
from .operators__protected_fields import PROTECTED_FIELDS


class CleanTextOperator(
    InputFunctionsMixin,
):
    """:meta private:"""

    def build(self):

        if self.params.dest_field in PROTECTED_FIELDS:
            raise ValueError(f"Field `{self.params.dest_field}` is protected")

        internal__clean_text(
            source=self.params.source_field,
            dest=self.params.dest_field,
            #
            # DATABASE PARAMS:
            root_dir=self.params.root_dir,
        )
