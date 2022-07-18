import flask

from __main__ import app, sqlquery

@app.route("/dashboard/server/<serverid>")
def server(serverid):
    if flask.session:
        data = sqlquery("SELECT * FROM servers WHERE ownerid = ? and id = ?", flask.session["id"], int(serverid)).fetchall()
        if len(data):
            return flask.render_template(
                "themes/{}/server/server.html".format(app.config["THEME"]),
                title="Console",
                serverinfo=data, 
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0], 
                panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/dashboard/server/<serverid>/files")
def server_files(serverid):
    if flask.session:
        data = sqlquery("SELECT * FROM servers WHERE ownerid = ? and id = ?", flask.session["id"], int(serverid)).fetchall()
        if len(data):
            return flask.render_template(
                "themes/{}/server/files.html".format(app.config["THEME"]),
                title="File Manager",
                serverinfo=data,
                files=["test1", "test2", "test3", "test4", "test5", "test6"]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")