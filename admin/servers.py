import flask

from __main__ import app, sqlquery

@app.route("/admin/servers", methods=["GET"])
def admin_servers():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/servers/servers.html".format(app.config["THEME"]),
                title="Servers",
                page="servers",
                servers=sqlquery("SELECT * FROM servers ORDER BY id ASC").fetchall(),
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0], 
                panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/servers/create", methods=["GET"])
def create_server():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            data = sqlquery("SELECT * FROM nodes ORDER BY id ASC").fetchall()
            if len(data):
                return flask.render_template(
                    "themes/{}/admin/servers/createserver.html".format(app.config["THEME"]),
                    title="Servers",
                    page="servers",
                    panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0],
                    panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0], 
                    nodes=sqlquery("SELECT * FROM nodes ORDER BY id ASC").fetchall(),
                    users=sqlquery("SELECT * FROM users ORDER BY id ASC").fetchall(),
                    images=sqlquery("SELECT * FROM images ORDER BY id ASC").fetchall()
                )
            else:
                flask.flash("error", "There are no nodes available")
                return flask.redirect("/admin/servers")
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")