from functools import wraps
from flask import redirect, url_for, abort
from flask_login import current_user
from extensions import login_manager
from models import User

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None

def permission_required(perm_slug):
    """
    Decorator to check if the current user's role has specific permissions.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            
            # Safe check in case user has no role assigned
            if not current_user.role or not current_user.role.has_permission(perm_slug):
                abort(403) 
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator