# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
"""
Statistics
===============================================================================


>>> from techminer2.tools import statistics
>>> statistics(
...     field='authors',    
...     database_params = {
...         "root_dir": "example/",
...         "database": "main",
...         "year_filter": (None, None),
...         "cited_by_filter": (None, None),
...     }
... ).head()
                    year                              ... local_citations                    
                   count    mean std     min     25%  ...             min  25%  50%  75%  max
authors                                               ...                                    
Almunawar M.N.       1.0  2019.0 NaN  2019.0  2019.0  ...             0.0  0.0  0.0  0.0  0.0
Alt R.               1.0  2018.0 NaN  2018.0  2018.0  ...             1.0  1.0  1.0  1.0  1.0
Anagnostopoulos I.   1.0  2018.0 NaN  2018.0  2018.0  ...             1.0  1.0  1.0  1.0  1.0
Anshari M.           1.0  2019.0 NaN  2019.0  2019.0  ...             0.0  0.0  0.0  0.0  0.0
Arner D.W.           1.0  2017.0 NaN  2017.0  2017.0  ...             0.0  0.0  0.0  0.0  0.0
<BLANKLINE>
[5 rows x 72 columns]


"""
from .._read_records import read_records


def statistics(
    field,
    database_params,
):
    """:meta private:"""

    records = read_records(**database_params)
    records = records.dropna(subset=[field])
    records[field] = records[field].str.split("; ")
    records = records.explode(field)
    records[field] = records[field].str.strip()
    summary = records.groupby(field).describe()

    return summary