from pathlib import Path

import inicfp

default_pacman = {
    "options": {
        "HoldPkg": "pacman glibc",
        "Architecture": "auto",
        "CheckSpace": None,
        "SigLevel": "Required DatabaseOptional",
        "LocalFileSigLevel": "Optional",
    },
    "core": {"Include": "/etc/pacman.d/mirrorlist"},
    "extra": {"Include": "/etc/pacman.d/mirrorlist"},
    "community": {"Include": "/etc/pacman.d/mirrorlist"},
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
        if v.startswith("__PARSE_FAILURE"):
            return False
    return True


def test_load():
    ini = inicfp.load(
        Path("./tests/conf/pacman.conf").open(), comments=False, whitespace=False
    )
    assert ini == default_pacman


def test_loads():
    ini = inicfp.loads(
        Path("./tests/conf/pacman.conf").read_text(), comments=False, whitespace=False
    )
    assert ini == default_pacman


def test_load_preserve():
    ini = inicfp.load(Path("./tests/conf/pacman.conf").open())
    assert parse_ok(ini)


def test_loads_preserve():
    ini = inicfp.loads(Path("./tests/conf/pacman.conf").read_text())
    assert parse_ok(ini)


def test_dumps():
    dumped = inicfp.dumps(default_pacman, comments=False, whitespace=False)
    assert dumped.strip() == default_pacman_str


def test_loads_dumps():
    ini = inicfp.loads(
        Path("./tests/conf/pacman.conf").read_text(), comments=False, whitespace=False
    )
    dumped = inicfp.dumps(ini, comments=False)
    assert dumped.strip() == default_pacman_str


def test_loads_preserve_dumps():
    ini = inicfp.loads(Path("./tests/conf/pacman.conf").read_text(), comments=True)
    dumped = inicfp.dumps(ini, comments=False, whitespace=False)
    assert dumped.strip() == default_pacman_str


def test_loads_edit_dumps():
    ini = inicfp.loads(
        Path("./tests/conf/pacman.conf").read_text(), comments=False, whitespace=False
    )
    ini["multilib"] = {"Include": "/etc/pacman.d/mirrorlist"}
    dumped = inicfp.dumps(ini, comments=False)
    assert dumped.strip() == pacman_multlib_str
