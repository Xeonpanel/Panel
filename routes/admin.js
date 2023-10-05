const checkAuth = require("../middleware/checkAuth");
const { Node, DockerImage } = require("../models");
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
        modulusLength: 4096,
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

module.exports = router;