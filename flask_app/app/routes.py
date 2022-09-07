import jwt
import requests
from flask import render_template, flash, url_for, request, redirect, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from .models import User
from .forms import RegistrationForm, LoginForm, VerifyForm, TypeMailCountry
from . import app, db, bcrypt
from .otp_mail import generate_otp, send_email


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def pas():
    return render_template("index.html", title="Home", user=current_user.get_id())


@app.route("/news")
def news():
    news = (
        requests.get("http://thailand_api:5001/thai_news").json()["data"]
        + requests.get("http://poland_api:5002/pol_news").json()["data"]
        + requests.get("http://latvia_api:5003/latv_news").json()["data"]
        + requests.get("http://lithuania_api:5004/lith_news").json()["data"]
        + requests.get("http://spain_api:5005/spain_news").json()["data"]
    )
    return render_template("news.html", seq=news)


@app.route("/norway")
def norway():
    return render_template("norway.html")


""" THAILAND"""


@app.route("/thailand")
def thailand():
    return render_template("thailand.html")


@app.route("/thailand/viscentr")
def thailand_visacent():
    response = requests.get("http://thailand_api:5001/thai_visaac").json()
    response = response["data"]
    return render_template("visa_centr.html", seq=response)


@app.route("/thailand/embassy")
def thailand_cons():
    response = requests.get("http://thailand_api:5001/thai_cons").json()
    response = response["data"]
    return render_template("embassy.html", seq=response)
    # return jsonify(response)


@app.route("/thailand/news")
def thailand_news():
    response = requests.get("http://thailand_api:5001/thai_news").json()
    response = response["data"]
    return render_template("news.html", seq=response)


""" POLAND """


@app.route("/poland")
def poland():
    return render_template("poland.html")


@app.route("/poland/viscentr")
def poland_visacent():
    response = requests.get("http://poland_api:5002/pol_visaac").json()
    response = response["data"]
    return render_template("visa_centr.html", seq=response)
    # return jsonify(response)


@app.route("/poland/embassy")
def poland_cons():
    response = requests.get("http://poland_api:5002/pol_cons").json()
    response = response["data"]
    return render_template("embassy.html", seq=response)
    # return jsonify(response)


@app.route("/poland/freeplaces")
def poland_freeplaces():
    # data = requests.get('http://realtime:5050/pol').json()['Poland']
    # return data
    return render_template("freeplaces.html")


@app.route("/poland/news")
def poland_news():
    response = requests.get("http://poland_api:5002/pol_news").json()
    response = response["data"]
    return render_template("news.html", seq=response)


""" Latvia """


@app.route("/latvia")
def latvia():
    return render_template("latvia.html")


@app.route("/latvia/viscentr")
def latvia_visacent():
    response = requests.get("http://latvia_api:5003/latv_visaac").json()
    response = response["data"]
    return render_template("visa_centr.html", seq=response)
    # return jsonify(response)


@app.route("/latvia/embassy")
def latvia_cons():
    response = requests.get("http://latvia_api:5003/latv_cons").json()
    response = response["data"]
    return render_template("embassy.html", seq=response)
    # return jsonify(response)


@app.route("/latvia/news")
def latvia_news():
    response = requests.get("http://latvia_api:5003/latv_news").json()
    response = response["data"]
    return render_template("news.html", seq=response)


""" Lithuania """


@app.route("/lithuania")
def lithuania():
    return render_template("lithuania.html")


@app.route("/lithuania/viscentr")
def lithuania_visacent():
    response = requests.get("http://lithuania_api:5004/lith_visaac").json()
    response = response["data"]
    return render_template("visa_centr.html", seq=response)
    # return jsonify(response)


@app.route("/lithuania/embassy")
def lithuania_cons():
    response = requests.get("http://lithuania_api:5004/lith_cons").json()
    response = response["data"]
    return render_template("embassy.html", seq=response)
    # return jsonify(response)


@app.route("/lithuania/news")
def lithuania_news():
    response = requests.get("http://lithuania_api:5004/lith_news").json()
    response = response["data"]
    return render_template("news.html", seq=response)


""" Spain """


@app.route("/spain")
def spain():
    return render_template("spain.html")


@app.route("/spain/viscentr")
def spain_visacent():
    response = requests.get("http://spain_api:5005/spain_visaac").json()
    response = response["data"]
    return render_template("visa_centr.html", seq=response)
    # return jsonify(response)


@app.route("/spain/embassy")
def spain_cons():
    response = requests.get("http://spain_api:5005/spain_cons").json()
    response = response["data"]
    return render_template("embassy.html", seq=response)
    # return jsonify(response)


@app.route("/spain/news")
def spain_news():
    response = requests.get("http://spain_api:5005/spain_news").json()
    response = response["data"]
    return render_template("news.html", seq=response)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        token = jwt.encode(
            {"email": form.email.data}, app.config["SECRET_KEY"], algorithm="HS256"
        )
        otp_code = generate_otp()
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            token=token,
            otp_code=otp_code,
            is_verify=False,
        )

        send_email(email=form.email.data, otp_code=otp_code)
        db.session.add(user)
        db.session.commit()
        flash("Thank for. To complete your registration please verify.", "success")
        return redirect(url_for("verify", token=token))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    'Error in field "{}": {}'.format(
                        getattr(form, field).label.text, error
                    )
                )

    return render_template("register.html", form=form, title="Registration")


@app.route("/verify/<string:token>", methods=["GET", "POST"])
def verify(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = VerifyForm()
    if form.validate_on_submit():
        data = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
        email = data["email"]
        user = User.query.filter_by(email=email).first()
        if user and int(form.otp.data) == int(user.otp_code):
            user.is_verify = True
            db.session.commit()
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect("/")
        else:
            user.otp_code = generate_otp()
            send_email(user.email, user.otp_code)
            flash("Failed verification. Enter new code on your email", "message")
            return redirect(url_for("verify", token=token))
    return render_template("verify.html", form=form, title="Verify")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (
            user
            and user.is_verify
            and bcrypt.check_password_hash(user.password, form.password.data)
        ):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect("/")
        else:
            flash("Failed login. Please check you email or password", "message")
    return render_template("login.html", form=form, title="Login")


# страница профиля
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    user = User.query.filter_by(id=current_user.get_id()).first()
    form = TypeMailCountry()
    if form.validate_on_submit() and request.method == "POST":
        from elasticsearch import Elasticsearch

        es = (
            Elasticsearch([app.config["ELASTICSEARCH_URL"]])
            if app.config["ELASTICSEARCH_URL"]
            else None
        )
        info = dict()
        info["user"] = user.email
        info["type_mailing"] = form.state_mail.data
        info["country"] = form.state_country.data
        es.index(index="mailing", body=info)
        es.indices.refresh(index="mailing")
        return render_template(
            "user.html",
            title="Profile setting",
            user=user,
            form=form,
            message="Your choice is saved!",
        )

    return render_template("user.html", title="Profile setting", user=user, form=form)


# @app.route('/to_elastic', methods=['GET', 'POST'])
# @login_required
# def to_elastic():
#     type = request.form.get('type')
#     country = request.form.get('type')
#
#     return render_template('user.html', title='Profile setting', user=user)


# логаут
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("pas"))
