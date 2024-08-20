import os
from app import create_app

application = create_app()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    application.run(debug=debug_mode, host='0.0.0.0', port=5001)