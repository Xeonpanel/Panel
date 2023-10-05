const express = require("express");
const router = express.Router();
const { User, Node, Port } = require("../models");
const crypto = require("crypto");
const process = require("process");
const chalk = require("chalk");

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

async function generateJWT(node) {
    try {
        let resp = await fetch(`https://${node.ip}:${node.port}/api/jwt`, {
            method: "GET",
        });
    
        let cookies = resp.headers.get("set-cookie");
        let encryptedBytes = await resp.text();
        let decryptedBytes = crypto.privateDecrypt(node.private_key, Buffer.from(encryptedBytes, "base64"));
        let decryptedText = decryptedBytes.toString();
    
        resp = await fetch(`https://${node.ip}:${node.port}/api/jwt`, {
            method: "POST",
            body: JSON.stringify({ decryptedBytes: decryptedText }),
            headers: {
                "Cookie": cookies,
                "Content-Type": "application/json"
            }
        });
    
        return await resp.text();
    } catch (err) {
        console.log(`[${chalk.red("Error")}] Node ${node.id} is offline`);
        return null;
    }
}

const jwtCache = {};

router.get("/:node_id/ping", async (req, res) => {
    const { node_id } = req.params;

    if (!node_id) {
        return res.json({ success: false, error: "Node id not provided" });
    }

    const node = await Node.findOne({ where: { id: node_id } });
    if (!node) {
        return res.json({ success: false, error: "Node not found" });
    }

    const jwt = await generateJWT(node);
    if (!jwt) {
        return res.json({ success: false, error: "Internal Server Error" });
    }

    const resp = await fetch(`https://${node.ip}:${node.port}/api`, {
        method: "GET",
        headers: {
            "x-access-token": jwt
        }
    });

    if (resp.status === 200) {
        return res.json({ success: true });
    } else {
        return res.json({ success: false, error: "Something went wrong" });
    }
});

module.exports = router;