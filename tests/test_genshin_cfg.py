from pathlib import Path

import confparser

default_gi = {
    'General': {
        'channel': '1',
        'cps': 'mihoyo', 
        'game_version': '3.3.0', 
        'sdk_version': '', 
        'sub_channel': '0'
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
        if v.startswith("__PARSE_FAILURE__"):
            return False
    return True

def test_load():
    ini = confparser.load("./tests/conf/genshin-config.ini", preserve_comments=False)
    assert ini == default_gi

def test_loads():
    ini = confparser.loads(Path("./tests/conf/genshin-config.ini").read_text(), preserve_comments=False)
    assert ini == default_gi

def test_load_preserve():
    ini = confparser.load("./tests/conf/genshin-config.ini")
    assert parse_ok(ini)

def test_loads_preserve():
    ini = confparser.loads(Path("./tests/conf/genshin-config.ini").read_text())
    assert parse_ok(ini)

def test_dumps():
    dumped = confparser.dumps(default_gi, preserve_comments=False)
    assert dumped.strip() == default_gi_str

def test_loads_dumps():
    ini = confparser.loads(Path("./tests/conf/genshin-config.ini").read_text(), preserve_comments=False)
    dumped = confparser.dumps(ini, preserve_comments=False)
    assert dumped.strip() == default_gi_str

def test_loads_preserve_dumps():
    ini = confparser.loads(Path("./tests/conf/genshin-config.ini").read_text(), preserve_comments=True)
    dumped = confparser.dumps(ini, preserve_comments=False)
    assert dumped.strip() == default_gi_str

def test_loads_edit_dumps():
    ini = confparser.loads(Path("./tests/conf/genshin-config.ini").read_text(), preserve_comments=False)
    # Random number dude
    ini["General"]["game_version"] = "6.2.0"
    ini["General"]["best_waifu"] = "Lumine"
    dumped = confparser.dumps(ini, preserve_comments=False)
    assert dumped.strip() == gi_modified_str
