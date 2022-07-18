import flask, os

from __main__ import app, sqlquery

@app.route("/setup/register-admin", methods=["POST"])
def register_admin():
    if not os.path.isfile("database.db"):
        import models
        sqlquery(
            "INSERT INTO settings (panel_name) VALUES (?)",
            "Xeonpanel"
        )
        sqlquery(
            "INSERT INTO settings (panel_logo) VALUES (?)",
            "Xeonpanel"
        )
        sqlquery( 
            "INSERT INTO users (username, email, password, user_type, api_key) VALUES (?, ?, ?, ?, ?)",
            flask.request.form["username"],
            flask.request.form["email"],
            flask.request.form["password"],
            "administrator",
            os.urandom(250).hex()
        )
        return flask.redirect("/setup/setup-final")
    else:
        flask.abort(403)

@app.route("/setup/setup-final", methods=["GET"])
def setup_final():
    if os.path.isfile("database.db"):
        return flask.render_template(
            "themes/{}/setup/setupfinal.html".format(app.config["THEME"]),
            title="Installing"
        )
    else:
        flask.abort(403)

@app.route("/setup/getting-started", methods=["GET"])
def getting_started():
    if not os.path.isfile("database.db"):
        return flask.render_template(
            "themes/{}/setup/welcome.html".format(app.config["THEME"]),
            title="Getting Started"
        )
    else:
        flask.abort(403)

@app.route("/setup/setup-account", methods=["GET"])
def setup_account():
    if not os.path.isfile("database.db"):
        return flask.render_template(
            "themes/{}/setup/setupaccount.html".format(app.config["THEME"]),
            title="Setup Account"
        )
    else:
        flask.abort(403)