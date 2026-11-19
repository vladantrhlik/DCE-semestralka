import json
import logging
import os

from flask import Flask, abort, jsonify, request, send_from_directory
from kazoo.client import KazooClient
from kazoo.exceptions import KazooException, NoNodeError, NodeExistsError


app = Flask(__name__)
zk_hosts = os.environ.get("ZK_HOSTS", "zookeeper:2181")
kv_root = os.environ.get("KV_ROOT", "/kv").rstrip("/")

if not kv_root.startswith("/") or kv_root == "/":
    raise ValueError("KV_ROOT must be an absolute ZooKeeper path other than '/'")

zk = KazooClient(hosts=zk_hosts)
frontend_dir = os.path.dirname(os.path.abspath(__file__))


@app.errorhandler(NoNodeError)
def handle_missing_node(error):
    return jsonify(error="key not found"), 404


@app.errorhandler(KazooException)
def handle_zookeeper_error(error):
    app.logger.exception("ZooKeeper request failed")
    return jsonify(error="ZooKeeper request failed"), 503


@app.get("/health")
def health():
    connected = zk.connected
    return jsonify(status="ok" if connected else "unavailable"), 200 if connected else 503


@app.get("/docs")
@app.get("/docs/")
def swagger_ui():
    return send_from_directory(frontend_dir, "swagger.html")


@app.get("/openapi.yaml")
def openapi_spec():
    return send_from_directory(frontend_dir, "openapi.yaml", mimetype="application/yaml")


@app.get("/kv")
def list_keys():
    return jsonify(keys=sorted(zk.get_children(kv_root)))


@app.route("/kv/<string:key>", methods=["GET", "PUT", "DELETE"])
def key_value(key):
    path = f"{kv_root}/{key}"

    if request.method == "GET":
        value, _ = zk.get(path)
        return jsonify(key=key, value=json.loads(value.decode("utf-8")))

    if request.method == "PUT":
        if not request.is_json:
            abort(415, description="Content-Type must be application/json")
        value = request.get_json()
        data = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        try:
            zk.create(path, data, makepath=True)
            status = 201
        except NodeExistsError:
            zk.set(path, data)
            status = 200
        return jsonify(key=key, value=value), status

    zk.delete(path)
    return "", 204


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
    zk.start(timeout=float(os.environ.get("ZK_START_TIMEOUT", "15")))
    zk.ensure_path(kv_root)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
