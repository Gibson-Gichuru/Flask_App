from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/')
def index():
    return render_template("index.html", current_time=datetime.utcnow())


@main.route('/user', methods=["POST", "GET"])
def user():
    form = NameForm()
    # validates the form using wtforms validators
    if form.validate_on_submit():
        # queries the database for a user by the name provided in the input field
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            # adds a new user to the database
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
            # send email to app admin once any new names are added to the database
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
                print("Email sent")
        else:
            session["known"] = True
        session["name"] = form.name.data
        form.name.data = ''
        return redirect(url_for(".user"))
    return render_template("user.html", form=form, name=session.get("name"), known=session.get("known", False))
