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
        if 'dev-packages' not in pipenv_data and 'packages' not in pipenv_data:
            raise ValueError(f'Pipfile have no dev-packages and packages: {self.from_file}')

        packages_data = self._generate_packages_data(pipenv_data)
        self._generate_packages_into_uv_file(packages_data)

    def _get_pipenv_data(self):
        with open(self.from_file, 'rb') as f:
            return tomllib.load(f)

    def _generate_packages_data(self, pipenv_data):
        """
        uv packages list example:
        ```pyproject.toml
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
        ```
        """
        packages_data = {'dev-packages': [], 'packages': [], 'sources': ''}
        for packages_type in self.packages_types:
            if packages_type not in pipenv_data:
                continue

            for package, version in pipenv_data[packages_type].items():
                if isinstance(version, str):
                    if version[0].isdigit():  # for case like: python-package = "1.0.2"
                        version = f'=={version}'

                    packages_data[packages_type].append(f'{package}{version}')
                elif isinstance(version, dict):
                    if 'git' not in version:
                        continue
                    elif 'ref' in version:
                        version['rev'] = version.pop('ref')

                    package_name = version['git'].split('/')[-1].replace('.git', '')
                    packages_data[packages_type].append(package_name)

                    packages_data['sources'] += f'{package_name} = {{ '
                    for key in version:
                        if key == 'editable':
                            continue
                        packages_data['sources'] += f'{key} = "{version[key]}", '
                    packages_data['sources'] = packages_data['sources'][:-2]
                    packages_data['sources'] += ' }\n'

            packages_data[packages_type].sort()

        return packages_data

    def _generate_packages_into_uv_file(self, packages_data):
        with open(self.to_file, 'rb') as f:
            uv_data = tomllib.load(f)

        uv_data['project']['dependencies'] = packages_data['packages']
        if packages_data['dev-packages']:
            uv_data['dependency-groups'] = {'dev': packages_data['dev-packages']}

        uv_data_toml = tomli_w.dumps(uv_data)
        if packages_data["sources"]:
            uv_data_toml += f'\n[tool.uv.sources]\n{packages_data["sources"]}'

        with open(self.to_file, "w") as f:
            f.write(uv_data_toml)
