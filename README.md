# sopel-reddit

A reddit plugin for Sopel IRC bots.


## Installation

**Stable version:**

```sh
pip install sopel-reddit
```

### From source

```sh
pip install -e path/to/sopel-reddit

# optional: for development
pip install -r dev-requirements.txt
```

_Note: Running the test suite with `pytest -v tests/` requires both
`sopel-reddit` **and `sopel` itself** to be installed in the same venv._


## Configuration

```ini
[reddit]
slash_info = True
# Allow expansion of inline references like `u/RandomRedditor` or `r/eyebleach`
# (links are always expanded)
```


## Special thanks

All contributors to [the original `reddit` plugin for
Sopel](https://github.com/sopel-irc/sopel/commits/master/sopel/modules/reddit.py).
