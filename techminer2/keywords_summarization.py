"""
Keywords Summarization
===============================================================================

>>> directory = "data/regtech/"

>>> from techminer2 import keywords_summarization
>>> keywords_summarization(
...     column="author_keywords",
...     keywords=["fintech", "blockchain"],
...     n_phrases=5,    
...     directory=directory,
... )
--INFO-- Generating data/regtech/reports/keywords_summarization.txt

"""
import sys
import textwrap
from os.path import isfile, join

from ._read_records import read_records
from .load_thesaurus_as_dict import load_thesaurus_as_dict


def keywords_summarization(
    column,
    keywords=None,
    n_phrases=10,
    sufix="",
    directory="./",
):
    def expand_keywords(keywords):
        #
        # Expands the original keywords list to the equivalent keywords in the thesaurus.
        #
        thesaurus_file = join(directory, "processed", "keywords.txt")
        if isfile(thesaurus_file):
            th = load_thesaurus_as_dict(thesaurus_file)
        else:
            raise FileNotFoundError(
                "The file {} does not exist.".format(thesaurus_file)
            )

        # extract keys for thesaurus
        reversed_th = {value: key for key, values in th.items() for value in values}
        th_keys = []
        for keyword in keywords:
            th_keys.append(reversed_th[keyword])
        expanded_keywords = [text for key in th_keys for text in th[key]]

        return expanded_keywords

    def select_documents(documents, column, expanded_keywords):
        documents = documents.copy()
        documents["_points_"] = 0
        documents["title"] = documents["title"].str.lower()

        for keyword in expanded_keywords:
            documents.loc[
                documents.title.str.contains(keyword, regex=False), "_points_"
            ] += 3

        for keyword in expanded_keywords:
            documents.loc[
                documents.abstract.str.contains(keyword, regex=False, na=False),
                "_points_",
            ] += 1

        #
        documents[column] = documents[column].str.split(";")
        documents[column] = documents[column].map(
            lambda x: [item.strip() for item in x] if isinstance(x, list) else x
        )
        documents[column] = documents[column].map(
            lambda x: len(set(expanded_keywords) & set(x)) if isinstance(x, list) else 0
        )
        documents["_points_"] = documents["_points_"] + documents[column]
        #
        documents = documents[documents._points_ > 0]
        documents = documents.sort_values(
            by=["_points_", "global_citations"], ascending=False
        )

        for keyword in expanded_keywords:
            keyword = keyword.replace("(", "\(").replace(")", "\)")
            keyword = keyword.replace("[", "\[").replace("]", "\]")
            documents["title"] = documents["title"].str.replace(
                r"\b" + keyword + r"\b", keyword.upper()
            )

            documents["abstract"] = documents["abstract"].str.replace(
                r"\b" + keyword + r"\b", keyword.upper()
            )

        return documents

    def write_report(documents, sufix):

        # ----< select columns to report >-----------------------------------------------
        documents = documents.copy()
        column_list = []
        reported_columns = [
            "title",
            "authors",
            "global_citations",
            "source_title",
            "year",
            "abstract",
        ]
        for column in reported_columns:
            if column in documents.columns:
                column_list.append(column)
        documents = documents[column_list]

        # ----< report >-----------------------------------------------------------------
        filename = join(directory, "reports", f"keywords_summarization{sufix}.txt")

        with open(filename, "w") as out_file:

            sys.stdout.write("--INFO-- Generating " + filename + "\n")

            for index, row in documents.iterrows():

                for column in reported_columns:

                    if column not in row.index:
                        continue

                    if column == "title":
                        print("      title :", end="", file=out_file)
                        print(
                            textwrap.fill(
                                row[column],
                                width=115,
                                initial_indent=" " * 23,
                                subsequent_indent=" " * 23,
                                fix_sentence_endings=True,
                            )[22:],
                            file=out_file,
                        )
                        continue

                    if column == "abstract":

                        if not isinstance(row[column], float):
                            print("            abstract :", end="", file=out_file)
                            print(
                                textwrap.fill(
                                    row[column],
                                    width=115,
                                    initial_indent=" " * 23,
                                    subsequent_indent=" " * 23,
                                    fix_sentence_endings=True,
                                )[22:],
                                file=out_file,
                            )
                        continue

                    print(" {:>19} : {}".format(column, row[column]), file=out_file)

                if index != documents.index[-1]:
                    print(
                        "-" * 120,
                        file=out_file,
                    )

    # ----< data must be a list >--------------------------------------------------------
    if isinstance(keywords, str):
        keywords = [keywords]
    keywords = [word for word in keywords if word != ""]

    documents = read_records(directory)
    expanded_keywords = expand_keywords(keywords)
    documents = select_documents(documents, column, expanded_keywords)
    documents = documents.head(n_phrases)
    write_report(documents, sufix)


