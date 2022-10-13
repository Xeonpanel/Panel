import flask, hashlib, sys, time, requests, os

from __main__ import app, query

# Panel gateway to Deamon

# Stop server
@app.post("/gateway/<node_id>/servers/<server_uuid>/stop")
def stop_server(node_id, server_uuid):
    if flask.session:
        session = requests.Session()
        session.headers.update({
            "Authorization": query("SELECT * FROM nodes WHERE id = ?", node_id)[0][5]
        })
        return session.post("http://{}/servers/{}/stop".format(query("SELECT * FROM nodes WHERE id = ?", node_id)[0][4], server_uuid)).json()

# Start server
@app.post("/gateway/<node_id>/servers/<server_uuid>/start")
def start_server(node_id, server_uuid):
    if flask.session:
        session = requests.Session()
        session.headers.update({
            "Authorization": query("SELECT * FROM nodes WHERE id = ?", node_id)[0][5]
        })
        return session.post("http://{}/servers/{}/start".format(query("SELECT * FROM nodes WHERE id = ?", node_id)[0][4], server_uuid)).json()