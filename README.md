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

app_id = abcdef0123456789
# Optional custom app ID for the reddit API
```

The `app_id` setting is provided mostly for future-proofing after [API policy
changes announced by Reddit Inc. in April
2023](https://old.reddit.com/r/reddit/comments/12qwagm/an_update_regarding_reddits_api/).
It exists so possible future API limitations can be worked around by users
without requiring a package update. **As of the time this package version was
published, the `app_id` setting _does not_ need to have a value.**


## Special thanks

All contributors to [the original `reddit` plugin for
Sopel](https://github.com/sopel-irc/sopel/commits/master/sopel/modules/reddit.py).
