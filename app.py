from uv_tools_migration import UVToolsMigration

uv_tools_migration = UVToolsMigration(
    from_file='./.examples/Pipfile',
    to_file='./.examples/pyproject.toml',
    with_dev_packages=True,
)
uv_tools_migration.process()
