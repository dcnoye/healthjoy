import uuid, json, requests
from pygments.formatters import HtmlFormatter
import markdown
import markdown.extensions.fenced_code
from flask import (
    flash,
    Blueprint,
    redirect,
    request,
    render_template,
    url_for,
)

from wtforms import Form, StringField, SubmitField, validators, PasswordField

home_blueprint = Blueprint('home', __name__, template_folder='templates')



class SubForm(Form):
    token = StringField('Token', validators=[validators.DataRequired('Token is required')])
    submit = SubmitField('Submit')

@home_blueprint.route('/')
def landing_page():
    """Landing page."""
    formatter = HtmlFormatter(style="colorful", full=True, cssclass="codehilite")
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
        resp = fork_it(form.token.data)
        if resp.status_code == 202:
           flash(f'payload accepted - {resp.status_code}', 'success')
        else:
           flash(f'Something went wrong - {resp.status_code}', 'error')
        return redirect(url_for('home.submit_page'))
    return render_template('views/sub.html', form=form)


def fork_it(token):
    headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28",
    }
    data = {
    "name": "New-fork",
    "default_branch_only": True,
    }

    owner = "dcnoye"
    repo = "healthjoy"
    url = f"https://api.github.com/repos/{owner}/{repo}/forks"
    resp = requests.post(url, headers=headers, json=data)
    return resp
