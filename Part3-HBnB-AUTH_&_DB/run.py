"""Development server"""
import os
from dotenv import load_dotenv

load_dotenv()

print("HBNB_MYSQL_USER:", os.getenv('HBNB_MYSQL_USER'))
print("HBNB_MYSQL_PWD:", os.getenv('HBNB_MYSQL_PWD'))
print("HBNB_MYSQL_HOST:", os.getenv('HBNB_MYSQL_HOST'))
print("HBNB_MYSQL_DB:", os.getenv('HBNB_MYSQL_DB'))

from api.v1.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)