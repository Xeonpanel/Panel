const express = require("express");
const router = express.Router();
const { User, Node, Port } = require("../models");
const crypto = require("crypto");
const process = require("process");

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

async function generateJWT(node) {
    let resp = await fetch(`https://${node.ip}:${node.port}/api/jwt`, {
        method: "GET",
    });

    let cookies = resp.headers.get("set-cookie");
    let encryptedBytes = await resp.text();
    let decryptedBytes = crypto.privateDecrypt(node.private_key, Buffer.from(encryptedBytes, "base64"));
    let decryptedText = decryptedBytes.toString();

    resp = await fetch(`https://${node.ip}:${node.port}/api/jwt`, {
        method: "POST",
        body: decryptedText,
        headers: {
            "Cookie": cookies,
        }
    });

    return await resp.text();
}

module.exports = router;