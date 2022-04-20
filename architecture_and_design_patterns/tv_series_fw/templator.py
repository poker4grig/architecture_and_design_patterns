from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def render(template_name, template_folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(template_folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)


# import os
#
#
# def render(template_name, template_folder='templates', **kwargs):
#     path = os.path.join(template_folder, template_name)
#
#     with open(path, encoding='utf-8') as file:
#         template = Template(file.read())
#
#     return template.render(**kwargs)
