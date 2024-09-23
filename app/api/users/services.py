from ..models.users import User
from .models import UserProfile
from ..utils.db import db
from flask import abort
from werkzeug.security import check_password_hash, generate_password_hash

def get_user_profile(user_id):
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        abort(404, "User profile not found")
    return [
        {
            'user_id': profile.user.id,  # Access the user model via relationship
            'email': profile.user.email,
            'username': profile.user.username,
            'profile': {
                'full_name': profile.full_name,
                'bio': profile.bio,
                'avatar_url': profile.avatar_url,
                'phone_number': profile.phone_number,
                'address': profile.address,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at
            }
        }
    ]

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

    profiles = UserProfile.query.all()

    if not profiles:
        abort(404, "No user profiles found")

    # return UserProfile.query.all()

    return [
        {
            'user_id': profile.user.id,  # Access the user model via relationship
            'email': profile.user.email,
            'username': profile.user.username,
            'profile': {
                'full_name': profile.full_name,
                'bio': profile.bio,
                'avatar_url': profile.avatar_url,
                'phone_number': profile.phone_number,
                'address': profile.address,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at
            }
        } for profile in profiles
    ]