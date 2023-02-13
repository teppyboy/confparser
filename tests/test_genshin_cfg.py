from pathlib import Path

import inicfp

default_gi = {
    "General": {
        "channel": "1",
        "cps": "mihoyo",
        "game_version": "3.3.0",
        "sdk_version": "",
        "sub_channel": "0",
    }
}

default_gi_str = """
[General]
channel = 1
cps = mihoyo
game_version = 3.3.0
sdk_version =
sub_channel = 0
""".strip()

gi_modified_str = """
[General]
channel = 1
cps = mihoyo
game_version = 6.2.0
sdk_version =
sub_channel = 0
best_waifu = Lumine
""".strip()


def parse_ok(ini: dict) -> bool:
    for v in ini.keys():
        if v.startswith("__PARSE_FAILURE"):
            return False
    return True


def test_load():
    ini = inicfp.load(
        Path("./tests/conf/genshin-config.ini").open(), comments=False, whitespace=False
    )
    assert ini == default_gi


def test_loads():
    ini = inicfp.loads(
        Path("./tests/conf/genshin-config.ini").read_text(),
        comments=False,
        whitespace=False,
    )
    assert ini == default_gi


def test_load_preserve():
    ini = inicfp.load(Path("./tests/conf/genshin-config.ini").open())
    assert parse_ok(ini)


def test_loads_preserve():
    ini = inicfp.loads(Path("./tests/conf/genshin-config.ini").read_text())
    assert parse_ok(ini)


def test_dumps():
    dumped = inicfp.dumps(default_gi, comments=False, whitespace=False)
    assert dumped.strip() == default_gi_str


def test_loads_dumps():
    ini = inicfp.loads(
        Path("./tests/conf/genshin-config.ini").read_text(),
        comments=False,
        whitespace=False,
    )
    dumped = inicfp.dumps(ini, comments=False)
    assert dumped.strip() == default_gi_str


def test_loads_preserve_dumps():
    ini = inicfp.loads(
        Path("./tests/conf/genshin-config.ini").read_text(), comments=True
    )
    dumped = inicfp.dumps(ini, comments=False)
    assert dumped.strip() == default_gi_str


def test_loads_edit_dumps():
    ini = inicfp.loads(
        Path("./tests/conf/genshin-config.ini").read_text(),
        comments=False,
        whitespace=False,
    )
    # Random number dude
    ini["General"]["game_version"] = "6.2.0"
    ini["General"]["best_waifu"] = "Lumine"
    dumped = inicfp.dumps(ini, comments=False)
    assert dumped.strip() == gi_modified_str
