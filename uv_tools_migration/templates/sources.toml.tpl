
[tool.uv.sources]
{% for package_name, version in sources %}{#
#}{{ package_name }} = { {% for key, value in version.items() %}{{ key }} = "{{ value }}"{% if not loop.last %}, {% endif %}{% endfor %} }
{% endfor %}
