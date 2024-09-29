from flask import Flask
from flask_restx import Api
from .controllers.auth_controller import auth_namespace as auth_ns
from .utils.db import db
from .models.users import User
from .config.config import config_dict
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .questions import questions_ns
from .subjects import subject_ns
from .users import users_ns
from .examinations import examination_ns
from flask_cors import CORS
import os
from flask import send_from_directory

def create_app(config=config_dict['dev']):

    app = Flask(__name__)


    CORS(app,
        resources={r"/*": {"origins": "*"}},  # Adjust this for production environments
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]  # Include OPTIONS here
    )

    app.config.from_object(config)

    db.init_app(app)

    jwt=JWTManager(app)

    migrate=Migrate(app, db)

    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


    api=Api(app,
        title='ExamBook API',
        version='1.0',
        description='A RESTAPI for the online Examination app',
        authorizations='authorizations',
        security='Bearer Auth'
    )

    api.add_namespace(auth_ns)
    api.add_namespace(questions_ns)
    api.add_namespace(subject_ns)
    api.add_namespace(examination_ns)
    api.add_namespace(users_ns)

    @app.route('/uploads/avatars/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
