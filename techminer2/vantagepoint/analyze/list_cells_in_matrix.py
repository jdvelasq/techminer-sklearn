"""
List Cells in Matrix
===============================================================================

Creates a list that has a row for each cell in the original matrix. The list is
sorted by the value of the cell. The columns of the original matrix correspond
to the 'column' column of the list, and the rows of the original matrix
correspond to the 'row' column of the list. The value of the cell is stored in
the 'value' column of the list.


>>> root_dir = "data/regtech/"

>>> from techminer2 import vantagepoint
>>> matrix = vantagepoint.analyze.auto_corr_matrix(
...     criterion='authors',
...     topics_length=10,
...     root_dir=root_dir,
... )

>>> matrix_list = vantagepoint.analyze.list_cells_in_matrix(matrix)
>>> matrix_list.cells_list_.head()
                row            column  CORR
0    Arner DW 3:185    Arner DW 3:185   1.0
1    Arner DW 3:185  Buckley RP 3:185   1.0
2   Brennan R 2:014   Brennan R 2:014   1.0
3  Buckley RP 3:185    Arner DW 3:185   1.0
4  Buckley RP 3:185  Buckley RP 3:185   1.0

>>> print(matrix_list.prompt_)
Analyze the table below which contains the auto-correlation values for the \
authors. High correlation values indicate that the topics tends to appear \
together in the same document and forms a group. Identify any notable \
patterns, trends, or outliers in the data, and discuss their implications for \
the research field. Be sure to provide a concise summary of your findings in \
no more than 150 words.
<BLANKLINE>
|    | row             | column           |   CORR |
|---:|:----------------|:-----------------|-------:|
|  1 | Arner DW 3:185  | Buckley RP 3:185 |  1     |
| 10 | Lin W 2:017     | Singh C 2:017    |  1     |
| 14 | Brennan R 2:014 | Crane M 2:014    |  1     |
| 16 | Hamdan A 2:018  | Sarea A 2:012    |  0.417 |
<BLANKLINE>
<BLANKLINE>

"""

from ...classes import ListCellsInMatrix


def list_cells_in_matrix(obj):
    """List the cells in a matrix."""

    def generate_prompt(obj):
        """Generate a ChatGPT prompt."""

        matrix = obj.cells_list_.copy()
        matrix = matrix[matrix.row != matrix.column]
        matrix = matrix[matrix.row < matrix.column]

        if obj.criterion_ == obj.other_criterion_ and obj.metric_ == "CORR":
            return prompt_for_auto_corr_matrix(obj, matrix)

        if obj.criterion_ != obj.other_criterion_ and obj.metric_ == "CORR":
            return prompt_for_cross_corr_matrix(obj, matrix)

        if obj.criterion_ == obj.other_criterion_ and obj.metric_ == "OCC":
            return prompt_for_co_occ_matrix(obj, matrix)

        if obj.criterion_ != obj.other_criterion_ and obj.metric_ == "OCC":
            return prompt_for_occ_matrix(obj, matrix)

        raise ValueError("Invalid metric")

    def prompt_for_auto_corr_matrix(obj, matrix):
        """Prompt for auto-correlation matrix."""

        return (
            "Analyze the table below which contains the auto-correlation "
            f"values for the {obj.criterion_}. High correlation "
            "values indicate that the topics tends to appear together in the "
            "same document and forms a group. Identify any notable patterns, "
            "trends, or outliers in the data, and discuss their implications "
            "for the research field. Be sure to provide a concise summary of "
            "your findings in no more than 150 words."
            f"\n\n{matrix.round(3).to_markdown()}\n\n"
        )

    def prompt_for_cross_corr_matrix(obj, matrix):
        """Prompt for cross-correlation matrix."""

        return (
            "Analyze the table below which contains the cross-correlation "
            f"values for the {obj.criterion_} based on the values "
            f"of the {obj.other_criterion_}. High correlation values "
            f"indicate that the topics in {obj.criterion_} are "
            f"related based on the values of the {obj.other_criterion_}. "
            "Identify any notable patterns, trends, or outliers in the data, "
            "and discuss their implications for the research field. Be sure "
            "to provide a concise summary of your findings in no more than "
            "150 words."
            f"\n\n{matrix.round(3).to_markdown()}\n\n"
        )

    def prompt_for_co_occ_matrix(obj, matrix):
        """Prompt for co-occurrence matrix."""

        return (
            "Analyze the table below, which contains the the co-occurrence "
            f"values for {obj.criterion_}. Identify any notable "
            "patterns, trends, or outliers in the data, and discuss their "
            "implications for the research field. Be sure to provide a "
            "concise summary of your findings in no more than 150 words."
            f"\n\n{matrix.to_markdown()}\n\n"
        )

    def prompt_for_occ_matrix(obj, matrix):
        """Prompt for co-occurrence matrix."""

        return (
            "Analyze the table below, which contains the the occurrence "
            f"values for {obj.criterion_} and "
            f"{obj.other_criterion_}. Identify any notable patterns, "
            "trends, or outliers in the data, and discuss their implications "
            "for the research field. Be sure to provide a concise summary of "
            "your findings in no more than 150 words."
            f"\n\n{matrix.to_markdown()}\n\n"
        )

    def transform_matrix_to_matrix_list(obj):
        """Transoform a matrix object to a matrix list object."""

        matrix = obj.matrix_
        value_name = obj.metric_

        matrix = matrix.melt(
            value_name=value_name, var_name="column", ignore_index=False
        )
        matrix = matrix.reset_index()
        matrix = matrix.rename(columns={"index": "row"})
        matrix = matrix.sort_values(
            by=[value_name, "row", "column"], ascending=[False, True, True]
        )
        matrix = matrix[matrix[value_name] > 0.0]
        matrix = matrix.reset_index(drop=True)

        return matrix

    #
    #
    # Main:
    #
    #

    results = ListCellsInMatrix()
    results.cells_list_ = transform_matrix_to_matrix_list(obj)
    results.criterion_ = obj.criterion_
    results.other_criterion_ = obj.other_criterion_
    results.metric_ = obj.metric_
    results.prompt_ = generate_prompt(results)

    return results