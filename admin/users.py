import flask

from __main__ import app, sqlquery

@app.route("/admin/users/create", methods=["GET"])
def create_user():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/users/createuser.html".format(app.config["THEME"]),
                title="Users",
                page="users",
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0], 
                panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/users", methods=["GET"])
def admin_users():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/users/users.html".format(app.config["THEME"]),
                title="Users",
                page="users",
                users=sqlquery("SELECT * FROM users ORDER BY id ASC").fetchall(),
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0], 
                panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/users/<userid>/view", methods=["GET"])
def view_user(userid):
    if flask.session:
        if flask.session["user_type"] == "administrator":
            data = sqlquery("SELECT * FROM users WHERE id = ?", int(userid),).fetchall()
            if len(data):
                return flask.render_template(
                    "themes/{}/admin/users/viewuser.html".format(app.config["THEME"]),
                    title="Users",
                    page="users",
                    panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0],
                    user=sqlquery("SELECT * FROM users WHERE id = ?", int(userid),).fetchall()[0], 
                    panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0]
                )
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")