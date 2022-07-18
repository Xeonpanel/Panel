import flask

from __main__ import app, sqlquery

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if flask.session:
        return flask.render_template("/dashboard/servers.html", title="Your servers", sqlquery=sqlquery)
    else:
        return flask.redirect("/")

@app.route("/dashboard/account", methods=["GET"])
def dashboard_account():
    if flask.session:
        return flask.render_template("/dashboard/account.html", title="Account settings", sqlquery=sqlquery)
    else:
        return flask.redirect("/")