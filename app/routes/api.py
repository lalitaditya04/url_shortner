from flask import Blueprint, jsonify, request
from app.models import URL
from app.utils import validate_url

api_bp = Blueprint('api', __name__)

@api_bp.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    url = data['url']
    is_valid, message = validate_url(url)
    if not is_valid:
        return jsonify({'error': message}), 400

    # Check for custom short code
    short_code = data.get('short_code')
    if short_code:
        existing_url = URL.get_by_short_code(short_code)
        if existing_url:
            return jsonify({'error': 'Short code already in use'}), 400

    url_data = URL.create(url, short_code)
    return jsonify(url_data), 201


@api_bp.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    url_data = URL.get_by_short_code(short_code)
    if not url_data:
        return jsonify({'error': 'URL not found'}), 404

    return jsonify(url_data), 200


@api_bp.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    url = data['url']
    is_valid, message = validate_url(url)
    if not is_valid:
        return jsonify({'error': message}), 400

    success = URL.update(short_code, url)
    if not success:
        return jsonify({'error': 'URL not found'}), 404

    url_data = URL.get_by_short_code(short_code)
    return jsonify(url_data), 200


@api_bp.route('/shorten/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    success = URL.delete(short_code)
    if not success:
        return jsonify({'error': 'URL not found'}), 404

    return '', 204


@api_bp.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    url_data = URL.get_by_short_code(short_code)
    if not url_data:
        return jsonify({'error': 'URL not found'}), 404

    return jsonify(url_data), 200
