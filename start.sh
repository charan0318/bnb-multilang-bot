
#!/bin/bash

# Install dependencies for Render deployment
pip install -r requirements-render.txt

# Set production environment
export FLASK_ENV=production

# Start the application with Gunicorn for production
if command -v gunicorn &> /dev/null; then
    echo "Starting with Gunicorn (production mode)..."
    gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --timeout 120 --keep-alive 2 --max-requests 1000 --preload wsgi:application
else
    echo "Gunicorn not found, starting with Flask development server..."
    python main.py
fi
