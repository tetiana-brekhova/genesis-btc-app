from flask import Blueprint, request, jsonify
from models import Subscription, db
from services.exchange_rate_service import get_current_rate
from services.email_service import send_email

bp = Blueprint('routes', __name__)

@bp.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email')
    if email:
        subscription = Subscription(email=email)
        db.session.add(subscription)
        db.session.commit()
        return jsonify({'message': 'Subscribed successfully'}), 200
    return jsonify({'error': 'Email is required'}), 400

@bp.route('/api/rate', methods=['GET'])
def rate():
    c_rate = get_current_rate()
    return jsonify({'rate': c_rate}), 200


