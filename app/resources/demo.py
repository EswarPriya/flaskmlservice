from flasgger import swag_from
from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument
from service import DemoService
from util import parse_params


class DemoResource(Resource):
    """ Verbs relative to the users """

    @staticmethod
    @parse_params(
        Argument('demo1', location='json', required=True, help='some info.'),
        Argument('demo2', location='json', required=False, help='some info.'),
        Argument('demo3', location='json', required=False, help='some info.')
    )
    @swag_from('../swagger/demo/POST.yml')
    def post(demo1, demo2, demo3):
        result = DemoService.doSomething()
        return jsonify(result)
