import flask

from __main__ import app, query

@app.get("/admin")
def admin():
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/settings.html", title="Settings", query=query)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")