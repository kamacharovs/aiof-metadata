import os
import aiof.core as core
import aiof.helpers as helpers
import aiof.car.core as car

from flask import Flask
from flask import request
from flask import jsonify


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/metadata/frequencies", methods=["GET"])
    def get_frequencies():
        return jsonify(list(helpers._frequency.keys()))

    @app.route("/metadata/car/loan", methods=["POST"])
    def get_car_loan():
        return jsonify(car.loan_calc(request.get_json(silent=True)))

    @app.route("/metadata/loan/payments/<string:frequency>", methods=["GET", "POST"])
    def get_loan_payments(frequency):
        return jsonify(core.loan_payments_calc_as_table(request.get_json(silent=True), frequency))

    @app.route("/metadata/compare/asset", methods=["GET"])
    def compare_asset_value():
        args = request.args
        if "value" in args:
            value = args["value"]
        if "contribution" in args:
            contribution = args["contribution"]
        return jsonify(helpers.compare_asset_to_market(value, contribution))

    return app

    
if __name__ == "__main__":
    create_app().run()