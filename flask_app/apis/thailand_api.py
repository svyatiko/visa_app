from flask import Flask, jsonify, make_response

import sys

sys.path.insert(0, "/app/es")
from EsController import EsController

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route("/<index>/", methods=["GET"])
def get_index_data(index):
    data = es_controller.get_all_index_data(index)
    response = {"data": data} if data else {"error": "Not found"}
    return response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    es_controller = EsController()
    app.run(debug=True, host="0.0.0.0", port=5001)
