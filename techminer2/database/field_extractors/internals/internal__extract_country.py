# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements

import glob
import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd  # type: ignore

from ....prepare.thesaurus.internals.thesaurus__read_as_dict import (
    thesaurus__read_as_dict,
)


def internal__extract_country(
    source_field,
    dest_field,
    #
    # DATABASE PARAMS:
    root_dir: str,
    database: str,
    record_years_range: Tuple[Optional[int], Optional[int]],
    record_citations_range: Tuple[Optional[int], Optional[int]],
    records_order_by: Optional[str],
    records_match: Optional[Dict[str, List[str]]],
):
    #
    # Loads the thesaurus
    thesaurus_path = os.path.join(root_dir, "thesauri/countries.the.txt")
    thesaurus = thesaurus__read_as_dict(thesaurus_path)
    names = list(thesaurus.keys())

    files = list(glob.glob(os.path.join(root_dir, "databases/_*.zip")))
    for file in files:
        data = pd.read_csv(file, encoding="utf-8", compression="zip")
        if source_field in data.columns:
            data[dest_field] = data[source_field].copy()
            data[dest_field] = data[dest_field].replace(np.nan, pd.NA)
            data[dest_field] = data[dest_field].str.split("; ")
            data[dest_field] = data[dest_field].map(
                lambda x: [
                    thesaurus[name][0] if name in y.lower() else pd.NA
                    for y in x
                    for name in names
                ],
                na_action="ignore",
            )
            data[dest_field] = data[dest_field].map(
                lambda x: [y for y in x if y is not pd.NA], na_action="ignore"
            )
            data[dest_field] = data[dest_field].map(
                lambda x: pd.NA if x == [] else x, na_action="ignore"
            )
            data[dest_field] = data[dest_field].map(
                lambda x: pd.NA if x is pd.NA else list(set(x)), na_action="ignore"
            )
            data[dest_field] = data[dest_field].str.join("; ")
            data[dest_field] = data[dest_field].map(
                lambda x: pd.NA if x == "" else x, na_action="ignore"
            )
        data.to_csv(file, sep=",", encoding="utf-8", index=False, compression="zip")