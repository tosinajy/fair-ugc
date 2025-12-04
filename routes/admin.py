from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from marshmallow import ValidationError
from extensions import db, bcrypt
from models import User, Role, Permission, PricingConfig, Calculation, Lead
from schemas import UserSchema, RoleSchema
from auth_utils import permission_required

def register(app):
    @app.route('/admin')
    @login_required
    @permission_required('can_view_dashboard')
    def admin_dashboard():
        calc_count = Calculation.query.count()
        lead_count = Lead.query.count()
        
        active_tab = request.args.get('tab', 'dashboard')
        page = request.args.get('page', 1, type=int)
        per_page = 10 
        
        users_paginated = None
        roles_paginated = None
        users = []
        roles = []
        permissions = []
        pricing_configs = []
        
        if active_tab == 'users':
            if current_user.role.has_permission('can_manage_users'):
                users_paginated = User.query.order_by(User.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
                roles = Role.query.all()
                
        elif active_tab == 'roles':
            if current_user.role.has_permission('can_manage_roles'):
                roles_paginated = Role.query.order_by(Role.id).paginate(page=page, per_page=per_page, error_out=False)
                permissions = Permission.query.all()
                
        elif active_tab == 'pricing':
            if current_user.role.has_permission('can_manage_pricing'):
                pricing_configs = PricingConfig.query.order_by(PricingConfig.category, PricingConfig.key).all()
            
        return render_template('admin/dashboard.html', 
                               active_tab=active_tab, 
                               calc_count=calc_count, 
                               lead_count=lead_count,
                               users_paginated=users_paginated, 
                               roles_paginated=roles_paginated,
                               roles=roles,
                               permissions=permissions,
                               pricing_configs=pricing_configs)

    @app.route('/admin/pricing/update', methods=['POST'])
    @login_required
    @permission_required('can_manage_pricing')
    def update_pricing():
        try:
            for key, value in request.form.items():
                if key.startswith('conf_'):
                    db_key = key.replace('conf_', '')
                    config = PricingConfig.query.filter_by(key=db_key).first()
                    if config:
                        config.value = float(value)
                        config.updated_by = current_user.username
            db.session.commit()
            flash('Pricing configuration updated.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating pricing: {str(e)}', 'error')
            
        return redirect(url_for('admin_dashboard', tab='pricing'))

    @app.route('/admin/users/add', methods=['POST'])
    @login_required
    @permission_required('can_manage_users')
    def add_user():
        form_data = {
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'role_id': request.form.get('role_id')
        }
        
        schema = UserSchema()
        try:
            data = schema.load(form_data)
            if User.query.filter_by(username=data['username']).first():
                flash('Username already exists.', 'error')
                return redirect(url_for('admin_dashboard', tab='users'))

            hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = User(
                username=data['username'], 
                password_hash=hashed_pw, 
                role_id=data['role_id'],
                updated_by=current_user.username
            )
            db.session.add(new_user)
            db.session.commit()
            flash(f'User {data["username"]} created.', 'success')
        except ValidationError as err:
            flash(f"Validation Error: {err.messages}", "error")
        except Exception as e:
            db.session.rollback()
            flash(f"System Error: {str(e)}", "error")
            
        return redirect(url_for('admin_dashboard', tab='users'))

    @app.route('/admin/users/delete/<int:user_id>')
    @login_required
    @permission_required('can_manage_users')
    def delete_user(user_id):
        if user_id == current_user.id:
            flash("You cannot delete yourself.", "error")
            return redirect(url_for('admin_dashboard', tab='users'))
            
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            flash('User deleted.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting user: {str(e)}", 'error')
            
        return redirect(url_for('admin_dashboard', tab='users'))

    @app.route('/admin/roles/add', methods=['POST'])
    @login_required
    @permission_required('can_manage_roles')
    def add_role():
        form_name = request.form.get('name')
        permissions_list = request.form.getlist('permissions')
        
        schema = RoleSchema()
        try:
            data = schema.load({'name': form_name})
            if Role.query.filter_by(name=data['name']).first():
                flash('Role name already exists.', 'error')
                return redirect(url_for('admin_dashboard', tab='roles'))

            new_role = Role(name=data['name'], updated_by=current_user.username)
            
            for p_id in permissions_list:
                perm = Permission.query.get(int(p_id))
                if perm:
                    new_role.permissions.append(perm)
                    
            db.session.add(new_role)
            db.session.commit()
            flash(f'Role {data["name"]} created.', 'success')
        except ValidationError as err:
             flash(f"Error: {err.messages}", "error")
        except Exception as e:
            db.session.rollback()
            flash(f"System Error: {str(e)}", "error")
            
        return redirect(url_for('admin_dashboard', tab='roles'))

    @app.route('/admin/roles/delete/<int:role_id>')
    @login_required
    @permission_required('can_manage_roles')
    def delete_role(role_id):
        try:
            role = Role.query.get_or_404(role_id)
            if role.name == 'admin':
                flash('Cannot delete the Admin role.', 'error')
            else:
                db.session.delete(role)
                db.session.commit()
                flash('Role deleted.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting role: {str(e)}", "error")
            
        return redirect(url_for('admin_dashboard', tab='roles'))