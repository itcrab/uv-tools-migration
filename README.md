![GitHub Actions CI](https://github.com/itcrab/uv-tools-migration/actions/workflows/python-package-ci.yml/badge.svg)

# uv-tools-migration

Migrate any projects from `pipenv` to `uv` without pain.

### Examples

You must have already `uv init` repo with `pyproject.toml` file.
Sample `app.py` you can use like this:
```Python
from uv_tools_migration import UVToolsMigration

uv_tools_migration = UVToolsMigration(
    from_file='./.examples/Pipfile',
    to_file='./.examples/pyproject.toml',
)
uv_tools_migration.process()
```

Run `app.py` for got packages from your `Pipfile` into `pyproject.toml`:
```Bash
uv run app.py
```

Run tests in terminal:
```Bash
uv run -m pytest -s
```

Run linters in terminal:
```Bash
uv run mypy .
uv run ruff check
```

Have a nice days!