# def _keywords_summarization(
#     column,
#     keywords=None,
#     n_phrases=10,
#     sufix="",
#     directory="./",
# ):
#     def expand_keywords(keywords):
#         #
#         # Expands the original keywords list to the equivalent keywords in the thesaurus.
#         #
#         thesaurus_file = join(directory, "keywords.txt")
#         if isfile(thesaurus_file):
#             th = load_file_as_dict(thesaurus_file)
#         else:
#             raise FileNotFoundError(
#                 "The file {} does not exist.".format(thesaurus_file)
#             )

#         # extract keys for thesaurus
#         reversed_th = {value: key for key, values in th.items() for value in values}
#         th_keys = []
#         for keyword in keywords:
#             th_keys.append(reversed_th[keyword])
#         expanded_keywords = [text for key in th_keys for text in th[key]]

#         return expanded_keywords

#     def select_documents(documents, column, expanded_keywords):
#         documents = documents.copy()
#         documents.index = documents.record_no
#         documents = documents[column]
#         documents = documents.str.split(";")
#         documents = documents.explode()
#         documents = documents.str.strip()
#         documents = documents.isin(expanded_keywords)
#         document_id = list(set(documents.index.tolist()))
#         return document_id

#     def load_abstracts(documents_id, expanded_keywords):
#         expanded_keywords = expanded_keywords.copy()
#         file_name = join(directory, "abstracts.csv")
#         abstracts = pd.read_csv(file_name)
#         abstracts = abstracts[abstracts.record_no.isin(documents_id)]
#         expanded_keywords = [
#             word.replace("(", "\(").replace(")", "\)") for word in expanded_keywords
#         ]
#         regex = r"\b(" + "|".join(expanded_keywords) + r")\b"
#         abstracts = abstracts[abstracts.text.str.contains(regex, regex=True)]
#         return abstracts

#     def summarize(abstracts, expanded_keywords):

#         porter_stemmer = PorterStemmer()

#         abstracts = abstracts.copy()

#         # Prepare text
#         abstracts["formatted_text"] = abstracts.text.copy()
#         replace_list = [
#             (r"[[0-9]]*", " "),
#             (r"s+", " "),
#             (r"[a-zA-Z]", " "),
#             (r"s+", " "),
#         ]
#         for pat, repl in replace_list:
#             abstracts["formatted_text"] = abstracts["formatted_text"].str.replace(
#                 pat, repl
#             )

#         # Count word frequency
#         stopwords = nltk.corpus.stopwords.words("english")
#         word_frequencies = {}
#         for phrase in abstracts["formatted_text"].values:
#             for word in nltk.word_tokenize(phrase):
#                 word = porter_stemmer.stem(word)
#                 if word not in stopwords:
#                     if word not in word_frequencies.keys():
#                         word_frequencies[word] = 1
#                     else:
#                         word_frequencies[word] += 1

#         # Compute puntuation
#         maximum_frequncy = max(word_frequencies.values())
#         for word in word_frequencies.keys():
#             word_frequencies[word] = word_frequencies[word] / maximum_frequncy

#         # Scores
#         abstracts["sentence_scores"] = 0
#         for index, row in abstracts.iterrows():
#             for word in nltk.word_tokenize(row["formatted_text"]):
#                 word = porter_stemmer.stem(word)
#                 if word in word_frequencies.keys():
#                     abstracts.at[index, "sentence_scores"] += word_frequencies[word]

#         # Select main phrases
#         abstracts = abstracts.sort_values(by=["sentence_scores"], ascending=False)
#         abstracts = abstracts.head(n_phrases)
#         abstracts["text"] = abstracts.text.str.capitalize()

