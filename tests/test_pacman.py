from pathlib import Path

import confparser

default_pacman = {
    'options': {
        'HoldPkg': 'pacman glibc', 
        'Architecture': 'auto', 
        'CheckSpace': None, 
        'SigLevel': 'Required DatabaseOptional', 
        'LocalFileSigLevel': 'Optional'
    }, 
    'core': {
        'Include': '/etc/pacman.d/mirrorlist'
    }, 
    'extra': {
        'Include': '/etc/pacman.d/mirrorlist'
    }, 
    'community': {
        'Include': '/etc/pacman.d/mirrorlist'
    }
}

default_pacman_str = """
[options]
HoldPkg = pacman glibc
Architecture = auto
CheckSpace
SigLevel = Required DatabaseOptional
LocalFileSigLevel = Optional
[core]
Include = /etc/pacman.d/mirrorlist
[extra]
Include = /etc/pacman.d/mirrorlist
[community]
Include = /etc/pacman.d/mirrorlist
""".strip()

pacman_multlib_str = """
[options]
HoldPkg = pacman glibc
Architecture = auto
CheckSpace
SigLevel = Required DatabaseOptional
LocalFileSigLevel = Optional
[core]
Include = /etc/pacman.d/mirrorlist
[extra]
Include = /etc/pacman.d/mirrorlist
[community]
Include = /etc/pacman.d/mirrorlist
[multilib]
Include = /etc/pacman.d/mirrorlist
""".strip()

def parse_ok(ini: dict) -> bool:
    for v in ini.keys():
        if v.startswith("__PARSE_FAILURE__"):
            return False
    return True

def test_load():
    ini = confparser.load("./tests/conf/pacman.conf", preserve_comments=False)
    assert ini == default_pacman

def test_loads():
    ini = confparser.loads(Path("./tests/conf/pacman.conf").read_text(), preserve_comments=False)
    assert ini == default_pacman

def test_load_preserve():
    ini = confparser.load("./tests/conf/pacman.conf")
    assert parse_ok(ini)

def test_loads_preserve():
    ini = confparser.loads(Path("./tests/conf/pacman.conf").read_text())
    assert parse_ok(ini)

def test_dumps():
    dumped = confparser.dumps(default_pacman, preserve_comments=False)
    assert dumped.strip() == default_pacman_str

def test_loads_dumps():
    ini = confparser.loads(Path("./tests/conf/pacman.conf").read_text(), preserve_comments=False)
    dumped = confparser.dumps(ini, preserve_comments=False)
    assert dumped.strip() == default_pacman_str

def test_loads_preserve_dumps():
    ini = confparser.loads(Path("./tests/conf/pacman.conf").read_text(), preserve_comments=True)
    dumped = confparser.dumps(ini, preserve_comments=False)
    assert dumped.strip() == default_pacman_str

def test_loads_edit_dumps():
    ini = confparser.loads(Path("./tests/conf/pacman.conf").read_text(), preserve_comments=False)
    ini["multilib"] = {
        "Include": "/etc/pacman.d/mirrorlist"
    }
    dumped = confparser.dumps(ini, preserve_comments=False)
    assert dumped.strip() == pacman_multlib_str
