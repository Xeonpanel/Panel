import flask

from __main__ import app, sqlquery

@app.route("/admin/servers", methods=["GET"])
def servers():
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/servers/servers.html", title="Servers", sqlquery=sqlquery)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")
        
@app.route("/admin/servers/create", methods=["GET"])
def create_server():
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/servers/createserver.html", title="Servers", sqlquery=sqlquery)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/servers/<serverid>/view", methods=["GET"])
def view_server(serverid):
    if flask.session:
        if sqlquery("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            if len(sqlquery("SELECT * FROM servers WHERE id = ?", serverid)):
                return flask.render_template("/admin/servers/viewserver.html", title="Servers", sqlquery=sqlquery, serverid=serverid)
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")