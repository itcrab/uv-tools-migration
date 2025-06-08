from uv_tools_migration import UVToolsMigration

uv_tools_migration = UVToolsMigration(
    from_file='./.examples/Pipfile',
    to_file='./.examples/pyproject.toml',
)
uv_tools_migration.process()
