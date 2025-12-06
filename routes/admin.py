from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from marshmallow import ValidationError
from extensions import db, bcrypt
from models import User, Role, Permission, BaseRate, NicheMultiplier, ExperienceMultiplier, UsageRight, AuditLog, Lead, Calculation, PitchTemplate
from schemas import UserSchema, RoleSchema
from auth_utils import permission_required
import datetime

def log_change(table, record_slug, action, old_val, new_val):
    log = AuditLog(
        table_name=table,
        record_slug=record_slug,
        action=action,
        old_value=str(old_val),
        new_value=str(new_val),
        changed_by=current_user.username
    )
    db.session.add(log)

def register(app):
    
    # --- 1. Dashboard Home ---
    @app.route('/admin')
    @login_required
    @permission_required('can_view_dashboard')
    def admin_dashboard():
        calc_count = Calculation.query.count()
        lead_count = Lead.query.count()
        return render_template('admin/index.html', 
                               calc_count=calc_count, 
                               lead_count=lead_count,
                               active_page='dashboard')

    # --- 2. User Management ---
    @app.route('/admin/users')
    @login_required
    @permission_required('can_manage_users')
    def admin_users():
        page = request.args.get('page', 1, type=int)
        users_paginated = User.query.order_by(User.id.desc()).paginate(page=page, per_page=10)
        roles = Role.query.all()
        return render_template('admin/users.html', 
                               users_paginated=users_paginated, 
                               roles=roles,
                               active_page='users')

    # --- 3. Role Management ---
    @app.route('/admin/roles')
    @login_required
    @permission_required('can_manage_roles')
    def admin_roles():
        roles = Role.query.all()
        permissions = Permission.query.all()
        return render_template('admin/roles.html', 
                               roles=roles, 
                               permissions=permissions,
                               active_page='roles')

    # --- 4. Pricing Engine ---
    @app.route('/admin/pricing')
    @login_required
    @permission_required('can_manage_pricing')
    def admin_pricing():
        base_rates = BaseRate.query.order_by(BaseRate.sort_order).all()
        niches = NicheMultiplier.query.order_by(NicheMultiplier.sort_order).all()
        exps = ExperienceMultiplier.query.order_by(ExperienceMultiplier.sort_order).all()
        usages = UsageRight.query.order_by(UsageRight.sort_order).all()
        return render_template('admin/pricing.html', 
                               base_rates=base_rates,
                               niches=niches,
                               exps=exps,
                               usages=usages,
                               active_page='pricing')
    
    # --- 5. Pitch Templates (NEW) ---
    @app.route('/admin/pitches')
    @login_required
    @permission_required('can_manage_pricing') # Reusing existing perm for content
    def admin_pitches():
        pitches = PitchTemplate.query.order_by(PitchTemplate.mood, PitchTemplate.name).all()
        return render_template('admin/pitches.html', 
                               pitches=pitches,
                               active_page='pitches')

    @app.route('/admin/pitches/add', methods=['POST'])
    @login_required
    @permission_required('can_manage_pricing')
    def add_pitch():
        try:
            name = request.form.get('name')
            mood = request.form.get('mood')
            content = request.form.get('content')
            
            new_pitch = PitchTemplate(
                name=name,
                mood=mood,
                content=content,
                updated_by=current_user.username
            )
            db.session.add(new_pitch)
            db.session.commit()
            log_change('PitchTemplate', name, 'CREATE', '', content[:20])
            flash('Pitch template created.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating pitch: {str(e)}', 'error')
        return redirect(url_for('admin_pitches'))

    @app.route('/admin/pitches/delete/<int:pitch_id>')
    @login_required
    @permission_required('can_manage_pricing')
    def delete_pitch(pitch_id):
        try:
            pitch = PitchTemplate.query.get_or_404(pitch_id)
            db.session.delete(pitch)
            db.session.commit()
            flash('Pitch template deleted.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting pitch: {str(e)}', 'error')
        return redirect(url_for('admin_pitches'))

    # --- 6. Audit Logs ---
    @app.route('/admin/audit')
    @login_required
    @permission_required('can_view_dashboard')
    def admin_audit():
        audit_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(50).all()
        return render_template('admin/audit.html', 
                               audit_logs=audit_logs,
                               active_page='audit')

    # --- Actions (Updates/Creates) ---

    @app.route('/admin/pricing/update/<string:table_type>', methods=['POST'])
    @login_required
    @permission_required('can_manage_pricing')
    def update_pricing_table(table_type):
        try:
            if table_type == 'base':
                records = BaseRate.query.all()
                for r in records:
                    new_price = float(request.form.get(f'price_{r.id}', r.base_price))
                    if new_price != r.base_price:
                        log_change('BaseRate', r.slug, 'UPDATE', r.base_price, new_price)
                        r.base_price = new_price
                        r.updated_by = current_user.username
            
            elif table_type == 'niche':
                records = NicheMultiplier.query.all()
                for r in records:
                    new_mult = float(request.form.get(f'mult_{r.id}', r.multiplier))
                    if new_mult != r.multiplier:
                        log_change('NicheMultiplier', r.slug, 'UPDATE', r.multiplier, new_mult)
                        r.multiplier = new_mult
                        r.updated_by = current_user.username

            elif table_type == 'exp':
                records = ExperienceMultiplier.query.all()
                for r in records:
                    new_mult = float(request.form.get(f'mult_{r.id}', r.multiplier))
                    if new_mult != r.multiplier:
                        log_change('ExpMultiplier', r.slug, 'UPDATE', r.multiplier, new_mult)
                        r.multiplier = new_mult
                        r.updated_by = current_user.username

            elif table_type == 'usage':
                records = UsageRight.query.all()
                for r in records:
                    new_mult = float(request.form.get(f'mult_{r.id}', r.multiplier))
                    if new_mult != r.multiplier:
                        log_change('UsageRight', r.slug, 'UPDATE', r.multiplier, new_mult)
                        r.multiplier = new_mult
                        r.updated_by = current_user.username

            db.session.commit()
            flash(f'{table_type.title()} pricing updated successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating pricing: {str(e)}', 'error')
            
        return redirect(url_for('admin_pricing'))

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
                return redirect(url_for('admin_users'))

            hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = User(username=data['username'], password_hash=hashed_pw, role_id=data['role_id'], updated_by=current_user.username)
            db.session.add(new_user)
            db.session.commit()
            flash(f'User {data["username"]} created.', 'success')
        except ValidationError as err:
            flash(f"Validation Error: {err.messages}", "error")
        except Exception as e:
            db.session.rollback()
            flash(f"System Error: {str(e)}", "error")
        return redirect(url_for('admin_users'))

    @app.route('/admin/users/delete/<int:user_id>')
    @login_required
    @permission_required('can_manage_users')
    def delete_user(user_id):
        if user_id == current_user.id:
            flash("You cannot delete yourself.", "error")
            return redirect(url_for('admin_users'))
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            flash('User deleted.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting user: {str(e)}", 'error')
        return redirect(url_for('admin_users'))

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
                return redirect(url_for('admin_roles'))

            new_role = Role(name=data['name'], updated_by=current_user.username)
            for p_id in permissions_list:
                perm = Permission.query.get(int(p_id))
                if perm: new_role.permissions.append(perm)
                    
            db.session.add(new_role)
            db.session.commit()
            flash(f'Role {data["name"]} created.', 'success')
        except ValidationError as err:
             flash(f"Error: {err.messages}", "error")
        except Exception as e:
            db.session.rollback()
            flash(f"System Error: {str(e)}", "error")
        return redirect(url_for('admin_roles'))

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
        return redirect(url_for('admin_roles'))