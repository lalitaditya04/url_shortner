from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import URL
from app.utils import validate_url
from datetime import datetime

views_bp = Blueprint('views', __name__)


@views_bp.route('/')
def index():
    return render_template('index.html')


@views_bp.route('/dashboard')
def dashboard():
    # In a real app, you'd paginate this
    urls = list(URL.get_all())
    return render_template('dashboard.html', urls=urls)


@views_bp.route('/delete/<short_code>', methods=['POST'])
def delete_url(short_code):
    URL.delete(short_code)  # Implement this in your model
    flash('URL deleted successfully!', 'success')
    return redirect(url_for('views.dashboard'))


@views_bp.route('/<short_code>')
def redirect_to_url(short_code):
    url_data = URL.get_by_short_code(short_code)
    if not url_data:
        return render_template('404.html'), 404

    URL.increment_access_count(short_code)
    return redirect(url_data['url'])


@views_bp.route('/create', methods=['POST'])
def create_short_url():
    original_url = request.form.get('url')
    custom_code = request.form.get('custom_code')

    is_valid, message = validate_url(original_url)
    if not is_valid:
        flash(message, 'danger')
        return render_template('index.html')  # direct render for immediate feedback

    try:
        url_data = URL.create(original_url, custom_code)
        short_url = f"{request.host_url}{url_data['short_code']}"
        flash('Short URL created successfully!', 'success')
        return render_template('index.html', short_url=short_url, original_url=original_url)
    except Exception as e:
        flash(str(e), 'danger')
        return render_template('index.html')


@views_bp.route('/update/<short_code>', methods=['POST'])
def update_url(short_code):
    new_url = request.form.get('url')

    is_valid, message = validate_url(new_url)
    if not is_valid:
        flash(message, 'danger')
        return redirect(url_for('views.edit_url', short_code=short_code))

    success = URL.update(short_code, new_url)
    if success:
        flash('URL updated successfully!', 'success')
    else:
        flash('No changes made or URL not found.', 'warning')

    return redirect(url_for('views.dashboard'))


@views_bp.route('/edit/<short_code>', methods=['GET'])
def edit_url(short_code):
    url_data = URL.get_by_short_code(short_code)
    if not url_data:
        flash('URL not found', 'danger')
        return redirect(url_for('views.dashboard'))

    return render_template('edit.html', url_data=url_data)
