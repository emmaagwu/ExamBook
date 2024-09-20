from flask_restx import Namespace
from .controller import register_routes

users_ns = Namespace('users', description='Operations related to user management')

register_routes(users_ns)