#         for text in expanded_keywords:
#             abstracts["text"] = abstracts["text"].str.replace(
#                 text, text.upper(), regex=False
#             )
#             abstracts["text"] = abstracts["text"].str.replace(
#                 text.capitalize(), text.upper(), regex=False
#             )

#         return abstracts

#     def save_summary(abstracts, sufix):
#         with open(
#             join(directory, f"abstract_summarization{sufix}.txt"), "w"
#         ) as out_file:
#             for _, row in abstracts.iterrows():
#                 paragraph = textwrap.fill(
#                     row["text"],
#                     width=90,
#                 )
#                 document_id = documents[
#                     documents.record_no == row["record_no"]
#                 ].document_id
#                 document_id = document_id.iloc[0]
#                 print("*** " + document_id, file=out_file)
#                 print(paragraph, file=out_file)
#                 print("\n", file=out_file)

#     def write_report(documents, abstracts, sufix):

#         # ----< select columns to report >-----------------------------------------------
#         documents = documents.copy()
#         column_list = []
#         reported_columns = [
#             "title",
#             "authors",
#             "global_citations",
#             "source_title",
#             "year",
#             "abstract",
#         ]
#         for column in reported_columns:
#             if column in documents.columns:
#                 column_list.append(column)
#         documents = documents[column_list + ["record_no"]]

#         # ----< select documents >-------------------------------------------------------
#         records_no = abstracts.record_no.drop_duplicates().tolist()

#         documents = documents[documents.record_no.isin(records_no)]
#         if "global_citations" in documents.columns:
#             documents = documents.sort_values(by="global_citations", ascending=False)

#         # ----< report >-----------------------------------------------------------------
#         with open(
#             join(directory, f"abstract_summarization{sufix}.txt"), "w"
#         ) as out_file:

#             for index, row in documents.iterrows():

#                 for column in reported_columns:

#                     if column not in row.index:
#                         continue

#                     if column == "title":
#                         print("      title :", end="", file=out_file)
#                         print(
#                             textwrap.fill(
#                                 row[column],
#                                 width=115,
#                                 initial_indent=" " * 23,
#                                 subsequent_indent=" " * 23,
#                                 fix_sentence_endings=True,
#                             )[22:],
#                             file=out_file,
#                         )
#                         continue

#                     if column == "abstract":
#                         print("            abstract :", end="", file=out_file)
#                         print(
#                             textwrap.fill(
#                                 row[column],
#                                 width=115,
#                                 initial_indent=" " * 23,
#                                 subsequent_indent=" " * 23,
#                                 fix_sentence_endings=True,
#                             )[22:],
#                             file=out_file,
#                         )
#                         continue

#                     if column in [
#                         "raw_author_keywords",
#                         "author_keywords",
#                         "raw_index_keywords",
#                         "index_keywords",
#                     ]:
#                         keywords = row[column]
#                         if pd.isna(keywords):
#                             continue
#                         keywords = keywords.split("; ")
#                         print(" {:>19} : {}".format(column, keywords[0]), file=out_file)
#                         for keyword in keywords[1:]:
#                             print(" " * 23 + keyword, file=out_file)
#                         continue

#                     print(" {:>19} : {}".format(column, row[column]), file=out_file)

#                 if index != documents.index[-1]:
#                     print(
#                         "-" * 120,
#                         file=out_file,
#                     )

#     # ----< data must be a list >--------------------------------------------------------
#     if isinstance(keywords, str):
#         keywords = [keywords]
#     keywords = [word for word in keywords if word != ""]

#     documents = read_filtered_records(directory)

#     expanded_keywords = expand_keywords(keywords)
#     documents_id = select_documents(documents, column, expanded_keywords)
#     abstracts = load_abstracts(documents_id, expanded_keywords)
#     abstracts = summarize(abstracts, expanded_keywords)

#     write_report(documents, abstracts, sufix)
#     # save_summary(abstracts, sufix)

#     # -----------------------------------------------------------------------------------
#     # summary = ".. ".join(abstracts.text.values)
#     # print(textwrap.fill(summary, width=90))
#     print("Done!")