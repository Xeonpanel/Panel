import flask

from __main__ import app, sqlquery

@app.route("/admin", methods=["GET"])
def admin():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/admin.html".format(app.config["THEME"]),
                title="Settings",
                page="settings",
                settings=sqlquery("SELECT * FROM settings").fetchall()[0],
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0  ]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

# View, create, list nodes

@app.route("/admin/nodes", methods=["GET"])
def admin_nodes():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/nodes/nodes.html".format(app.config["THEME"]),
                title="Nodes",
                page="nodes",
                nodes=sqlquery("SELECT * FROM nodes ORDER BY id ASC").fetchall(),
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0]
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
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/users/create", methods=["GET"])
def create_user():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/users/createuser.html".format(app.config["THEME"]),
                title="Users",
                page="users",
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0]
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
                    node=sqlquery("SELECT * FROM nodes WHERE id = ?", int(nodeid),).fetchall()[0]
                )
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/users", methods=["GET"])
def admin_users():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/users/users.html".format(app.config["THEME"]),
                title="Users",
                page="users",
                users=sqlquery("SELECT * FROM users ORDER BY id ASC").fetchall(),
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/users/<userid>/view", methods=["GET"])
def view_user(userid):
    if flask.session:
        if flask.session["user_type"] == "administrator":
            data = sqlquery("SELECT * FROM users WHERE id = ?", int(userid),).fetchall()
            if len(data):
                return flask.render_template(
                    "themes/{}/admin/users/viewuser.html".format(app.config["THEME"]),
                    title="Users",
                    page="users",
                    panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0],
                    user=sqlquery("SELECT * FROM users WHERE id = ?", int(userid),).fetchall()[0]
                )
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

# View, create, list servers

@app.route("/admin/servers", methods=["GET"])
def admin_servers():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/servers/servers.html".format(app.config["THEME"]),
                title="Servers",
                page="servers",
                servers=sqlquery("SELECT * FROM servers ORDER BY id ASC").fetchall(),
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/servers/create", methods=["GET"])
def create_server():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            data = sqlquery("SELECT * FROM nodes ORDER BY id ASC").fetchall()
            if len(data):
                return flask.render_template(
                    "themes/{}/admin/servers/createserver.html".format(app.config["THEME"]),
                    title="Servers",
                    page="servers",
                    panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0],
                    nodes=sqlquery("SELECT * FROM nodes ORDER BY id ASC").fetchall(),
                    users=sqlquery("SELECT * FROM users ORDER BY id ASC").fetchall(),
                    images=sqlquery("SELECT * FROM images ORDER BY id ASC").fetchall()
                )
            else:
                flask.flash("error", "There are no nodes available")
                return flask.redirect("/admin/servers")
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

# View, create, list images

@app.route("/admin/images", methods=["GET"])
def admin_images():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/images/images.html".format(app.config["THEME"]),
                title="Images",
                page="images",
                images=sqlquery("SELECT * FROM images ORDER BY id ASC").fetchall(),
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/admin/images/create", methods=["GET"])
def create_image():
    if flask.session:
        if flask.session["user_type"] == "administrator":
            return flask.render_template(
                "themes/{}/admin/images/createimage.html".format(app.config["THEME"]),
                title="Images",
                page="images",
                panelname=sqlquery("SELECT panel_name FROM settings").fetchone()[0]
            )
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")