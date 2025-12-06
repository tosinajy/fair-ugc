from app import app
from extensions import db, bcrypt
from models import User, Role, Permission, BaseRate, NicheMultiplier, ExperienceMultiplier, UsageRight, PitchTemplate

def seed_database():
    with app.app_context():
        print("Refreshing database schema...")
        db.drop_all()
        db.create_all()

        # 1. Permissions & Roles
        print("Creating Roles...")
        perms = {
            'can_manage_users': Permission(slug='can_manage_users', description='Manage Users'),
            'can_manage_roles': Permission(slug='can_manage_roles', description='Manage Roles'),
            'can_view_dashboard': Permission(slug='can_view_dashboard', description='View Dashboard'),
            'can_manage_pricing': Permission(slug='can_manage_pricing', description='Manage Pricing'),
        }
        for p in perms.values(): db.session.add(p)
        
        admin_role = Role(name='admin', updated_by='system')
        admin_role.permissions = list(perms.values())
        db.session.add(admin_role)

        # 2. Admin User
        hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(username='admin', password_hash=hashed_pw, role_id=1, updated_by='system')
        db.session.add(admin_user)

        # 3. Base Rates
        print("Seeding Pricing Data...")
        base_rates = [
            BaseRate(slug='video_1', name='1 Video', description='Standard 15-60s', base_price=150, icon_class='fas fa-video', sort_order=1),
            BaseRate(slug='video_3', name='3 Bundle', description='Hook testing', base_price=375, icon_class='fas fa-layer-group', sort_order=2),
            BaseRate(slug='photos_5', name='5 Photos', description='Static assets', base_price=125, icon_class='fas fa-camera', sort_order=3),
            BaseRate(slug='video_1_hooks_3', name='Vid + Hooks', description='1 body, 3 intros', base_price=200, icon_class='fas fa-random', sort_order=4),
            BaseRate(slug='raw', name='Raw Footage', description='Unedited files', base_price=225, icon_class='fas fa-file-video', sort_order=5),
        ]
        db.session.add_all(base_rates)

        niches = [
            NicheMultiplier(slug='lifestyle', name='☕ General Lifestyle / Vlogs', multiplier=1.0, logic_note='Standard Baseline', sort_order=1),
            NicheMultiplier(slug='beauty', name='💄 Beauty, Skincare & Fashion', multiplier=1.1, logic_note='High competition', sort_order=2),
            NicheMultiplier(slug='health', name='🧘‍♀️ Health & Wellness', multiplier=1.25, logic_note='Regulated industry', sort_order=3),
            NicheMultiplier(slug='home', name='🏠 Home, Kitchen & Pets', multiplier=1.3, logic_note='Prop intensive', sort_order=4),
            NicheMultiplier(slug='tech', name='💻 Tech, Apps & SaaS', multiplier=1.5, logic_note='Specialized knowledge', sort_order=5),
            NicheMultiplier(slug='finance', name='📈 Finance & Business', multiplier=1.6, logic_note='High value leads', sort_order=6),
        ]
        db.session.add_all(niches)

        exps = [
            ExperienceMultiplier(slug='beginner', name='Beginner', years_range='< 1 Year', multiplier=0.8, 
                               description='Best for creators building their initial portfolio.', sort_order=1),
            ExperienceMultiplier(slug='intermediate', name='Intermediate', years_range='1-3 Years', multiplier=1.0, 
                               description='For creators with consistent quality and proven ROI.', sort_order=2),
            ExperienceMultiplier(slug='pro', name='Pro', years_range='3+ Years', multiplier=1.5, 
                               description='For strategists with premium equipment and high demand.', sort_order=3),
        ]
        db.session.add_all(exps)

        rights = [
            UsageRight(slug='ads_30', name='Paid Ads (30 Days)', multiplier=0.30, sort_order=1),
            UsageRight(slug='ads_90', name='Paid Ads (90 Days)', multiplier=0.50, sort_order=2),
            UsageRight(slug='ads_365', name='Paid Ads (1 Year)', multiplier=1.00, sort_order=3),
            UsageRight(slug='perpetual', name='Perpetual Buyout', multiplier=3.00, is_premium=True, sort_order=4),
        ]
        db.session.add_all(rights)

        # 4. Pitch Templates
        print("Seeding Pitch Templates...")
        pitches = [
            # PROFESSIONAL
            PitchTemplate(name="Standard Professional", mood="professional", updated_by="system", content="Hi {brand_name},\n\nI’ve been following your brand and love your approach to the market. I’m a content creator specializing in {product_type} and would love to help tell your story with high-converting creative.\n\nAttached is my portfolio.\n\nBest,\n[Your Name]"),
            PitchTemplate(name="ROI Focused", mood="professional", updated_by="system", content="Hello {brand_name} Team,\n\nI noticed your recent campaigns and see a great opportunity to increase engagement. My UGC strategy for {product_type} focuses on problem-aware hooks that drive conversions.\n\nLet's discuss how we can improve your ROAS.\n\nRegards,\n[Your Name]"),
            PitchTemplate(name="Agency Style", mood="professional", updated_by="system", content="Dear {brand_name},\n\nWe are looking to partner with premium brands in the {product_type} space. My content is shot on cinema-grade equipment and edited for high retention.\n\nPlease find my media kit attached.\n\nBest,\n[Your Name]"),

            # CASUAL
            PitchTemplate(name="Friendly Fan", mood="casual", updated_by="system", content="Hey {brand_name}! 👋\n\nHuge fan of your {product_type}! I actually use it daily. I create authentic UGC that feels just like a friend recommending a product. Let's chat about how we can make some viral content together!\n\nCheers,\n[Your Name]"),
            PitchTemplate(name="Short & Sweet", mood="casual", updated_by="system", content="Hi {brand_name}!\n\nLove what you guys are doing with {product_type}. I have a few ideas for TikToks that could really pop. Do you have a minute to chat?\n\nTalk soon,\n[Your Name]"),
            PitchTemplate(name="Storyteller", mood="casual", updated_by="system", content="Hey guys! \n\nI have a really funny story about how I started using {product_type} and I think it would make a great Reel. Let me know if you're open to collabs!\n\n- [Your Name]"),

            # BOLD
            PitchTemplate(name="The Hook Master", mood="bold", updated_by="system", content="What's up {brand_name}!\n\nYour {product_type} is a game changer, but I think we can make it pop even more on TikTok. I specialize in high-energy, fast-paced edits that stop the scroll.\n\nLet's crush Q4 together.\n\n- [Your Name]"),
            PitchTemplate(name="Disruptor", mood="bold", updated_by="system", content="Stop scrolling. 🛑\n\nThat's what your customers need to do. I make aggressive, high-energy content for {product_type} brands that refuse to be ignored. \n\nReady to dominate?\n\n[Your Name]"),
            PitchTemplate(name="Viral Hunter", mood="bold", updated_by="system", content="Yo {brand_name}!\n\nI've analyzed your competitors and I know exactly how to beat them. My last {product_type} video got 50k views in 24 hours. \n\nLet's get you some of that heat.\n\n[Your Name]")
        ]
        db.session.add_all(pitches)

        db.session.commit()
        print("Database reseeded successfully with Pitch Templates.")

if __name__ == '__main__':
    seed_database()