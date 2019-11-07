"""
Defines the blueprint for the users
"""
from flask import Blueprint
from flask_restful import Api

from resources import DemoResource

DEMO_BLUEPRINT = Blueprint('demo', __name__)
Api(DEMO_BLUEPRINT).add_resource(
    DemoResource,
    '/Demo/'
)
