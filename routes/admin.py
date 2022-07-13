import flask

from __main__ import app, sqlquery

@app.route("/admin", methods=["GET"])
def admin():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/admin.html".format(app.config["THEME"]),
                title="Settings",
                page="settings",
                settings=sqlquery("SELECT * FROM settings").fetchall()[0],
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0  ]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")



