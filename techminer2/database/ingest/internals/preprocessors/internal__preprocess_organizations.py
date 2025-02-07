# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
"""
Create 'organizations.txt' thesaurus file 
===============================================================================

Creates a organizations thesaurus from the data in the database.


# >>> from techminer2.ingest._list_cleanup_organizations import list_cleanup_organizations
# >>> list_cleanup_organizations(root_dir="example/")  # doctest: +SKIP
# --INFO-- The example/thesauri/organizations.the.txt thesaurus file was created


"""
import pathlib
import re

import pandas as pd  # type: ignore
import pkg_resources  # type: ignore

# TODO: remove dependency
from .....thesaurus.organizations.apply_thesaurus import (
    apply_thesaurus as apply_organizations_thesaurus,
)


def internal__preprocess_organizations(root_dir="./"):
    """Creates organizations.txt thesaurus file."""

    dataframe = load_affiliations_from_country_thesaurus(root_dir)
    dataframe = add_country_code_column(dataframe)
    dataframe = add_candidate_organization_column(dataframe)
    dataframe = replace_abbreviations(dataframe)
    knwon_orgs = load_known_organizations()
    dataframe = assigns_from_kwown_organizations(dataframe, knwon_orgs)
    dataframe = assings_names_by_priority(dataframe)
    dataframe = format_organization_names(dataframe)
    save_organizations_thesaurus(dataframe, root_dir)

    apply_organizations_thesaurus(root_dir)

    print(
        f"--INFO-- The {pathlib.Path(root_dir) / 'thesauri/organizations.the.txt'} "
        "thesaurus file was created"
    )


def load_affiliations_from_country_thesaurus(root_dir):
    """Loads data from countries.txt file."""

    country = None
    countries = []
    affiliations = []

    #
    # collects the countries and the respective affiliations
    file_path = pathlib.Path(root_dir) / "thesauri/countries.the.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.startswith(" "):
                country = line.strip()
            else:
                affiliation = line.strip()
                countries.append(country)
                affiliations.append(affiliation)

    frame = pd.DataFrame(
        {
            "raw_affiliation": affiliations,
            "country": countries,
        }
    )
    return frame


def add_country_code_column(frame):
    """Add 'code' column to the frame."""

    #
    # Load country thesaurus
    countries = {}
    #
    file_path = pkg_resources.resource_filename(
        "techminer2", "package_data/thesaurus/geography/country-to-alpha3.the.txt"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.startswith(" "):
                country = line.strip()
            else:
                code = line.strip()
                countries[country] = code

    frame = frame.copy()
    frame["code"] = "unknown"
    for country, code in countries.items():
        frame.loc[frame.country == country, "code"] = code

    return frame


def add_candidate_organization_column(frame):
    """Adds raw candidate organizations.

    The raw candidate organizations are the two first components
    of the raw affiliations in lower case.

    """
    frame = frame.copy()
    frame["organization"] = frame.raw_affiliation
    return frame


def replace_abbreviations(frame):
    """Replace abbr in affiliation names."""

    abbr_dict = {}
    file_path = pkg_resources.resource_filename(
        "techminer2", "package_data/thesaurus/abbreviations/organizations_abbr.the.txt"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.startswith(" "):
                word = line.strip()
            else:
                abbr = line.strip()
                abbr_dict[word] = abbr

    for word, abbr in abbr_dict.items():
        frame["organization"] = frame["organization"].str.replace(
            r"\b" + word + r"\b", abbr, regex=True
        )

    frame["organization"] = frame["organization"].str.strip()

    return frame


def add_a_empty_organization_column(frame):
    """Adds empty organizations."""

    frame = frame.copy()
    frame["organizations"] = pd.NA
    return frame


def load_known_organizations():
    """Loads known organizations from GitHub repo."""

    file_path = pkg_resources.resource_filename(
        "techminer2", "package_data/word_lists/known_organizations.txt"
    )
    with open(file_path, "r", encoding="utf-8") as file:
        known_organizations = file.read().split("\n")
    known_organizations = [org.strip() for org in known_organizations]
    return known_organizations


def assigns_from_kwown_organizations(frame, knwon_orgs):
    """Adds organizations from known organizations."""

    frame = frame.copy()
    for org in knwon_orgs:
        frame.loc[
            frame.raw_affiliation.astype(str).str.contains(org, case=False),
            "organization",
        ] = org
    return frame


# names sorted by proirity
NAMES = [
    "Min",  # ministry, ministerio
    "Univ",  # university, universidad, univedade, ...
    "Bank",  # bank, banco
    "Banco",
    "AG",  # agency, agencia
    "Counc",  # council, concilio, consejo
    "Conc",  # concilio, consejo
    "Com",  # comission, comision
    "Consortium",
    "Politec",  # polytechnic, politecnico
    "Polytech",  # polytechnic, politecnico
    "Hosp",  # hospital
    "Assn",  # association
    "Asoc",  # asociacion
    "Soc",
    "Consor",
    "Co",
    "Org",
    "Inc",
    "Ltd",
    "Off",
    "Corp",
    "Gob",
    "Gov",
    "Found",
    "Fund",
    "Inst",
    "Coll",
    "Sch",
]


def assings_names_by_priority(frame):
    """Assigns the organization name by priority."""

    def select_name(affiliation):
        for name in NAMES:
            regex = r"\b" + name + r"\b"

            if re.search(regex, affiliation, re.IGNORECASE):
                parts = affiliation.split(",")
                for part in parts:
                    if re.search(regex, part, re.IGNORECASE):
                        return part.strip()
        return affiliation

    #
    # Main code:
    #
    frame = frame.copy()
    for index, row in frame.iterrows():
        if row.organization is pd.NA:
            frame.loc[index, "organization"] = select_name(
                frame.loc[index, "affiliation"]
            )

    frame["organization"] = frame["organization"].map(select_name)
    return frame


def format_organization_names(frame):
    """Formats the organization names."""

    frame = frame.copy()
    frame["organization"] = (
        frame["organization"].astype(str) + " (" + frame["code"] + ")"
    )
    return frame


def save_organizations_thesaurus(frame, root_dir):
    """Saves the thesaurus."""

    frame = frame.copy()

    existent_organizations = read_existent_organizations_txt_thesaurus(root_dir)

    if existent_organizations is not None:
        frame = pd.concat([existent_organizations, frame], ignore_index=True)
        frame = frame.drop_duplicates(subset=["raw_affiliation"])
        frame = frame.reset_index(drop=True)

    ##
    frame = frame.sort_values(["organization", "raw_affiliation"])
    frame = frame.groupby("organization", as_index=False).agg({"raw_affiliation": list})

    file_path = pathlib.Path(root_dir) / "thesauri/organizations.the.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        for _, row in frame.iterrows():
            file.write(row.organization + "\n")
            for aff in row.raw_affiliation:
                file.write("    " + aff + "\n")


def read_existent_organizations_txt_thesaurus(root_dir):
    """Read the existent thesaurus if exists."""
    file_path = pathlib.Path(root_dir) / "thesauri/organizations.the.txt"

    organization = None
    organizations = []
    affiliations = []

    if not file_path.exists():
        return None

    # collects the countries and the respective affiliations
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.startswith(" "):
                organization = line.strip()
            else:
                affiliation = line.strip()
                organizations.append(organization)
                affiliations.append(affiliation)

    frame = pd.DataFrame(
        {
            "raw_affiliation": affiliations,
            "organization": organizations,
        }
    )

    return frame
