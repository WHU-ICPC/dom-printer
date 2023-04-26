#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
import time
import shutil
import threading
from base64 import b64encode

from flask import Flask, jsonify

app = Flask(__name__)

BASE_DIR = os.environ.get("PRINT_BASE_DIR", "simulation\server")
NEW_DIR = os.path.join(BASE_DIR, "new")
OLD_DIR = os.path.join(BASE_DIR, "old")

processed = {}
lock = threading.Lock()

nonce_pattern = re.compile(r"[0-9a-zA-Z-]+")


@app.route("/api/print", methods=["GET"])
def get_file():
    files = os.listdir(NEW_DIR)
    for file in files:
        if file.endswith(".txt"):
            nonce = os.path.splitext(file)[0]
            if nonce_pattern.fullmatch(nonce) and nonce not in processed:
                txt_file = os.path.join(NEW_DIR, file)
                dat_file = os.path.join(NEW_DIR, f"{nonce}.dat")

                with open(txt_file, "rb") as f:
                    info = b64encode(f.read()).decode("utf-8")
                with open(dat_file, "rb") as f:
                    data = b64encode(f.read()).decode("utf-8")
                with lock:
                    processed[nonce] = time.time()

                return jsonify({"id": nonce, "info": info, "data": data})

    return jsonify({"error": "No files available"}), 404


@app.route("/api/print/<nonce>", methods=["DELETE"])
def delete_file(nonce):
    if nonce in processed:
        txt_file = os.path.join(NEW_DIR, f"{nonce}.txt")
        dat_file = os.path.join(NEW_DIR, f"{nonce}.dat")

        shutil.move(txt_file, os.path.join(OLD_DIR, f"{nonce}.txt"))
        shutil.move(dat_file, os.path.join(OLD_DIR, f"{nonce}.dat"))
        with lock:
            del processed[nonce]

        return jsonify({"result": "success"})

    return jsonify({"error": "File not found"}), 404


def clean_processed():
    while True:
        time.sleep(30)
        now = time.time()
        for key in list(processed.keys()):
            if now - processed[key] > 30:
                with lock:
                    del processed[key]


if __name__ == "__main__":
    clear = threading.Thread(target=clean_processed, daemon=True)
    clear.start()
    app.run(host='0.0.0.0', port=5000)
