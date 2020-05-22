import os

from flask import Flask
from flask import jsonify
from aiof.core import frequencies


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

    @app.route("/metadata/frequencies")
    def get_frequencies():
        return jsonify(frequencies())

    return app


if __name__ == "__main__":
    create_app().run()