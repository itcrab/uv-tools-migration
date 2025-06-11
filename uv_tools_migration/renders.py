from pathlib import Path

import jinja2


class SourcesTomlRender:
    def __init__(self, sources):
        self.sources = sources

        self.base_path = Path(__file__).parent
        self.git_key = 'git'

        self._clean()

    def _validate_version(self, version):
        if self.git_key not in version:
            raise ValueError(f'Pipfile have no `git` link to the repository in this case: {version}')

    def _clean(self):
        for _, version in self.sources:
            self._validate_version(version)

            version.pop('editable', None)
            if 'ref' in version:
                version['rev'] = version.pop('ref')

    def _read_template(self):
        with open(f'{self.base_path}/templates/sources.toml.tpl', 'r') as f:
            return f.read()

    def render(self):
        if not self.sources:
            return ''

        return jinja2.Template(self._read_template()).render(sources=self.sources)
