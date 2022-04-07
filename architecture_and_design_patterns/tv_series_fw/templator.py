from jinja2 import Template
import os


def render(template_name, template_folder='templates', **kwargs):
    path = os.path.join(template_folder, template_name)

    with open(path, encoding='utf-8') as file:
        template = Template(file.read())

    return template.render(**kwargs)
