from flask import Blueprint
from wtforms.fields import HiddenField
from jinja2.utils import pass_eval_context
from jinja2.utils import markupsafe

import re

jinja_extensions_blueprint = Blueprint('jinja_extensions_blueprint', __name__, template_folder='templates')


@jinja_extensions_blueprint.app_template_global
def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)
