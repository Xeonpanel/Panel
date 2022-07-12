import flask, os

from __main__ import app, sqlquery

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if os.path.isfile("database.db"):
        if flask.session:
            data = sqlquery("SELECT * FROM servers WHERE ownerid = ? ORDER BY id DESC", flask.session["id"],).fetchall()
            return flask.render_template(
                "themes/{}/dashboard/servers.html".format(app.config["THEME"]),
                title="Your Servers",
                page="servers",
                servers=data
            )
        else:
            return flask.redirect("/login")
    else:
        return flask.redirect("/setup/getting-started")

@app.route("/dashboard/account", methods=["GET"])
def account():
    if os.path.isfile("database.db"):
        if flask.session:
            return flask.render_template(
                "themes/{}/dashboard/account.html".format(app.config["THEME"]),
                title="Account Settings",
                page="account"
            )
        else:
            return flask.redirect("/login")
    else:
        return flask.redirect("/setup/getting-started")