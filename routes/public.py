from flask import render_template, request, jsonify, current_app
from extensions import db, limiter
from models import Lead, PitchTemplate, BaseRate, NicheMultiplier, ExperienceMultiplier, UsageRight
from schemas import CalculationSchema, LeadSchema
from marshmallow import ValidationError
import random

def register(app):
    @app.route('/')
    def index():
        # Fetch active pricing data for the frontend form
        base_rates = BaseRate.query.order_by(BaseRate.sort_order).all()
        niches = NicheMultiplier.query.order_by(NicheMultiplier.sort_order).all()
        experiences = ExperienceMultiplier.query.order_by(ExperienceMultiplier.sort_order).all()
        usage_rights = UsageRight.query.order_by(UsageRight.sort_order).all()
        
        return render_template('index.html', 
                               base_rates=base_rates, 
                               niches=niches, 
                               experiences=experiences, 
                               usage_rights=usage_rights)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/terms')
    def terms():
        return render_template('terms.html')

    @app.route('/calculate', methods=['POST'])
    @limiter.limit("20 per minute") 
    def calculate():
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        # Note: We rely on frontend to send valid slugs derived from DB
        
        try:
            # CHANGED: content_type is now a list
            c_type_slugs = json_data.get('content_type', [])
            if isinstance(c_type_slugs, str): c_type_slugs = [c_type_slugs] # Handle legacy single string if sent
            
            exp_slug = json_data.get('experience_level')
            niche_slug = json_data.get('niche')
            usage_slugs = json_data.get('usage_rights', [])

            # 1. Calculate Total Base Rate (Sum of all selected types)
            total_base_price = 0
            base_breakdown = []
            
            for slug in c_type_slugs:
                base_obj = BaseRate.query.filter_by(slug=slug).first()
                if base_obj:
                    total_base_price += base_obj.base_price
                    base_breakdown.append(base_obj.name)
            
            # Fallback if nothing found (shouldn't happen with validation)
            if total_base_price == 0: total_base_price = 150

            # 2. Multipliers
            exp_obj = ExperienceMultiplier.query.filter_by(slug=exp_slug).first()
            niche_obj = NicheMultiplier.query.filter_by(slug=niche_slug).first()
            
            exp_factor = exp_obj.multiplier if exp_obj else 1.0
            niche_factor = niche_obj.multiplier if niche_obj else 1.0
            
            # Logic: (Sum of Bases) * Exp * Niche
            adjusted_base = total_base_price * exp_factor * niche_factor
            
            # 3. Usage Rights
            total_usage_percent = 0.0
            usage_breakdown = []
            
            for u_slug in usage_slugs:
                u_obj = UsageRight.query.filter_by(slug=u_slug).first()
                if u_obj:
                    cost = adjusted_base * u_obj.multiplier
                    total_usage_percent += u_obj.multiplier
                    usage_breakdown.append({
                        'name': u_obj.name,
                        'rate': u_obj.multiplier,
                        'cost': int(cost)
                    })
            
            total_usage_cost = adjusted_base * total_usage_percent
            total_val = adjusted_base + total_usage_cost
            
            return jsonify({
                'min_price': int(total_val),
                'max_price': int(total_val * 1.2),
                'breakdown': {
                    'base_rate': int(total_base_price),
                    'selected_types': base_breakdown, # Send names back for UI
                    'niche_factor': niche_factor,
                    'exp_factor': exp_factor,
                    'adjusted_base': int(adjusted_base),
                    'usage_items': usage_breakdown,
                    'total_usage_cost': int(total_usage_cost)
                }
            })
        except Exception as e:
            current_app.logger.error(f"Calculation Error: {str(e)}")
            return jsonify({"error": "Internal calculation error"}), 500

    @app.route('/api/pitch/generate', methods=['POST'])
    @limiter.limit("10 per minute")
    def generate_pitch():
        try:
            data = request.get_json() or {}
            mood = data.get('mood', 'professional')
            niche_slug = data.get('niche', 'lifestyle')
            
            niche_obj = NicheMultiplier.query.filter_by(slug=niche_slug).first()
            niche_name = niche_obj.name if niche_obj else "our industry"
            clean_niche = niche_name.split(' ', 1)[1] if ' ' in niche_name else niche_name

            templates = PitchTemplate.query.filter_by(mood=mood).all()
            if not templates:
                templates = PitchTemplate.query.all()
                
            selected = random.choice(templates)
            content = selected.content.replace('{product_type}', f"{clean_niche} products")
            
            return jsonify({"content": content})
        except Exception:
            return jsonify({"error": "Could not generate pitch"}), 500

    @app.route('/api/lead', methods=['POST'])
    @limiter.limit("5 per minute")
    def save_lead():
        try:
            json_data = request.get_json()
            schema = LeadSchema()
            data = schema.load(json_data)

            existing = Lead.query.filter_by(email=data['email']).first()
            if not existing:
                lead = Lead(email=data['email'], updated_by="user_submission")
                db.session.add(lead)
                db.session.commit()
            return jsonify({'status': 'success'})
        except ValidationError as err:
            return jsonify(err.messages), 400
        except Exception:
            db.session.rollback()
            return jsonify({'error': 'Database error'}), 500