from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from .services import (
    get_user_profile, update_user_profile, delete_user_profile, 
    admin_get_user, admin_get_all_users, admin_delete_user, change_password
)
from werkzeug.utils import secure_filename
import os
from flask import request, jsonify, current_app
from ..utils.decorator import admin_required  # Assuming you have an admin decorator


def allowed_file(filename):
    """Check if the file extension is allowed"""
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    print(f"Allowed Extensions: {allowed_extensions}")
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def register_routes(api):
    profile_model = api.model('UserProfile', {
        'user_id': fields.Integer(description='The unique identifier of the user'),
        'email': fields.String(description='Email address of the user'),
        'username': fields.String(description='Username of the user'),
        'full_name': fields.String(description='Full name of the user'),
        'bio': fields.String(description='Short bio of the user'),
        'avatar_url': fields.String(description='URL to the profile picture'),
        'phone_number': fields.String(description='Phone number of the user'),
        'address': fields.String(description='Home address of the user'),
        'created_at': fields.DateTime(readOnly=True),
        'updated_at': fields.DateTime(readOnly=True),
    })

    # User's own profile
    @api.route('/profile')
    class UserProfileResource(Resource):
        @api.marshal_with(profile_model)
        @jwt_required()
        def get(self):
            """Get the authenticated user's profile"""
            current_user_id = get_jwt_identity()
            return get_user_profile(current_user_id)

        @api.expect(profile_model)  # Expecting a user profile payload
        @api.marshal_with(profile_model)  # Return the user profile after updating
        @jwt_required()  # Require authentication
        def put(self):
            """Update the authenticated user's profile, including file upload"""
            current_user_id = get_jwt_identity()

            # Handle file upload
            if 'avatar' in request.files:
                file = request.files['avatar']
                if file.filename == '':
                    return jsonify({"error": "No selected file"}), 400

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    upload_folder = current_app.config['UPLOAD_FOLDER']
                    filepath = os.path.join(upload_folder, filename)
                    file.save(filepath)

                    # Update the user's avatar URL with the new file location
                    api.payload['avatar_url'] = filepath

            # Update the user's profile with the fields in the payload
            return update_user_profile(current_user_id, api.payload)

        @jwt_required()
        def delete(self):
            """Delete the authenticated user's profile"""
            current_user_id = get_jwt_identity()
            return delete_user_profile(current_user_id)

    # Admin-only endpoints
    @api.route('/admin/users')
    class AdminUsersResource(Resource):
        @api.marshal_list_with(profile_model)
        @jwt_required()
        # @admin_required  # Only admins can access these
        def get(self):
            """Admin: Get all users' profiles"""
            return admin_get_all_users()

    @api.route('/admin/users/<int:user_id>')
    class AdminUserResource(Resource):
        @api.marshal_with(profile_model)
        @jwt_required()
        @admin_required  # Only admins can access these
        def get(self, user_id):
            """Admin: Get any user's profile"""
            return admin_get_user(user_id)

        @api.marshal_with(profile_model)
        @jwt_required()
        @admin_required
        def put(self, user_id):
            """Admin: Update any user's profile"""

            try:
                # Create a dictionary to hold the profile data
                profile_data = {}

                # Handle form fields
                profile_data['full_name'] = request.form.get('full_name')
                profile_data['bio'] = request.form.get('bio')
                profile_data['phone_number'] = request.form.get('phone_number')
                profile_data['address'] = request.form.get('address')

                # Log the form data for debugging
                print(f"Received form data: {profile_data}")     




                # Handle file upload (avatar)
                if 'avatar' in request.files:
                    file = request.files['avatar']

                    print("File uploaded:", file)

                    if file.filename == '':
                        return jsonify({"error": "No selected file"}), 400

                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        upload_folder = current_app.config['UPLOAD_FOLDER']
                        filepath = os.path.join(upload_folder, filename)
                        file.save(filepath)
                        upload_path = current_app.config['UPLOAD_PATH']
                        fileretrieve_path = os.path.join(upload_path, filename)

                        # Update the user's avatar URL with the new file location
                        profile_data['avatar_url'] = fileretrieve_path

                # Log the full profile data including the avatar URL
                print(f"Profile data being updated: {profile_data}")

                # Call the function to update the user's profile with the form data
                return update_user_profile(user_id, profile_data)

            except Exception as e:
                return jsonify({"error": str(e)}), 400

        @jwt_required()
        @admin_required
        def delete(self, user_id):
            """Admin: Delete any user's account"""
            return admin_delete_user(user_id)

    # Change password route
    change_password_model = api.model('ChangePassword', {
        'old_password': fields.String(required=True, description='The old password'),
        'new_password': fields.String(required=True, description='The new password'),
    })

    @api.route('/change-password')
    class ChangePasswordResource(Resource):
        @api.expect(change_password_model)
        @jwt_required()
        def put(self):
            """Authenticated user can change their password"""
            current_user_id = get_jwt_identity()
            data = api.payload
            return change_password(current_user_id, data['old_password'], data['new_password'])
