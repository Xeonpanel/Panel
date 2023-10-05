const express = require("express");
const router = express.Router();
const { User, Node, Port } = require("../models");
const crypto = require("crypto");

async function generateJWT(node) {
    let resp = await fetch(`https://${node.ip}:${node.port}/api/jwt`, {
        method: "GET",
    });

    let encryptedBytes = await resp.text();
    let decryptedBytes = crypto.privateDecrypt(node.private_key, Buffer.from(encryptedBytes, "base64"));
    let decryptedText = decryptedBytes.toString("utf8");

    resp = await fetch(`https://${node.ip}:${node.port}/api/jwt`, {
        method: "POST",
        body: decryptedText,
    });

    return await resp.text();
}

module.exports = router;