from jinja2 import Template
from .templates import HtmlTemplates

class HtmlTemplateService:
    
    def __init__(self, template:HtmlTemplates, data:dict[str, str]):
        self.template = template
        self.data = data
    
    def load_template(self):
        with open(self.template) as file_:
            template = Template(file_.read())

        html_string = template.render(self.data)
        return html_string