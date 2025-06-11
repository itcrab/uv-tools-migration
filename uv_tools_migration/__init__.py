import tomllib

import tomli_w

from uv_tools_migration.renders import SourcesTomlRender


class UVToolsMigration:
    """
    UVToolsMigration is tool for migration from `pipenv` to `uv`
    """

    def __init__(self, from_file: str, to_file: str) -> None:
        self.from_file = from_file
        self.to_file = to_file

        self.packages_types = ('dev-packages', 'packages')

    def process(self) -> None:
        pipenv_data = self._get_pipenv_data(self.from_file)
        if 'dev-packages' not in pipenv_data and 'packages' not in pipenv_data:
            raise ValueError(f'Pipfile have no dev-packages and packages: {self.from_file}')

        packages_data = self._generate_packages_data(pipenv_data)
        self._generate_packages_into_uv_file(packages_data)

    def _get_pipenv_data(self, file_path: str) -> dict:
        with open(file_path, 'rb') as f:
            return tomllib.load(f)

    def _generate_packages_data(self, pipenv_data: dict) -> dict[str, list[str | tuple[str, dict]]]:
        """
        uv packages list example:
        ```pyproject.toml
        ...
        [project]
        ...
        dependencies = [
            "django==5.2.2",
            "djangorestframework==3.16.0",
            "lxml==5.4.0",
        ]
        ...
        [dependency-groups]
        dev = [
            "django-debug-toolbar==5.2.0",
            "django-timed-tests",
        ]
        ...
        [tool.uv.sources]
        django-timed-tests = { git = "https://github.com/itcrab/django-timed-tests", rev = "feature/store-report-into-file" }
        ...
        ```
        """
        packages_data: dict[str, list[str | tuple[str, dict]]] = {'dev-packages': [], 'packages': [], 'sources': []}
        for packages_type in self.packages_types:
            if packages_type not in pipenv_data:
                continue

            for package_name, version in pipenv_data[packages_type].items():
                if isinstance(version, str):
                    if version[0].isdigit():  # for case like: python-package = "1.0.2"
                        version = f'=={version}'

                    packages_data[packages_type].append(f'{package_name}{version}')
                elif isinstance(version, dict):
                    packages_data[packages_type].append(package_name)

                    packages_data['sources'].append((package_name, version))

            packages_data[packages_type].sort()

        return packages_data

    def _generate_packages_into_uv_file(self, packages_data: dict) -> None:
        source_render = SourcesTomlRender(packages_data['sources'])

        uv_data = self._get_pipenv_data(self.to_file)
        uv_data['project']['dependencies'] = packages_data['packages']
        if packages_data['dev-packages']:
            uv_data['dependency-groups'] = {'dev': packages_data['dev-packages']}

        with open(self.to_file, "w") as f:
            uv_data_toml = tomli_w.dumps(uv_data)
            f.write(uv_data_toml)

            if packages_data["sources"]:
                uv_sources_toml = source_render.render()
                f.write(uv_sources_toml)
