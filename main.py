"""
================================================================================
TheDraftClinic - Main Application Entry Point
================================================================================
By MOA Digital Agency LLC
Developed by: Aisance KALONJI
Contact: moa@myoneart.com
Website: www.myoneart.com
================================================================================

This is the main entry point for the TheDraftClinic Flask application.
It creates the application instance and runs the development server.
================================================================================
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
