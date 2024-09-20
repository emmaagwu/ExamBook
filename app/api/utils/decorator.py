from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import abort
from ..models.users import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            abort(403, "Admin privileges required")
        
        return fn(*args, **kwargs)
    
    return wrapper