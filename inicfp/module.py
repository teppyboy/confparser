from io import IOBase
from ast import literal_eval

__all__ = ["load", "loads", "dump", "dumps"]


def load(
    fp: IOBase, comments: bool = False, whitespace: bool = False, errors="ignore"
) -> dict:
    return loads(fp.read(), comments=comments, whitespace=whitespace, errors=errors)


def loads(
    conf: str, comments: bool = False, whitespace: bool = False, errors="ignore"
) -> dict:
    parsed: dict = {}
    lines: list[str] = conf.splitlines()
    ignore: set[int] = set()
    current: dict = parsed
    for index, line in enumerate(lines):
        if index in ignore:
            continue
        line = line.strip()
        # Whitespace
        if line == "":
            if whitespace:
                current["__WHITESPACE_" + str(index)] = None
            continue
        # Comment
        if line.startswith("#"):
            if line.startswith("# __PARSE_ERROR"):
                current["__PARSE_ERROR_" + str(index)] = line[
                    len("# __PARSE_ERROR: ") :
                ]
                continue
            if comments:
                current["__COMMENT_" + str(index)] = line[1:]
            continue
        # ini comment
        if line.startswith(";"):
            if comments:
                current["__INI_COMMENT_" + str(index)] = line[1:]
            continue
        # Section
        if line.startswith("[") and line.endswith("]"):
            cur = {}
            section_name = line[1:-1].strip()
            if "." not in line:
                current = cur
                parsed[section_name] = current
                continue
            # Subsection
            trees = section_name.split(".")
            # Relative
            if section_name.startswith("."):
                cur_parent = current
            else:
                cur_parent = parsed
            for parent in trees:
                if parent == "":
                    continue
                if not cur_parent.get(parent):
                    cur_parent[parent] = {}
                cur_parent = cur_parent[parent]
            current = cur_parent
            continue
        # Keys
        line_split = []
        for spliter in ["=", ":", " "]:
            line_split = line.split(spliter, 1)
            if len(line_split) == 1:
                continue
            break
        # Keys with no values
        if len(line_split) == 1:
            current[line_split[0].strip()] = None
            continue
        indicator, comment = None, None
        try:
            var, val = line_split
            # Inline comments
            try:
                if " #" in val:
                    val, comment = val.split(" #", 1)
                    if comments:
                        indicator = "__INLINE_COMMENT_" + str(index)
                elif " ;" in val:
                    val, comment = val.split(" ;", 1)
                    if comments:
                        indicator = "__INLINE_INI_COMMENT_" + str(index)
            except ValueError:
                pass
            val = val.strip()
            # Multiple line value (triggered by quotes)
            for quote in ['"', "'"]:
                if not val.startswith(quote):
                    continue
                val = val[1:]
                cur_line = ""
                cur_idx = index + 1
                while not cur_line.endswith(quote):
                    if cur_idx >= len(lines):
                        col = line.find(quote)
                        raise ValueError(
                            f"Unterminated string starting at: line {index + 1} column {col + 1} (char {col})"
                        )
                    val += cur_line + "\n"
                    cur_line = lines[cur_idx]
                    ignore.add(cur_idx)
                    cur_idx += 1
                val += cur_line[:-1]
                break
        except ValueError as e:
            if errors == "ignore":
                current["__PARSE_ERROR_" + str(index)] = e
                continue
            raise
        try:
            val = literal_eval(val)
        except Exception:
            pass
        current[var.strip()] = val
        if indicator:
            current[indicator] = comment
    return parsed


def dump(
    obj,
    fp: IOBase,
    comments: bool = True,
    whitespace: bool = True,
    comment_type: str = "conf",
):
    fp.write(
        dumps(
            obj=obj, comments=comments, whitespace=whitespace, comment_type=comment_type
        )
    )


def dumps(
    obj: dict,
    comments: bool = True,
    whitespace: bool = True,
    comment_type: str = "conf",
    parent: str = "",
) -> str:
    if not parent:
        parent = ""
    else:
        parent += "."
    string = ""
    for key, value in obj.items():
        if key.startswith("__PARSE_ERROR_"):
            if comments:
                if comment_type == "conf":
                    string += f"# __PARSE_ERROR: {str(value)}\n"
                elif comment_type == "ini":
                    string += f"; __PARSE_ERROR: {str(value)}\n"
            continue
        if key.startswith("__WHITESPACE_"):
            if whitespace:
                string += "\n"
            continue
        if key.startswith("__INI_COMMENT_"):
            if comments:
                string += f";{value}\n"
            continue
        if key.startswith("__COMMENT_"):
            if comments:
                string += f"#{value}\n"
            continue
        if key.startswith("__INLINE_INI_COMMENT_"):
            if comments:
                string = string[:-1] + f" ;{value}\n"
            continue
        if key.startswith("__INLINE_COMMENT_"):
            if comments:
                string = string[:-1] + f" #{value}\n"
            continue
        if isinstance(value, dict):
            # No need last \n as dumps did for us already
            val = dumps(
                obj=value,
                comments=comments,
                whitespace=whitespace,
                comment_type=comment_type,
                parent=parent + key,
            )
            string += f"[{parent + key}]\n{val}"
            continue
        if value is None and key != "":
            string += f"{key}\n"
            continue
        string += f"{key} = {value}".strip() + "\n"
    return string
