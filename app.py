from flask import Flask, request, jsonify, redirect, render_template
from flask_cors import CORS

from config import current_config
from services.url_service import UrlService

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(current_config)
CORS(app)

# Initialize URL service
url_service = UrlService()

# API Endpoints

@app.route('/shorten', methods=['POST'])
def create_short_url():
    """Create a new short URL."""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        created_url = url_service.create_url(data['url'])
        return jsonify(created_url), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred while creating the URL'}), 500

@app.route('/shorten/<shortcode>', methods=['GET'])
def get_url(shortcode):
    """Get a URL by its shortcode."""
    url_doc = url_service.get_url_by_shortcode(shortcode)
    
    if url_doc:
        return jsonify(url_doc), 200
    else:
        return jsonify({'error': 'URL not found'}), 404

@app.route('/shorten/<shortcode>', methods=['PUT'])
def update_url(shortcode):
    """Update a URL by its shortcode."""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        updated_url = url_service.update_url_by_shortcode(shortcode, data['url'])
        
        if updated_url:
            return jsonify(updated_url), 200
        else:
            return jsonify({'error': 'URL not found'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred while updating the URL'}), 500

@app.route('/shorten/<shortcode>', methods=['DELETE'])
def delete_url(shortcode):
    """Delete a URL by its shortcode."""
    deleted = url_service.delete_url_by_shortcode(shortcode)
    
    if deleted:
        return '', 204
    else:
        return jsonify({'error': 'URL not found'}), 404

@app.route('/shorten/<shortcode>/stats', methods=['GET'])
def get_url_stats(shortcode):
    """Get statistics for a URL by its shortcode."""
    url_stats = url_service.get_url_stats(shortcode)
    
    if url_stats:
        return jsonify(url_stats), 200
    else:
        return jsonify({'error': 'URL not found'}), 404

@app.route('/<shortcode>', methods=['GET'])
def redirect_to_url(shortcode):
    """Redirect to the original URL."""
    original_url = url_service.increment_access_count(shortcode)
    
    if original_url:
        return redirect(original_url)
    else:
        return jsonify({'error': 'URL not found'}), 404

# Frontend routes

@app.route('/', methods=['GET'])
def index():
    """Render the home page."""
    return render_template('index.html')

# Error handlers

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 