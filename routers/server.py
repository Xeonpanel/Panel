import flask, requests, json

from __main__ import app, sqlquery

@app.route("/dashboard/server/<serverid>")
def server(serverid):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            return flask.render_template("/server/server.html", title="Console", sqlquery=sqlquery, serverid=serverid)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/dashboard/server/<serverid>/files")
def server_files(serverid):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            return flask.render_template("/server/files.html", title="File Manager", sqlquery=sqlquery, serverid=serverid, requests=requests, json=json)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/dashboard/server/<serverid>/configuration")
def server_configuration(serverid):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            return flask.render_template("/server/configuration.html", title="Configuration", sqlquery=sqlquery, serverid=serverid)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")