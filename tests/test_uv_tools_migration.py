import shutil

import pytest

from helpers import get_fixture_data
from uv_tools_migration import UVToolsMigration


class TestUVToolsMigration:
    @pytest.mark.parametrize("mock_from_dir,mock_expected_dir", [
        ("full_data", 'full_data'),
        ("no_dev_packages", 'no_dev_packages'),
        ("no_packages", 'no_packages'),
        ("no_equals_version_in_packages", 'full_data'),
        ("no_equals_version_in_dev_packages", 'full_data'),
        ("no_equals_version_in_dev_and_packages", 'full_data'),
    ])
    def test_ok(self, tmp_path, mock_from_dir, mock_expected_dir):
        from_file = f'./tests/fixtures/uv_tools_migration/{mock_from_dir}/Pipfile'
        to_file = shutil.copy2('./tests/fixtures/pyproject.toml', tmp_path)

        uv_tools_migration = UVToolsMigration(from_file, to_file)
        uv_tools_migration.process()

        expected_file = f'./tests/fixtures/uv_tools_migration/{mock_expected_dir}/pyproject.toml'
        assert get_fixture_data(to_file) == get_fixture_data(expected_file)

    def test_no_dev_and_packages(self, tmp_path):
        from_file = './tests/fixtures/uv_tools_migration/no_dev_and_packages/Pipfile'
        to_file = tmp_path / 'pyproject.toml'

        uv_tools_migration = UVToolsMigration(from_file, to_file)
        with pytest.raises(ValueError) as e:
            uv_tools_migration.process()

        assert str(e.value) == f'Pipfile have no dev-packages and packages: {from_file}'

    def test_no_git(self, tmp_path):
        from_file = './tests/fixtures/uv_tools_migration/no_git/Pipfile'
        to_file = tmp_path / 'pyproject.toml'

        uv_tools_migration = UVToolsMigration(from_file, to_file)
        with pytest.raises(ValueError) as e:
            uv_tools_migration.process()

        expected_json = {
            'scr': 'https://github.com/itcrab/django-timed-tests.git',
            'ref': 'feature/store-report-into-file',
            'editable': True
        }
        assert str(e.value) == f'Pipfile have no `git` link to the repository in this case: {expected_json}'
