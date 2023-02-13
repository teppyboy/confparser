def get_comments(obj) -> list[str] | None:
    comments = []
    for k, v in obj.items():
        if k.startswith("__COMMENT_") or k.startswith("__COMMENT_INI_"):
            comments.append(v)
    return comments or None


def get_parse_errors(obj) -> list[str] | None:
    parse_errors = []
    for k, v in obj.items():
        if k.startswith("__PARSE_ERROR_"):
            parse_errors.append(v)
    return parse_errors or None


def _remove(obj, remove: list[str]) -> dict:
    for k in obj.keys():
        for rm in remove:
            if k.startswith(rm):
                del obj[k]
    return obj


def remove_comments(obj) -> dict:
    _remove(obj, remove=["__COMMENT_", "__COMMENT_INI_"])


def remove_whitespace(obj) -> dict:
    _remove(obj, remove=["__WHITESPACE_"])


def remove_parse_errors(obj) -> dict:
    _remove(obj, remove=["__PARSE_ERROR_"])


def remove_all(obj) -> dict:
    _remove(
        obj, remove=["__COMMENT_", "__COMMENT_INI_", "__WHITESPACE_", "__PARSE_ERROR_"]
    )
