import flask

from __main__ import app, sqlquery

@app.route("/admin", methods=["GET"])
def admin():
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/settings.html", title="Settings", sqlquery=sqlquery)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")