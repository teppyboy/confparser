from os import PathLike
from pathlib import Path


def load(file: PathLike, preserve_comments: bool = True) -> dict:
    return loads(Path(file).read_text(), preserve_comments=preserve_comments)


def loads(conf: str, preserve_comments: bool = True) -> dict:
    parsed: dict = {}
    lines: list[str] = conf.splitlines()
    ignore: list[int] = []
    current: dict = parsed
    for index, line in enumerate(lines):
        if index in ignore:
            continue
        line = line.strip()
        if line == "":
            if preserve_comments:
                current["__WHITESPACE__" + str(index)] = None
            continue
        if line.startswith("#"):
            if preserve_comments:
                current["__COMMENT__" + str(index)] = line[1:]
            continue
        if line.startswith(";"):
            if preserve_comments:
                current["__INI_COMMENT__" + str(index)] = line[1:]
            continue
        if line.startswith("[") and line.endswith("]"):
            current = {}
            parsed[line[1:-1].strip()] = current
            continue
        line_split = line.split("=")
        if len(line_split) == 1:
            current[line_split[0].strip()] = None
            continue
        try:
            var, val = line_split
        except ValueError as e:
            parsed["__PARSE_FAILURE__" + str(index)] = e
            pass
        current[var.strip()] = val.strip()
    return parsed


def dump(file: PathLike, conf: dict, preserve_comments: bool = True):
    Path(file).write_text(dumps(conf=conf, preserve_comments=preserve_comments))


def dumps(conf: dict, preserve_comments: bool = True) -> str:
    string = ""
    for key, value in conf.items():
        if key.startswith("__PARSE_FAILURE__"):
            if preserve_comments:
                string += f"# __PARSE_FAILURE__: {str(value)}\n"
            continue
        if key.startswith("__WHITESPACE__"):
            if preserve_comments:
                string += f"\n"
            continue
        if key.startswith("__COMMENT__"):
            if preserve_comments:
                string += f"#{value}\n"
            continue
        if key.startswith("__INI_COMMENT__"):
            if preserve_comments:
                string += f";{value}\n"
            continue
        if isinstance(value, dict):
            # No need last \n as dumps did for us already
            string += f"[{key}]\n{dumps(conf=value, preserve_comments=preserve_comments)}"
            continue
        if isinstance(value, str):
            string += f"{key} = {value}".strip() + "\n"
            continue
        if value is None and key != "":
            string += f"{key}\n"
            continue
    return string

