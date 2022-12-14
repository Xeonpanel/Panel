import flask, os, time, datetime
from __main__ import db, bycrypt, app
from models import Users

@app.post("/setup/register-admin")
def setup_register_admin():
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    email = flask.request.form["email"]

    if username and password and email:
        if not os.path.exists("database/database.sqlite"):
            with app.app_context():
                db.create_all()
                db.session.commit()
        with app.app_context():
            hashed_password = bycrypt.generate_password_hash(password).decode("utf-8")
            admin = Users(username=username, password=hashed_password, email=email, admin=True, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
            db.session.add(admin)
            db.session.commit()
        
        os.remove("routers/setup.py")
        return flask.redirect("/setup/setup-final")

@app.get("/setup/finish")
def setup_reboot_server():
    time.sleep(1)
    exit(0)

@app.get("/setup/setup-final")
def setup_final():
    return flask.render_template(
        "/setup/setupfinal.html",
        title="Installing",
        page="setup.installing"
    )

@app.get("/setup/getting-started")
def setup_getting_started():
    return flask.render_template(
        "/setup/welcome.html",
        title="Getting Started",
        page="setup.gettingstarted"
    )

@app.get("/setup/setup-account")
def setup_account():
    return flask.render_template(
        "/setup/setupaccount.html",
        title="Setup Account",
        page="setup.setupaccount"
    )
