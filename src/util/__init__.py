import unicodedata


def normalize_name(name: str) -> str:
    normalize_text = unicodedata.normalize("NFD", name)
    final_text = "".join(c for c in normalize_text if unicodedata.category(c) != "Mn")
    return final_text.lower()
