import flask

from __main__ import app, query

@app.get("/admin/nodes")
def nodes():
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/nodes/nodes.html", title="Nodes", query=query)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.get("/admin/nodes/create")
def create_node():
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            return flask.render_template("/admin/nodes/createnode.html", title="Nodes", query=query)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.get("/admin/nodes/<nodeid>/view")
def view_node(nodeid):
    if flask.session:
        if query("SELECT * FROM users WHERE id = ?", flask.session["id"])[0][5] == "administrator":
            if len(query("SELECT * FROM nodes WHERE id = ?", nodeid)):
                return flask.render_template("/admin/nodes/viewnode.html", title="Nodes", query=query, nodeid=nodeid)
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")