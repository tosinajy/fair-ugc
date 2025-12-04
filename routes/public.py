from flask import render_template, request, jsonify
from extensions import db, limiter
from models import Lead, PricingConfig, PitchTemplate
from schemas import CalculationSchema, LeadSchema
from marshmallow import ValidationError
import random

def get_price_config(key, default=0.0):
    """Helper to safely fetch pricing variables from DB."""
    try:
        conf = PricingConfig.query.filter_by(key=key).first()
        return float(conf.value) if conf else default
    except Exception:
        return default

def register(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/calculate', methods=['POST'])
    @limiter.limit("20 per minute") 
    def calculate():
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No input data provided"}), 400

        schema = CalculationSchema()
        try:
            data = schema.load(json_data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        try:
            # Extract Data
            c_type = data['content_type']
            exp_level = data['experience_level']
            niche = data['niche']
            usage_list = data['usage_rights']
            
            # Logic
            base_rate = get_price_config(f'base_{c_type}', 50.0)
            exp_mult = get_price_config(f'mult_exp_{exp_level}', 0.0)
            niche_mult = get_price_config(f'mult_niche_{niche}', 0.0)
            
            adjusted_base = base_rate + (base_rate * exp_mult) + (base_rate * niche_mult)
            
            total_usage_fee = 0.0
            for right in usage_list:
                u_percent = get_price_config(f'usage_{right}', 0.0)
                total_usage_fee += (adjusted_base * u_percent)
            
            total_val = adjusted_base + total_usage_fee
            
            return jsonify({
                'min_price': int(total_val),
                'max_price': int(total_val * 1.2)
            })
        except Exception as e:
            app.logger.error(f"Calculation Error: {str(e)}")
            return jsonify({"error": "Internal calculation error"}), 500

    @app.route('/api/pitch/generate', methods=['POST'])
    @limiter.limit("10 per minute")
    def generate_pitch():
        try:
            data = request.get_json() or {}
            mood = data.get('mood', 'professional')
            
            templates = PitchTemplate.query.filter_by(mood=mood).all()
            if not templates:
                templates = PitchTemplate.query.all()
                
            if not templates:
                return jsonify({"content": "Hi {brand_name}, let's work together!"})
                
            selected = random.choice(templates)
            return jsonify({"content": selected.content})
        except Exception as e:
            return jsonify({"error": "Could not generate pitch"}), 500

    @app.route('/api/lead', methods=['POST'])
    @limiter.limit("5 per minute")
    def save_lead():
        try:
            json_data = request.get_json()
            schema = LeadSchema()
            data = schema.load(json_data)

            lead = Lead(email=data['email'], updated_by="user_submission")
            db.session.add(lead)
            db.session.commit()
            return jsonify({'status': 'success'})
        except ValidationError as err:
            return jsonify(err.messages), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Database error'}), 500