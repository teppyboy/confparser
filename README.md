# confparser

Very simple .ini-like text parser (supports pacman.conf & basic ini, etc.)

## Usage

```python
import confparser
parsed: dict = confparser.load("./tests/conf/genshin-config.ini", preserve_comments=False)
# Tada, you've just parsed a .ini file to a dict
```

## Documentation

soon:tm:

## Running tests

This project uses [pytest](pytest.org) to do unit tests, to run tests simply execute:

```bash
pytest
```

## License

[MIT License](LICENSE)