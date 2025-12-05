from app import app
from extensions import db, bcrypt
from models import User, Role, Permission, PricingConfig

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

        # 2. Create Roles
        admin_role = Role(name='admin', updated_by='system')
        admin_role.permissions = list(perm_objs.values())
        
        editor_role = Role(name='editor', updated_by='system')
        editor_role.permissions = [perm_objs['can_view_dashboard']]
        
        db.session.add_all([admin_role, editor_role])
        db.session.commit()

        # 3. Create Admin User
        hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(username='admin', password_hash=hashed_pw, role_id=admin_role.id, updated_by='system')
        db.session.add(admin_user)

        # 4. Seed Pricing Config (UPDATED)
        configs = [
            # Content Types (Base Rates)
            ('base_video_1', 150.0, 'base', '1 Short-Form Video (15-60s)'),
            ('base_video_3', 375.0, 'base', '3 Video Bundle (Hook Testing)'),
            ('base_photos_5', 125.0, 'base', '5 Static Photos'),
            ('base_video_1_hooks_3', 200.0, 'base', '1 Video + 3 Hooks'),
            ('base_raw', 225.0, 'base', 'Raw Footage (No Edits)'),
            
            # Niche Multipliers (Factors: 1.0, 1.1, etc.)
            ('mult_niche_lifestyle', 1.0, 'multiplier', 'General Lifestyle / Vlogs'),
            ('mult_niche_beauty', 1.1, 'multiplier', 'Beauty, Skincare & Fashion'),
            ('mult_niche_health', 1.25, 'multiplier', 'Health & Wellness'),
            ('mult_niche_home', 1.3, 'multiplier', 'Home, Kitchen & Pets'),
            ('mult_niche_tech', 1.5, 'multiplier', 'Tech, Apps & SaaS'),
            ('mult_niche_finance', 1.6, 'multiplier', 'Finance & Business'),

            # Experience Level (Factors: 0.8x, 1.0x, 1.5x)
            ('mult_exp_beginner', 0.8, 'multiplier', 'Beginner (0.8x)'),
            ('mult_exp_intermediate', 1.0, 'multiplier', 'Intermediate (1.0x)'),
            ('mult_exp_pro', 1.5, 'multiplier', 'Pro (1.5x)'),

            # Usage Rights (Add-on Percentages)
            ('usage_organic', 0.0, 'usage', 'Organic Only'),
            ('usage_ads_30', 0.30, 'usage', 'Paid Ads (30 Days)'),
            ('usage_ads_90', 0.50, 'usage', 'Paid Ads (90 Days)'),
            ('usage_ads_365', 1.00, 'usage', 'Paid Ads (365 Days)'),
            ('usage_perpetual', 3.00, 'usage', 'Perpetual / Full Buyout'),
        ]

        for key, val, cat, desc in configs:
            c = PricingConfig(key=key, value=val, category=cat, description=desc, updated_by='system')
            db.session.add(c)
        
        db.session.commit()
        print("Database re-seeded successfully with Updated Pricing.")

if __name__ == '__main__':
    seed_database()