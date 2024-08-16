# -*- coding: utf-8 -*-
import sys
import os

from app import create_app

# Path to the application
sys.path.insert(0, '/var/www/mail.harmonyworks.net/public_html')

# Create the application instance
application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
