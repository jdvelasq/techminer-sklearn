"""
This module implements functions to add OCC:citations counters to topics 
in the values or axis of a dataframe.




"""

import numpy as np

from . import techminer


def add_counters_to_axis(
    dataframe,
    axis,
    criterion,
    root_dir,
    database,
    start_year,
    end_year,
    **filters,
):
    """Adds OCC:citations counters to topics in the axis of a dataframe.

    Args:
        dataframe (pandas.DataFrame): The dataframe.
        axis (int): 0 for index, 1 for columns.
        criterion (str): The criterion to be analyzed.
        root_dir (str): The working directory.
        database (str): The database name. It can be 'documents', 'cited_by' or 'references'.
        start_year (int): The start year for filtering the data.
        end_year (int): The end year for filtering the data.
        filters (dict): A dictionary of filters. The keys are the field names and the values are the filter values.

    Returns:
        pandas.DataFrame: The dataframe with OCC:citations counters added to topics in the axis.

    """

    dataframe = dataframe.copy()

    new_column_names = items2counters(
        criterion=criterion,
        root_dir=root_dir,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    if axis == 0:
        dataframe.index = dataframe.index.map(new_column_names)
    else:
        dataframe.columns = dataframe.columns.map(new_column_names)

    return dataframe


def add_counters_to_column_values(
    column,
    name,
    directory,
    database,
    table,
    start_year,
    end_year,
    **filters,
):
    new_column_names = items2counters(
        criterion=column,
        root_dir=directory,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )
    table[name] = table[name].map(new_column_names)
    return table


def items2counters(
    criterion,
    root_dir,
    database,
    start_year,
    end_year,
    **filters,
):
    """Creates a dictionary to transform a 'item' to a 'item counter:counter'."""

    indicators = techminer.indicators.indicators_by_topic(
        criterion=criterion,
        root_dir=root_dir,
        database=database,
        start_year=start_year,
        end_year=end_year,
        **filters,
    )

    names = indicators.index.to_list()
    occ = indicators.OCC.to_list()
    cited_by = indicators.global_citations.to_list()

    n_zeros_occ = int(np.log10(max(occ))) + 1
    n_zeros_cited_by = int(np.log10(max(cited_by))) + 1

    fmt_occ = "{:0" + str(n_zeros_occ) + "d}"
    fmt_cited_by = "{:0" + str(n_zeros_cited_by) + "d}"
    fmt = "{} " + f"{fmt_occ}:{fmt_cited_by}"

    return {
        name: fmt.format(name, int(nd), int(tc))
        for name, nd, tc in zip(names, occ, cited_by)
    }


def remove_counters_from_axis(
    dataframe,
    axis,
):
    """Remove counters from axis."""

    def remove_counters(text):
        text = text.split(" ")
        text = text[:-1]
        text = " ".join(text)
        return text

    dataframe = dataframe.copy()

    if axis == 0:
        dataframe.index = dataframe.index.map(remove_counters)
    else:
        dataframe.columns = dataframe.columns.map(remove_counters)

    return dataframe