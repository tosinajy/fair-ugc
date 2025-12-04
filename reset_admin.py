import sys
from app import app
from app.models import db, User, Role
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def reset_admin():
    """
    Resets the database with default roles and a super admin user.
    Usage: python reset_admin.py
    """
    with app.app_context():
        print("Creating/Updating Tables...")
        db.create_all()

        # 1. Ensure Roles Exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', updated_by='system_script')
            admin_role.set_permissions({'can_manage_users': True, 'can_manage_roles': True, 'can_view_dashboard': True})
            db.session.add(admin_role)
            print("Created Admin role.")
        else:
            # Ensure admin always has full perms on reset
            admin_role.set_permissions({'can_manage_users': True, 'can_manage_roles': True, 'can_view_dashboard': True})

        editor_role = Role.query.filter_by(name='editor').first()
        if not editor_role:
            editor_role = Role(name='editor', updated_by='system_script')
            editor_role.set_permissions({'can_manage_users': False, 'can_manage_roles': False, 'can_view_dashboard': True})
            db.session.add(editor_role)
            print("Created Editor role.")

        db.session.commit()

        # 2. Create/Reset Admin User
        admin_user = User.query.filter_by(username='admin').first()
        hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')

        if admin_user:
            admin_user.password_hash = hashed_pw
            admin_user.role_id = admin_role.id
            admin_user.updated_by = 'system_script'
            print("Admin user password reset to 'admin123'.")
        else:
            admin_user = User(
                username='admin', 
                password_hash=hashed_pw, 
                role_id=admin_role.id,
                updated_by='system_script'
            )
            db.session.add(admin_user)
            print("Created Admin user with password 'admin123'.")
        
        # 3. Create Test Editor User
        editor_user = User.query.filter_by(username='editor_test').first()
        if not editor_user:
            hashed_pw_ed = bcrypt.generate_password_hash('editor123').decode('utf-8')
            editor_user = User(
                username='editor_test',
                password_hash=hashed_pw_ed,
                role_id=editor_role.id,
                updated_by='system_script'
            )
            db.session.add(editor_user)
            print("Created Editor test user.")

        db.session.commit()
        print("Database initialized successfully.")

if __name__ == '__main__':
    reset_admin()