import os
import aiof.helpers as helpers
import aiof.car.core as car
import aiof.fi.core as fi

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, NotFound


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(NotFound)
    def page_not_found_handler(e: HTTPException):
        return 'Not found', 404


    @app.route("/metadata/frequencies", methods=["GET"])
    def get_frequencies():
        return jsonify(list(helpers._frequency.keys()))

    @app.route("/metadata/car/loan", methods=["POST"])
    def get_car_loan():
        return jsonify(car.loan_calc(request.get_json(silent=True)))

    @app.route("/metadata/compare/asset", methods=["GET"])
    def compare_asset_value():
        args = request.args
        if "value" in args:
            value = args["value"]
        if "contribution" in args:
            contribution = args["contribution"]
        return jsonify(helpers.compare_asset_to_market(value, contribution))



    @app.route("/metadata/fi/time/to/fi", methods=["POST"])
    def time_to_fi():
        return jsonify(fi.time_to_fi_req(request.get_json(silent=True)))
    
    @app.route("/metadata/fi/added/time", methods=["POST"])
    def added_time_to_fi():
        return jsonify(fi.added_time_to_fi_req(request.get_json(silent=True)))

    @app.route("/metadata/fi/rule/of/72", methods=["POST"])
    def rule_of_72():
        return jsonify(fi.rule_of_72_req(request.get_json(silent=True)))

    @app.route("/metadata/fi/ten/million/dream/<int:monthlyInvestment>", methods=["GET"])
    def ten_million_dream(monthlyInvestment):
        return jsonify(fi.ten_million_dream(monthlyInvestment))

    @app.route("/metadata/fi/compound/interest", methods=["POST"])
    def compound_interest():
        return jsonify(fi.compound_interest_req(request.get_json(silent=True)))

    @app.route("/metadata/fi/investment/fees/effect", methods=["POST"])
    def investment_fees_effect():
        return jsonify(fi.investment_fees_effect_req(request.get_json(silent=True)))

    @app.route("/metadata/fi/cost/of/raising/children", methods=["POST"])
    def cost_of_raising_children():
        return jsonify(fi.cost_of_raising_children_req(request.get_json(silent=True)))
    @app.route("/metadata/fi/cost/of/raising/children/families", methods=["GET"])
    def cost_of_raising_children_families():
        return jsonify(fi.cost_of_raising_children_faimilies())


    return app

    
#if __name__ == "__main__":
#    create_app().run()