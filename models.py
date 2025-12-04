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

class PricingConfig(db.Model):
    __tablename__ = 'pricing_config'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.String(200))
    updated_by = db.Column(db.String(100))

class PitchTemplate(db.Model):
    __tablename__ = 'pitch_templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mood = db.Column(db.String(50)) 
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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