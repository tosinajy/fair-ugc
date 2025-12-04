from app import app
from app.models import db, User, Role, Permission, PricingConfig
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def seed_database():
    with app.app_context():
        print("Dropping old database...")
        db.drop_all()
        print("Creating new schema...")
        db.create_all()

        # 1. Create Permissions
        perms_list = [
            ('can_manage_users', 'Access to add/delete users'),
            ('can_manage_roles', 'Access to add/delete roles'),
            ('can_view_dashboard', 'View Admin Dashboard'),
            ('can_manage_pricing', 'Adjust pricing logic variables')
        ]
        
        perm_objs = {}
        for slug, desc in perms_list:
            p = Permission(slug=slug, description=desc)
            db.session.add(p)
            perm_objs[slug] = p
        
        db.session.commit()

        # 2. Create Roles & Assign Permissions
        admin_role = Role(name='admin', updated_by='system')
        # Admin gets all permissions
        admin_role.permissions = list(perm_objs.values())
        
        editor_role = Role(name='editor', updated_by='system')
        # Editor gets specific permissions
        editor_role.permissions = [perm_objs['can_view_dashboard']]
        
        db.session.add_all([admin_role, editor_role])
        db.session.commit()

        # 3. Create Admin User
        hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(username='admin', password_hash=hashed_pw, role_id=admin_role.id, updated_by='system')
        db.session.add(admin_user)

        # 4. Seed Pricing Config
        configs = [
            # Base Rates
            ('base_video', 150.0, 'base', 'Base rate for 1 UGC Video'),
            ('base_photo', 50.0, 'base', 'Base rate for Photo Bundle'),
            ('base_testimonial', 75.0, 'base', 'Base rate for Testimonial'),
            
            # Experience Multipliers
            ('mult_exp_inter', 0.20, 'multiplier', 'Intermediate Experience Multiplier'),
            ('mult_exp_pro', 1.0, 'multiplier', 'Pro Experience Multiplier'),
            
            # Niche Multipliers
            ('mult_niche_tech', 0.50, 'multiplier', 'Tech/Finance Niche Multiplier'),
            ('mult_niche_beauty', 0.20, 'multiplier', 'Beauty Niche Multiplier'),

            # Usage Rights (Multipliers on Base)
            ('usage_ads_30', 0.30, 'usage', 'Paid Ads 30 Days'),
            ('usage_ads_90', 0.50, 'usage', 'Paid Ads 90 Days'),
            ('usage_exclusivity', 0.40, 'usage', 'Exclusivity Clause'),
            ('usage_whitelisting', 0.25, 'usage', 'Whitelisting Access'),
        ]

        for key, val, cat, desc in configs:
            c = PricingConfig(key=key, value=val, category=cat, description=desc, updated_by='system')
            db.session.add(c)
        
        db.session.commit()
        print("Database re-seeded successfully with Dynamic Pricing and Relational Permissions.")

if __name__ == '__main__':
    seed_database()