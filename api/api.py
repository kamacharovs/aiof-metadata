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

    @app.route("/car/loan", methods=["GET"])
    def get_car_loan():
        return jsonify(car.loan_calc(25000, 3.75, 72))

    @app.route("/loan/payments/<string:frequency>", methods=["POST"])
    def get_loan_payments(frequency):
        loan_amount = request.form["loanAmount"]
        number_of_years = request.form["numberOfYears"]
        rate_of_interest = request.form["rateOfInterest"]
        return core.loan_payments_calc_as_table(loan_amount, number_of_years, rate_of_interest, frequency)

    return app

    
if __name__ == "__main__":
    create_app().run()