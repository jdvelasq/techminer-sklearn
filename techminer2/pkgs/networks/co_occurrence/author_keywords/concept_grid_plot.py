# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Concept Grid Plot
===============================================================================


>>> from techminer2.pkgs.networks.co_occurrence.author_keywords import ConceptGridPlot
>>> plot = (
...     ConceptGridPlot()
...     #
...     # FIELD:
...     .having_terms_in_top(30)
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
>>> # plot.render("sphinx/images/co_occurrence_network/concept_grid_plot", format="png")


# .. image:: /images/co_occurrence_network/concept_grid_plot.png
#     :width: 900px
#     :align: center

"""
from .....internals.mixins import InputFunctionsMixin
from ..internals.concept_grid_plot import InternalConceptGridPlot


class ConceptGridPlot(
    InputFunctionsMixin,
):
    """:meta private:"""

    def build(self):
        """:meta private:"""

        return (
            InternalConceptGridPlot()
            .update_params(**self.params.__dict__)
            .with_field("author_keywords")
            .build()
        )
