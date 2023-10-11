import argparse
from flask import Flask, make_response, request, jsonify
from pysyncobj.batteries import ReplLockManager
from werkzeug.exceptions import NotFound, BadRequest

from storage import Storage


app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", "--self",
    type=str
)
parser.add_argument(
    "-o", "--other",
    type=str,
    nargs="+"
)
args = parser.parse_args()

manager = ReplLockManager(autoUnlockTime=50)
storage = Storage(args.self, args.other, manager)


@app.route("/", methods=["GET"])
def handler_ping():
    return make_response()


@app.get("/keys")
def handler_keys():
    return jsonify(storage.keys())


@app.post("/set")
def handler_set():
    data = request.json

    if (
        not isinstance(data, dict)
        or "key" not in data
        or "value" not in data
        or not isinstance(data["key"], str)
    ):
        return BadRequest()

    storage.set(data["key"], data["value"])
    return make_response()


@app.get("/get/<key>")
def handler_get(key):
    if key not in storage.keys():
        return NotFound()
    return jsonify(
        {
            "key": key,
            "value": storage.get(key)
        }
    )


@app.post("/pop/<key>")
def handler_pop(key):
    storage.pop(key)
    return make_response()


@app.post("/clear")
def handler_clear():
    storage.clear()
    return make_response()


def is_correct_data(data):
    if not isinstance(data, dict):
        return False
    pop_list = data.get("pop", [])
    if not isinstance(pop_list, list):
        return False
    for item in pop_list:
        if not isinstance(item, str):
            return False
    set_dict = data.get("set", dict())
    if not isinstance(set_dict, dict):
        return False
    for key in set_dict:
        if not isinstance(key, str):
            return False

    get_list = data.get("get", [])
    if not isinstance(get_list, list):
        return False
    for key in get_list:
        if not isinstance(item, str):
            return False
    return True


@app.post("/execute")
def handler_execute():
    data = request.json

    if is_correct_data(data):
        pop_list, set_dict, get_list = data.get("pop", []), data.get("set", {}), data.get("get", [])

        with manager.tryAcquire("execute", sync=True):
            for elem in pop_list:
                storage.pop(elem)
            for elem in set_dict:
                storage.set(elem, set_dict[elem])
            return jsonify(
                {
                    "get": [storage.get(key) for key in get_list]
                }
            )
    else:
        return BadRequest("incorrect data")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
