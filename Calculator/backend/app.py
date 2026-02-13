"""
Scientific Calculator Backend Application

This is the main entry point for the Flask backend server.
It configures the application, registers routes, and serves the frontend.
"""

import os
import sys

# Add the project root to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.routes.calculator import calculator_bp


def create_app():
    """
    Application factory function.
    Creates and configures the Flask application.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__, static_folder=None)
    
    # Enable CORS for all routes (allows frontend to communicate with backend)
    CORS(app)
    
    # Register the calculator blueprint
    app.register_blueprint(calculator_bp)
    
    # Get the frontend directory path
    frontend_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'frontend'
    )
    
    # Serve static files (CSS, JS)
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        """Serve CSS files from frontend/css directory."""
        return send_from_directory(os.path.join(frontend_dir, 'css'), filename)
    
    @app.route('/js/<path:filename>')
    def serve_js(filename):
        """Serve JavaScript files from frontend/js directory."""
        return send_from_directory(os.path.join(frontend_dir, 'js'), filename)
    
    # Serve the main HTML file
    @app.route('/')
    def index():
        """Serve the main calculator page."""
        return send_from_directory(frontend_dir, 'index.html')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        """Health check endpoint to verify server is running."""
        return {"status": "healthy", "message": "Scientific Calculator API is running"}
    
    return app


# Create the application instance
app = create_app()


if __name__ == '__main__':
    # Run the development server
    print("=" * 50)
    print("Scientific Calculator Backend Server")
    print("=" * 50)
    print("Starting server at http://localhost:5000")
    print("API endpoints available at http://localhost:5000/api/calculator/")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
