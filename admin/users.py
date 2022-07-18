import flask

from __main__ import app, sqlquery

@app.route("/admin/users", methods=["GET"])
def users():
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/users/users.html", title="Users", sqlquery=sqlquery)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/users/create", methods=["GET"])
def create_user():
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/users/createuser.html", title="Users", sqlquery=sqlquery)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/users/<userid>/view", methods=["GET"])
def view_user(userid):
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            if len(sqlquery("SELECT * FROM users WHERE id = ?", userid)):
                return flask.render_template("/admin/users/viewuser.html", title="Users", sqlquery=sqlquery, userid=userid)
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")