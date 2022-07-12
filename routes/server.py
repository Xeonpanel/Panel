import flask, sqlite3, os, requests

from __main__ import app, sqlquery

@app.route("/dashboard/server/<serverid>")
def server(serverid):
    if flask.session:
        data = sqlquery("SELECT * FROM servers WHERE ownerid = ? and id = ?", flask.session["id"], int(serverid)).fetchall()
        if len(data):
            return flask.render_template(
                "themes/{}/server/server.html".format(app.config["THEME"]),
                title="Console",
                serverinfo=data
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")