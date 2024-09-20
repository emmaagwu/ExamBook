from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from .services import (
    get_user_profile, update_user_profile, delete_user_profile, 
    admin_get_user, admin_get_all_users, admin_delete_user, change_password
)
from ..utils.decorator import admin_required  # Assuming you have an admin decorator

def register_routes(api):
    profile_model = api.model('UserProfile', {
        # 'user_id': fields.Integer(description='The unique identifier of the user'),
        # 'email': fields.String(description='Email address of the user'),
        # 'username': fields.String(description='Username of the user'),
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

        @api.expect(profile_model)
        @api.marshal_with(profile_model)
        @jwt_required()
        def put(self):
            """Update the authenticated user's profile"""
            current_user_id = get_jwt_identity()
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

        @api.expect(profile_model)
        @api.marshal_with(profile_model)
        @jwt_required()
        @admin_required
        def put(self, user_id):
            """Admin: Update any user's profile"""
            return update_user_profile(user_id, api.payload)

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
