import flask

from __main__ import app, query

@app.get("/dashboard")
def dashboard():
    if flask.session:
        return flask.render_template(
            "/dashboard/servers.html",
            title="Your servers",
            servers=query("SELECT * FROM servers WHERE owner_id = ?", flask.session["id"]),
            panellogo=query('SELECT panel_logo FROM settings')[0][0],
            panelname=query('SELECT panel_name FROM settings')[0][0],
            usertype=query("SELECT user_type FROM users WHERE id = ?", flask.session["id"])[0][0]
        )
    else:
        return flask.redirect("/")

@app.get("/dashboard/account")
def dashboard_account():
    if flask.session:
        return flask.render_template("/dashboard/account.html", title="Account settings", query=query)
    else:
        return flask.redirect("/")