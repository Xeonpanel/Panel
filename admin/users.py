import flask

from __main__ import app, query

@app.get("/admin/users")
def users():
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/users/users.html", title="Users", query=query)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.get("/admin/users/create")
def create_user():
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/users/createuser.html", title="Users", query=query)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.get("/admin/users/<userid>/view")
def view_user(userid):
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            if len(query("SELECT * FROM users WHERE id = ?", userid)):
                return flask.render_template("/admin/users/viewuser.html", title="Users", query=query, userid=userid)
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")