# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Clusters to Terms Mapping
===============================================================================


>>> from techminer2.pkgs.networks.co_occurrence.author_keywords import ClustersToTermsMapping
>>> mapping = (
...     ClustersToTermsMapping()
...     #
...     # FIELD:
...     .having_terms_in_top(10)
...     .having_terms_ordered_by("OCC")
...     .having_term_occurrences_between(None, None)
...     .having_term_citations_between(None, None)
...     .having_terms_in(None)
...     #
...     # COUNTERS:
...     .using_term_counters(True)
...     #
...     # NETWORK:
...     .using_clustering_algorithm_or_dict("louvain")
...     .using_association_index("association")
...     #
...     # DATABASE:
...     .where_directory_is("example/")
...     .where_database_is("main")
...     .where_record_years_between(None, None)
...     .where_record_citations_between(None, None)
...     .where_records_match(None)
...     #
...     .build()
... )
>>> from pprint import pprint
>>> pprint(mapping)



"""
from .....internals.mixins import InputFunctionsMixin
from ..internals.clusters_to_terms_mapping import InternalClustersToTermsMapping


class ClustersToTermsMapping(
    InputFunctionsMixin,
):
    """:meta private:"""

    def build(self):
        """:meta private:"""

        return (
            InternalClustersToTermsMapping()
            .update_params(**self.params.__dict__)
            .with_field("author_keywords")
            .build()
        )
