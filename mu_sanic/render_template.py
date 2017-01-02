from jinja2 import Environment, PackageLoader
from sanic.response import html
from .config import your_app , your_app_template

app_env = Environment(loader = PackageLoader(your_app,your_app_template))

def _render(template,context):
    html_template = app_env.get_template(str(template))
    html_content = html_template.render(context)
    return html_content

def render_template(template,**context):
    content = _render(template,context)
    return html(content)
    


