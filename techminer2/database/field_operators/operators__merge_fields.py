# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Merge Fields
===============================================================================

>>> from techminer2.database.operations import MergeFieldsOperator
>>> (
...     MergeFieldsOperator()  # doctest: +SKIP
...     .for_fields(
...         with_name=["author_keywords", "index_keywords"],
...         to_name="merged_keywords",
...     ).for_data(
...         in_root_dir="example",
...     ).build()
... )

"""
from ...internals.set_params_mixin.set_params_mixin import SetParamsMixin
from ...internals.set_params_mixin.set_source_dest_params import SourceDestParams
from ..internals.field_operators.internal__merge_fields import internal__merge_fields
from .operators__protected_fields import PROTECTED_FIELDS


class MergeFieldsOperator(
    SetParamsMixin,
):
    """:meta private:"""

    def __init__(self):
        self.params = SourceDestParams()

    def build(self):

        if self.params.dest in PROTECTED_FIELDS:
            raise ValueError(f"Field `{self.params.dest}` is protected")

        internal__merge_fields(
            source=self.params.source,
            dest=self.params.dest,
            #
            # DATABASE PARAMS:
            root_dir=self.params.root_dir,
        )