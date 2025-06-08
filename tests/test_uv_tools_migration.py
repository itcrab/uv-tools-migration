import shutil

import pytest

from tests.helpers import get_fixture_data
from uv_tools_migration import UVToolsMigration


class TestUVToolsMigration:
    @pytest.mark.parametrize("mock_from_file,mock_expected_file", [
        ("Pipfile", 'Pipfile_expected.toml'),
        ("Pipfile_no_dev_packages", 'Pipfile_no_dev_packages_expected.toml'),
        ("Pipfile_no_packages", 'Pipfile_no_packages_expected.toml'),
    ])
    def test_ok(self, tmp_path, mock_from_file, mock_expected_file):
        from_file = f'./tests/fixtures/{mock_from_file}'
        to_file = shutil.copy2('./tests/fixtures/pyproject.toml', tmp_path)

        uv_tools_migration = UVToolsMigration(from_file, to_file)
        uv_tools_migration.process()

        expected_file = f'./tests/fixtures/{mock_expected_file}'
        assert get_fixture_data(to_file) == get_fixture_data(expected_file)

    def test_no_dev_and_packages(self, tmp_path):
        from_file = './tests/fixtures/Pipfile_no_dev_and_packages'
        to_file = shutil.copy2('./tests/fixtures/pyproject.toml', tmp_path)

        uv_tools_migration = UVToolsMigration(from_file, to_file)
        with pytest.raises(ValueError) as e:
            uv_tools_migration.process()

        assert str(e.value) == f'Pipfile have no dev-packages and packages: {from_file}'
