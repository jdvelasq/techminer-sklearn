# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-few-public-methods
"""
Delete a Field
===============================================================================

>>> from techminer2.database.field_operators import DeleteFieldOperator
>>> (
...     DeleteFieldOperator()  # doctest: +SKIP 
...     #
...     # FIELDS:
...     .with_field("author_keywords_copy")
...     #
...     # DATABASE:
...     .where_directory_is("example/")
...     #
...     .build()
... )

"""

from ...internals.mixins import InputFunctionsMixin
from ..ingest.internals.operators.internal__delete_field import internal__delete_field
from .protected_fields import PROTECTED_FIELDS


class DeleteFieldOperator(
    InputFunctionsMixin,
):
    """:meta private:"""

    def build(self):

        if self.params.field in PROTECTED_FIELDS:
            raise ValueError(f"Field `{self.params.field}` is protected")

        internal__delete_field(
            field=self.params.field,
            #
            # DATABASE PARAMS:
            root_dir=self.params.root_dir,
        )
