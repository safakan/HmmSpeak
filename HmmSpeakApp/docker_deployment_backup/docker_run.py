from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Get port from environment variable (default to 7860 for Hugging Face Spaces)
    port = int(os.environ.get('PORT', 7860))
    # Use 0.0.0.0 to bind to all interfaces
    app.run(host='0.0.0.0', port=port, debug=False) 