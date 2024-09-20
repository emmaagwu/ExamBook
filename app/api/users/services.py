from ..models.users import User
from .models import UserProfile
from ..utils.db import db
from flask import abort
from werkzeug.security import check_password_hash, generate_password_hash

def get_user_profile(user_id):
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        abort(404, "User profile not found")
    return profile

def update_user_profile(user_id, data):
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        abort(404, "User profile not found")

    profile.full_name = data.get('full_name', profile.full_name)
    profile.bio = data.get('bio', profile.bio)
    profile.avatar_url = data.get('avatar_url', profile.avatar_url)
    profile.phone_number = data.get('phone_number', profile.phone_number)
    profile.address = data.get('address', profile.address)

    db.session.commit()
    return profile

def delete_user_profile(user_id):
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        abort(404, "User profile not found")
    
    profile.delete()
    return '', 204

# Admin: Get any user profile
def admin_get_user(user_id):
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        abort(404, "User profile not found")
    return profile

# Admin: Delete any user
def admin_delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, "User not found")

    # Delete the user's profile if it exists
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if profile:
        db.session.delete(profile)
    
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Change user's password
def change_password(user_id, old_password, new_password):
    user = User.query.get(user_id)
    if not user:
        abort(404, "User not found")

    if not check_password_hash(user.password_hash, old_password):
        abort(400, "Old password is incorrect")

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return {'message': 'Password updated successfully'}


# Admin: Get all user profiles
def admin_get_all_users():
    # Query all users with their profiles
    # users = User.query.all()

    # if not users:
    #     abort(404, "No users found")

    # profiles = UserProfile.query.all()

    # return [
    #     {
    #         'user_id': user.id,
    #         'email': user.email,
    #         'profile': {
    #             'full_name': user.profile.full_name if user.profile else None,
    #             'bio': user.profile.bio if user.profile else None,
    #             'avatar_url': user.profile.avatar_url if user.profile else None,
    #             'phone_number': user.profile.phone_number if user.profile else None,
    #             'address': user.profile.address if user.profile else None,
    #             'created_at': user.profile.created_at if user.profile else None,
    #             'updated_at': user.profile.updated_at if user.profile else None
    #         }
    #     } for user in users 
    # ]


    # return [
    #     {
    #         'profile': {
    #             'user_id': profile.user.id,
    #             'email': profile.user.email,
    #             'username': profile.user.username,
    #             'full_name': profile.full_name if profile else None,
    #             'bio': profile.bio if profile else None,
    #             'avatar_url': profile.avatar_url if profile else None,
    #             'phone_number': profile.phone_number if profile else None,
    #             'address': profile.address if profile else None,
    #             'created_at': profile.created_at if profile else None,
    #             'updated_at': profile.updated_at if profile else None
    #         }
    #     } for profile in profiles
    # ]
    return UserProfile.query.all()