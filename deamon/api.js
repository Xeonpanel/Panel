const express = require("express");
const crypto = require("crypto");
const { Token } = require("./models");
const jwt = require("jsonwebtoken");
const { requireJWT } = require("./jwt");
const fs = require("fs");
const Docker = require("dockerode");
const path = require("path");

const router = express.Router();
const docker = new Docker({ socketPath: "/var/run/docker.sock" });

router.get("/jwt", async (req, res) => {
    const randomBytes = crypto.randomBytes(24).toString("hex");
    req.session.randomBytes = randomBytes;
    const token = await Token.findAll();

    if (token.length <= 0) {
        return res.status(500).send("Internal Server Error");
    }

    const publicKey = token[0].public_key;

    const encryptedBytes = crypto.publicEncrypt(publicKey, Buffer.from(randomBytes));
    const encryptedText = encryptedBytes.toString("base64");

    return res.send(encryptedText);
});

router.post("/jwt", async (req, res) => {
    const { randomBytes } = req.session;
    const { decryptedBytes } = req.body;

    if (!randomBytes || !decryptedBytes) {
        return res.status(400).send("Bad Request");
    }

    if (randomBytes !== decryptedBytes) {
        return res.status(401).send("Unauthorized");
    }

    const token = await Token.findAll()
    const jwt_key = token[0].jwt_key;
    const jwtToken = jwt.sign({ authorized: true }, jwt_key);
    res.send(jwtToken);
});

router.get("/", requireJWT, async (req, res) => {
    return res.json({ success: true });
});

router.post("/server", requireJWT, async (req, res) => {
    const { dockerfile, name, ram, cpu, port, uuid } = req.body;

    if (!dockerfile || !name || !ram || !cpu || !port || !uuid) {
        return res.status(400).send("Bad Request");
    }

    if (fs.existsSync(path.join(__dirname, "containers", uuid))) {
        return res.status(400).send("Bad Request");
    }

    fs.mkdirSync(path.join(__dirname, "containers", uuid), { recursive: true });
    const containerPath = path.join(__dirname, "containers", uuid);
    fs.writeFileSync(path.join(containerPath, "Dockerfile"), dockerfile);

    const image = await docker.buildImage({
        context: containerPath,
        src: ["Dockerfile"]
    }, { t: uuid });

    image.pipe(process.stdout);

    const server = await docker.run(uuid, [], null, {
        name: uuid,
        HostConfig: {
            PortBindings: {
                "80/tcp": [{
                    HostPort: port.toString()
                }]
            },
            Memory: ram * 1024 * 1024,
            NanoCPUs: cpu,
            Detach: true
        }
    });

    res.json({ success: true, server: server });
});

router.get("/servers", requireJWT, async (req, res) => {
    const containers = await docker.listContainers();

    res.send(containers);
});

module.exports = router;