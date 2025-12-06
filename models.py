from extensions import db
from flask_login import UserMixin
from datetime import datetime

# --- Association Table ---
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    updated_by = db.Column(db.String(100))
    permissions = db.relationship('Permission', secondary=role_permissions, lazy='subquery',
        backref=db.backref('roles', lazy=True))
    users = db.relationship('User', backref='role', lazy=True)

    def has_permission(self, perm_slug):
        return any(p.slug == perm_slug for p in self.permissions)

# --- PRICING MODELS ---

class BaseRate(db.Model):
    __tablename__ = 'base_rates'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    icon_class = db.Column(db.String(50), default='fas fa-video')
    base_price = db.Column(db.Integer, nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    updated_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NicheMultiplier(db.Model):
    __tablename__ = 'niche_multipliers'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    multiplier = db.Column(db.Float, nullable=False, default=1.0)
    logic_note = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)
    updated_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExperienceMultiplier(db.Model):
    __tablename__ = 'experience_multipliers'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    years_range = db.Column(db.String(50))
    description = db.Column(db.String(200))
    multiplier = db.Column(db.Float, nullable=False, default=1.0)
    sort_order = db.Column(db.Integer, default=0)
    updated_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UsageRight(db.Model):
    __tablename__ = 'usage_rights'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    multiplier = db.Column(db.Float, nullable=False, default=0.0)
    is_premium = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    updated_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50))
    record_slug = db.Column(db.String(50))
    action = db.Column(db.String(50))
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    changed_by = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# --- CONTENT MODELS ---

class PitchTemplate(db.Model):
    __tablename__ = 'pitch_templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mood = db.Column(db.String(50)) 
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Added fields
    updated_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    updated_by = db.Column(db.String(100))

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.String(100))

class Calculation(db.Model):
    __tablename__ = 'calculations'
    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(50))
    niche = db.Column(db.String(50))
    usage_rights = db.Column(db.Text)
    calculated_min = db.Column(db.Integer)
    calculated_max = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.String(100))