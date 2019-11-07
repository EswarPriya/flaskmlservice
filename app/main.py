import config
import routes
from flasgger import Swagger
from flask import Flask
from flask.blueprints import Blueprint

app = Flask(__name__)

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Application",
    "specs": [
        {
            "version": "0.0.1",
            "title": "Application",
            "endpoint": 'spec',
            "route": '/application/spec',
            "rule_filter": lambda rule: True  # all in
        }
    ],
    "static_url_path": "/application/apidocs"
}

Swagger(app)

app.debug = config.DEBUG

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        app.register_blueprint(
            blueprint,
            url_prefix=config.APPLICATION_ROOT
        )

if __name__ == '__main__':
    # print(config.PORT)
    app.run(host=config.HOST, port=config.PORT)
