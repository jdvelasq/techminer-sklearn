# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
"""
Highlight phrase
===============================================================================


>>> from techminer2.search import highlight_phrase
>>> highlight_phrase(
...    text = (
...        "They highlight the limited adoption of Regulatory Technology (RegTech) and "
...        "Electronic Signatures in Palestine's banking sector, proposing the establishment "
...        "of an independent Electronic Transactions Unit as a solution. They emphasize the "
...        "need for RegTech in achieving regulatory compliance, risk management, and reporting "
...        "in the face of changing regulations and digital dynamics. Additionally, the papers "
...        "delve into ethical concerns surrounding the application of Artificial Intelligence (AI) "
...        "in finance and suggest that RegTech, combined with Islamic finance principles, can "
...        "mitigate these ethical issues. Overall, the papers underscore the transformative "
...        "potential of RegTech while discussing its benefits, challenges, and implications "
...        "for diverse sectors, ultimately aiming to improve compliance, efficiency, and ethical "
...        "practices in the financial industry."
...     ),
...     #
...     # DATABASE PARAMS:
...     root_dir="data/regtech/",
... )
they highlight the limited adoption of REGULATORY_TECHNOLOGY (REGTECH) and
electronic signatures in palestine's BANKING sector, proposing the
establishment of an independent ELECTRONIC_TRANSACTIONS_UNIT as a solution.
they emphasize the need for REGTECH in achieving REGULATORY_COMPLIANCE,
RISK_MANAGEMENT, and REPORTING in the face of changing regulations and
digital dynamics. additionally, the papers delve into ethical concerns
surrounding the application of ARTIFICIAL_INTELLIGENCE (ai) in FINANCE and
suggest that REGTECH, combined with ISLAMIC_FINANCE principles, can
mitigate these ETHICAL_ISSUES. overall, the papers underscore the
transformative potential of REGTECH while discussing its benefits,
challenges, and implications for diverse sectors, ultimately aiming to
improve COMPLIANCE, efficiency, and ethical practices in the
FINANCIAL_INDUSTRY.

"""
import os
import os.path
import re
import textwrap

from ..thesaurus_lib import load_system_thesaurus_as_dict_reversed

TEXTWRAP_WIDTH = 73
THESAURUS_FILE = "words.txt"


def highlight_phrase(
    text,
    #
    # DATABASE PARAMS:
    root_dir="./",
):
    """
    :meta private:
    """

    #
    # Obtains a regex for descriptors
    thesaurus = load_thesaurus(root_dir)
    descriptors = list(thesaurus.values())
    descriptors = [d.translate(str.maketrans("_", " ")) for d in descriptors]
    descriptors = [d.lower().strip() for d in descriptors]
    descriptors = sorted(descriptors, key=lambda x: len(x.split(" ")), reverse=True)
    descriptors = [re.escape(d) for d in descriptors]
    descriptors = "|".join(descriptors)
    regex = re.compile(r"\b(" + descriptors + r")\b")

    #
    # Highlight the text with the descriptors
    text = text.lower().replace("_", " ")
    text = re.sub(regex, lambda z: z.group().upper().replace(" ", "_"), text)

    print(textwrap.fill(str(text), width=TEXTWRAP_WIDTH))


def load_thesaurus(root_dir):
    th_file = os.path.join(root_dir, THESAURUS_FILE)
    if not os.path.isfile(th_file):
        raise FileNotFoundError(f"The file {th_file} does not exist.")
    thesaurus = load_system_thesaurus_as_dict_reversed(th_file)
    return thesaurus