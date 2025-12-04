import random
from flask import Flask, render_template
from config import Config
from extensions import db, bcrypt, login_manager, limiter
import routes.public as public_routes
import routes.auth as auth_routes
import routes.admin as admin_routes

# Import models to ensure they are registered with SQLAlchemy
from models import PitchTemplate 

app = Flask(__name__)
app.config.from_object(Config)

# --- Init Extensions ---
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
limiter.init_app(app)

# --- Register Routes ---
public_routes.register(app)
auth_routes.register(app)
admin_routes.register(app)

# --- Global Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', content="<div class='ui container center aligned' style='margin-top:50px;'><h1>404</h1><p>Page Not Found</p></div>"), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('base.html', content="<div class='ui container center aligned' style='margin-top:50px;'><h1>403</h1><p>Access Denied</p></div>"), 403

@app.errorhandler(500)
def internal_error(e):
    return render_template('base.html', content="<div class='ui container center aligned' style='margin-top:50px;'><h1>500</h1><p>Internal Server Error</p></div>"), 500

# --- Seed Script Wrapper (Optional) ---
def seed_pitch_templates():
    if not PitchTemplate.query.first():
        templates = [
            PitchTemplate(
                name="Professional/Corporate",
                mood="professional",
                content="Hi {brand_name},\n\nI’ve been following your brand for a while and love your approach to the market. I’m a content creator specializing in {product_type} and would love to help tell your story.\n\nAttached is my portfolio.\n\nBest,\n[Your Name]"
            ),
            PitchTemplate(
                name="Casual/Authentic",
                mood="casual",
                content="Hey {brand_name} team! 👋\n\nHuge fan of your {product_type}! I actually use it daily. I create authentic UGC that feels just like a friend recommending a product. Let's chat about how we can make some viral content together!\n\nCheers,\n[Your Name]"
            ),
            PitchTemplate(
                name="Bold/High Energy",
                mood="bold",
                content="What's up {brand_name}!\n\nYour {product_type} is a game changer, but I think we can make it pop even more on TikTok. I specialize in high-energy, fast-paced edits that stop the scroll.\n\nLet's crush Q4 together.\n\n- [Your Name]"
            )
        ]
        db.session.add_all(templates)
        db.session.commit()
        print("Seeded Pitch Templates.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_pitch_templates()
    app.run(debug=True)