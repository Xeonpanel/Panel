import flask

from __main__ import app, sqlquery

@app.route("/admin/nodes", methods=["GET"])
def admin_nodes():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/nodes/nodes.html".format(app.config["THEME"]),
                title="Nodes",
                page="nodes",
                nodes=sqlquery("SELECT * FROM nodes ORDER BY id ASC").fetchall(),
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0], 
                panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/nodes/create", methods=["GET"])
def create_node():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/nodes/createnode.html".format(app.config["THEME"]),
                title="Nodes",
                page="nodes",
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0], 
                panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/nodes/<nodeid>/view", methods=["GET"])
def view_node(nodeid):
    if flask.session:
        if flask.session["user_type"] == "administrator":
            data = sqlquery("SELECT * FROM nodes WHERE id = ?", int(nodeid),).fetchall()
            if len(data):
                return flask.render_template(
                    "themes/{}/admin/nodes/viewnode.html".format(app.config["THEME"]),
                    title="Nodes",
                    page="nodes",
                    panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0],
                    panellogo=sqlquery("SELECT panel_logo FROM settings").fetchone()[0], 
                    node=sqlquery("SELECT * FROM nodes WHERE id = ?", int(nodeid),).fetchall()[0]
                )
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")