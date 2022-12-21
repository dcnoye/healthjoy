from pygments.formatters import HtmlFormatter
import markdown
import markdown.extensions.fenced_code
from flask import (
    Blueprint,
    request,
    render_template,
)

from wtforms import Form, StringField, SubmitField, validators, PasswordField

home_blueprint = Blueprint('home', __name__, template_folder='templates')



class SubForm(Form):
    token = StringField('Token', validators=[validators.DataRequired('Token is required')])
    label = StringField('Label', validators=[validators.DataRequired('Label is required')])
    submit = SubmitField('Submit')

@home_blueprint.route('/')
def landing_page():
    """Landing page."""
    formatter = HtmlFormatter(style="emacs", full=True, cssclass="codehilite")
    css_string = formatter.get_style_defs()

    readme_file = open("README.md", "r")
    markdown_string = markdown.markdown(
        readme_file.read(),
        extensions=["fenced_code", "codehilite"]
    )
    markdown_css = "<style>" + css_string + "</style>"
    good_stuff = markdown_css + markdown_string

    return good_stuff


@home_blueprint.route('/sub', methods=['GET', 'POST'])
def submit_page():
    form = SubForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.token.data)
        print(form.label.data)
        
        return redirect(url_for('home.landing_page'))
    return render_template('views/sub.html', form=form)
