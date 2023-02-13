# confparser

Very simple .ini-like text parser (supports pacman.conf & basic ini, etc.)

## About

This implements `.ini` as described in [Wikipedia](https://en.wikipedia.org/wiki/INI_file), including support for all standard features and some extended features:

+ Name/value delimiter (`=`, `:` and whitespace)
+ Number sign as comments
+ Inline comments
+ Quoted values
+ Multi-line values (supported when using quoted values)

## Usage

```python
import inicfp
parsed: dict = inicfp.load(open("./tests/conf/genshin-config.ini"), comments=False, whitespace=False)
# Tada, you've just parsed a .ini file to a dict
```

## Installation

### Run from source

Assuming you have poetry installed:

```bash
git clone https://github.com/teppyboy/inicfp
cd inicfp
poetry install
poetry shell # Needed to use inicfg
```

## Documentation

soon:tm:

## Running tests

This project uses [pytest](pytest.org) to do unit tests, to run tests simply execute `pytest`


## License

[MIT License](LICENSE)
