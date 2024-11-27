from flask import Flask, redirect
from app.api import api_v1_blueprint
from part2.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprint
    app.register_blueprint(api_v1_blueprint)
    
    # Add root route that redirects to API documentation
    @app.route('/')
    def index():
        return redirect('/api/v1/')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)