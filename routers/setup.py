import flask, os, time, datetime
from __main__ import db, bcrypt, app
from models import Users

@app.post("/setup/register-admin")
def setup_register_admin():
    if os.path.isfile("routers/setup.py"):
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        email = flask.request.form["email"]

        if username and password and email:  
            if not os.path.exists("database/database.sqlite"):
                with app.app_context(): 
                    db.create_all()
                    db.session.commit() 
                
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            admin = Users(username=username, password=hashed_password, email=email, admin=True, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
            db.session.add(admin)
            db.session.commit()
            
            os.remove("routers/setup.py")
            return flask.redirect("/setup/setup-final")
    else:
        flask.abort(404)

@app.get("/setup/finish")
def setup_reboot_server():
    return flask.redirect("/")

@app.get("/setup/setup-final")
def setup_final():
    return flask.render_template(
        "/setup/setupfinal.html",
        title="Installed",
        page="setup.installed"
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
