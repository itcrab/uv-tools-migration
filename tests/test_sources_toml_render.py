from helpers import get_fixture_data
from uv_tools_migration import SourcesTomlRender


class TestSourcesTomlRender:
    def test_ok(self):
        sources_toml = SourcesTomlRender(sources=[
            ('django-timed-tests', {'git': "https://github.com/itcrab/django-timed-tests", 'rev': "feature/store-report-into-file"}),
        ]).render()

        expected_file = './tests/fixtures/sources_toml_render/ok/sources.toml'
        assert sources_toml == get_fixture_data(expected_file)

    def test_blank(self):
        sources_toml = SourcesTomlRender(sources=[]).render()
        assert sources_toml == ''
