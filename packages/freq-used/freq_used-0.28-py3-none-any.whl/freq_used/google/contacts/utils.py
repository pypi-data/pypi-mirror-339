"""
util functions for Google Contacts
"""


def get_label_str(*label_list: str) -> str:
    return " ::: ".join(list(label_list) + ["* myContacts"])


def is_home_email(email: str) -> bool:
    return (
        "gmail.com" in email
        or "yahoo.com" in email
        or "yahoo.co.kr" in email
        or "hotmail.com" in email
        or "naver.com" in email
        or "hanmail.net" in email
        or "daum.net" in email
        or "bawi.org" in email
        or "empal.com" in email
    )
