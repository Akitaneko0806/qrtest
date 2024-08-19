import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('/var/www/mail.harmonyworks.net/public_html/logs/flask_app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug("This is a test log message.")


from app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5001)
