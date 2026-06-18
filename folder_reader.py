# def read_txt_file(path: str) -> list[str]:
#     with open(path, "r", encoding="utf-8") as f:
#         return [line.strip() for line in f if line.strip()]


# import os
# from typing import Dict


# def read_txt_folder(folder_path: str) -> Dict[str, str]:
#     """
#     Reads all .txt files from a folder.
#     Returns: { filename: file_content }
#     """
#     data = {}

#     for file_name in os.listdir(folder_path):
#         if not file_name.lower().endswith(".txt"):
#             continue

#         full_path = os.path.join(folder_path, file_name)

#         if not os.path.isfile(full_path):
#             continue

#         with open(full_path, "r", encoding="utf-8") as f:
#             content = f.read().strip()

#             if content:
#                 data[file_name] = content

#     return data


import os
import re
from typing import Dict


def read_txt_folder(folder_path: str) -> Dict[str, Dict[str, str]]:
    """
    Reads all .txt files from a folder and extracts TITLE and ABSTRACT.

    Returns:
        {
            filename: {
                "title": "...",
                "abstract": "..."
            }
        }
    """
    data: Dict[str, Dict[str, str]] = {}

    title_pattern = re.compile(
        r"TITLE\s*(.*?)\s*(?:ABSTRACT|CLAIMS|$)",
        re.DOTALL | re.IGNORECASE
    )
    abstract_pattern = re.compile(
        r"ABSTRACT\s*(.*?)\s*(?:CLAIMS|$)",
        re.DOTALL | re.IGNORECASE
    )

    for file_name in os.listdir(folder_path):
        if not file_name.lower().endswith(".txt"):
            continue

        full_path = os.path.join(folder_path, file_name)
        if not os.path.isfile(full_path):
            continue

        with open(full_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            if not text:
                continue

            title_match = title_pattern.search(text)
            abstract_match = abstract_pattern.search(text)

            sections = {}

            if title_match:
                sections["title"] = title_match.group(1).strip()

            if abstract_match:
                sections["abstract"] = abstract_match.group(1).strip()

            if sections:
                data[file_name] = sections

    return data

