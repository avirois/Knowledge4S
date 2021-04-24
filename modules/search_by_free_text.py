"""
Search by free module.

"""
import os

STORAGE = "storage"


def oreder_by__containing_freetext(freetext, ids):
    ids = [str(id_) for id_ in ids]
    ordered = []
    search_strings = freetext.split(" ")
    directory = os.listdir(STORAGE)
    files = [file for file in directory if file.split(".txt")[0] in ids]
    for sstring in search_strings:
        for fname in files:
            if os.path.isfile(STORAGE + os.sep + fname):
                with open(STORAGE + os.sep + fname, "r") as f:
                    for line in f:
                        if sstring in line.lower():
                            ordered.append(fname.split(".txt")[0])
                            break
    return ordered + [id_ for id_ in ids if id_ not in ordered]
