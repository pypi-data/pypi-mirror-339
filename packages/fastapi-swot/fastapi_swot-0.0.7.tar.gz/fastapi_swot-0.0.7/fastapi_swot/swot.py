import os
import pathlib
from typing import List, Optional, Set


class SWOT:
    tlds = None
    stoplist = None

    @staticmethod
    def read_list(resource: str) -> Optional[Set[str]]:
        base_path = (
            f"{pathlib.Path(os.path.abspath(os.path.dirname(__file__)))}/domains"
        )
        file_path = f"{base_path}/{resource}"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return set(line.strip() for line in f)
        return None

    tlds = read_list("tlds.txt")
    if tlds is None:
        raise FileNotFoundError("Cannot find tlds.txt")

    stoplist = read_list("stoplist.txt")
    if stoplist is None:
        raise FileNotFoundError("Cannot find stoplist.txt")


def is_under_tld(parts: List[str]) -> bool:
    return check_set(SWOT.tlds, parts)


def is_stoplisted(parts: List[str]) -> bool:
    return check_set(SWOT.stoplist, parts)


def check_set(set_: Set[str], parts: List[str]) -> bool:
    subj = ""
    for part in parts:
        subj = f"{part}{subj}"
        if subj in set_:
            return True
        subj = f".{subj}"
    return False


def is_academic(email: str) -> bool:
    parts = domain_parts(email)
    return not is_stoplisted(parts) and (
        is_under_tld(parts) or bool(find_school_names(email))
    )


def find_school_names(email_or_domain: str) -> List[str]:
    return find_school_names_from_parts(domain_parts(email_or_domain))


def find_school_names_from_parts(parts: List[str]) -> List[str]:
    resource_path = ""
    for part in parts:
        resource_path = f"{resource_path}/{part}"
        school = SWOT.read_list(f'{resource_path.lstrip("/")}.txt')
        if school is not None:
            return list(school)
    return []


def domain_parts(email_or_domain: str) -> List[str]:
    cleaned = email_or_domain.strip().lower()
    after_at = cleaned.split("@")[-1]
    after_protocol = after_at.split("://")[-1]
    before_port = after_protocol.split(":")[0]
    return before_port.split(".")[::-1]  # reversed
