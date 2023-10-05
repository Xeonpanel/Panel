const checkAuth = require("../middleware/checkAuth");
const { Node, DockerImage, Port } = require("../models");
var captcha = require("nodejs-captcha");
const express = require("express");
const crypto = require("crypto");
const { route } = require("./auth");
const { Op } = require("sequelize");

const router = express.Router();

router.get("/nodes", checkAuth, async (req, res) => {
    const nodes = await Node.findAll();
    return res.render("admin/nodes/index", {user: req.session.user, message: req.flash("message"), nodes: nodes});
});

router.post("/nodes", checkAuth, async (req, res) => {
    const { name, ip, port } = req.body;

    if (!name || !ip || !port) {
        req.flash("message", "Fields not provided");
        return res.redirect("/admin/nodes");
    }

    if (await Node.findOne({ where: { [Op.or]: [{ ip: ip }, { name: name }] } })) {
        req.flash("message", "Node name or ip already exists");
        return res.redirect("/admin/nodes");
    }

    const { privateKey, publicKey } = crypto.generateKeyPairSync("rsa", {
        modulusLength: 2048,
        publicKeyEncoding: { type: "spki", format: "pem" },
        privateKeyEncoding: { type: "pkcs8", format: "pem" }
    });

    const node = await Node.create({
        name: name, ip: ip, port: port,
        private_key: privateKey.toString(),
        public_key: publicKey.toString()
    });
    return res.redirect("/admin/nodes");
});

router.get("/nodes/:id", checkAuth, async (req, res) => {
    const { id } = req.params;

    if (!id) {
        req.flash("message", "Node id not provided");
        return res.redirect("/admin/nodes");
    }

    const node = await Node.findOne({ where: { id: id } });
    if (!node) {
        req.flash("message", "Node not found");
        return res.redirect("/admin/nodes");
    }

    node.b64_public = Buffer.from(node.public_key).toString("base64");
    const ports = await Port.findAll({ where: { node_id: node.id } });
    node.ports = ports;
    return res.render("admin/nodes/node", {user: req.session.user, message: req.flash("message"), node: node});
});

router.post("/nodes/:node_id/ports/:port_id/delete", checkAuth, async (req, res) => {
    const { node_id, port_id } = req.params;

    if (!node_id || !port_id) {
        req.flash("message", "Node id or port id not provided");
        return res.redirect("/admin/nodes/" + node_id);
    }

    const port = await Port.findOne({ where: { id: port_id, node_id: node_id } });
    if (!port) {
        req.flash("message", "Port not found");
        return res.redirect("/admin/nodes/" + node.id);
    }

    const node = await Node.findOne({ where: { id: node_id } });
    if (!node) {
        req.flash("message", "Node not found");
        return res.redirect("/admin/nodes/" + node_id);
    }

    // checks toevoegen voor als de port al gebruikt wordt
    await port.destroy();
    return res.redirect("/admin/nodes/" + node_id);
    // checks toevoegen voor als de port al gebruikt wordt
});

router.post("/nodes/:id", checkAuth, async (req, res) => {
    const { port } = req.body;
    const { id } = req.params;

    if (!port || !id) {
        req.flash("message", "Port or node id not provided");
        return res.redirect("/admin/nodes/" + id);
    }

    if (port < 1 || port > 65535) {
        req.flash("message", "Port not valid");
        return res.redirect("/admin/nodes/" + id);
    }

    const portBlacklist = [22, 21, 80, 443, 3000, 3001, 3002, 3003, 3004, 3005, 3006, 8080];
    if (portBlacklist.includes(parseInt(port))) {
        req.flash("message", "Port not allowed");
        return res.redirect("/admin/nodes/" + id);
    }

    const regex = new RegExp("^[0-9]+$");
    if (!regex.test(port)) {
        req.flash("message", "Port not valid");
        return res.redirect("/admin/nodes/" + id);
    }

    const node = await Node.findOne({ where: { id: id } });
    if (!node) {
        req.flash("message", "Node not found");
        return res.redirect("/admin/nodes/" + id);
    }

    const portExists = await Port.findOne({ where: { port: port, node_id: node.id } });
    if (portExists) {
        req.flash("message", "Port already exists");
        return res.redirect("/admin/nodes/" + id);
    }

    await Port.create({ port: port, node_id: node.id });
    return res.redirect("/admin/nodes/" + id);
});

module.exports = router;