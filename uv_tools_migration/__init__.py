import tomllib

import tomli_w


class UVToolsMigration:
    """
    UVToolsMigration is tool for migration from `pipenv` to `uv`
    """

    def __init__(self, from_file, to_file, with_dev_packages):
        self.from_file = from_file
        self.to_file = to_file

        self.packages_types = ('packages',)
        if with_dev_packages:
            self.packages_types = ('dev-packages', 'packages')

    def process(self):
        pipenv_data = self._get_pipenv_data()
        packages_list, sources_str = self._generate_packages_list_and_sources_str(pipenv_data)
        self._generate_packages_into_uv_file(packages_list, sources_str)

    def _get_pipenv_data(self):
        with open(self.from_file, 'rb') as f:
            return tomllib.load(f)

    def _generate_packages_list_and_sources_str(self, pipenv_data):
        """
        uv packages list example:
        ```pyproject.toml
        ...
        dependencies = [
            "django>=5.2.2",
            "djangorestframework>=3.16.0",
            "lxml>=5.4.0",
            "django-timed-tests",
        ]
        ...
        [tool.uv.sources]
        django-timed-tests = { git = "https://github.com/itcrab/django-timed-tests", rev = "feature/store-report-into-file" }
        ```
        """
        packages_list = []
        sources_str = ''
        for packages_type in self.packages_types:
            for package, version in pipenv_data[packages_type].items():
                if isinstance(version, str):
                    if version[0].isdigit():  # for case like: python-package = "1.0.2"
                        version = f'=={version}'

                    packages_list.append(f'{package}{version}')
                elif isinstance(version, dict):
                    if 'git' not in version:
                        continue
                    elif 'ref' in version:
                        version['rev'] = version.pop('ref')

                    package_name = version['git'].split('/')[-1].replace('.git', '')
                    packages_list.append(package_name)

                    sources_str += f'{package_name} = {{ '
                    for key in version:
                        if key == 'editable':
                            continue
                        sources_str += f'{key} = "{version[key]}", '
                    sources_str = sources_str[:-2]
                    sources_str += ' }\n'

        packages_list.sort()

        return packages_list, sources_str

    def _generate_packages_into_uv_file(self, packages_list, sources_str):
        with open(self.to_file, 'rb') as f:
            uv_data = tomllib.load(f)

        uv_data['project']['dependencies'] = packages_list

        uv_data_toml = tomli_w.dumps(uv_data)
        uv_data_toml += f'\n[tool.uv.sources]\n{sources_str}'

        with open(self.to_file, "w") as f:
            f.write(uv_data_toml)
