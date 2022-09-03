import flask

from __main__ import app, query

@app.route("/admin/servers", methods=["GET"])
def servers():
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/servers/servers.html", title="Servers", query=query)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")
        
@app.route("/admin/servers/create", methods=["GET"])
def create_server():
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/servers/createserver.html", title="Servers", query=query)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/servers/<serverid>/view", methods=["GET"])
def view_server(serverid):
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            if len(query("SELECT * FROM servers WHERE id = ?", serverid)):
                return flask.render_template("/admin/servers/viewserver.html", title="Servers", query=query, serverid=serverid)
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")