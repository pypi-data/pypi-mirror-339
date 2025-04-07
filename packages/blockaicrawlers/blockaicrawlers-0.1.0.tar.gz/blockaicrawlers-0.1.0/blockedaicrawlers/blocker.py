from flask import Flask, request, Blueprint, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import json
from datetime import datetime
import os

# Setup default logger
logger = logging.getLogger("flask_ai_blocker")

class FlaskAIBlocker: # This class is a Flask extension to block AI web crawlers based on User-Agent strings.  
    def __init__(self, app=None, 
                 config_path='blockedaicrawlers/ai_crawlers.json'):
        self.app = app
        self.config_path = config_path
        self.blacklist = {}
        self.whitelist = {}
        self.blueprint = Blueprint('ai_blocker', __name__)

        # Set up the blueprint's request handler
        self.blueprint.before_app_request(self._block_ai_crawlers)
        if app is not None:
            self.init_app(app)

    def init_app(self, app): #initialize the extension with a Flask application.
        self.app = app
        self._load_config()
        app.register_blueprint(self.blueprint) #Register the blueprint with the Flask app
        
        # Add robots.txt route
        if 'robots.txt' not in [rule.rule for rule in app.url_map.iter_rules()]:
            app.add_url_rule('/robots.txt', 'robots_txt', self._robots_txt)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)


    def _load_config(self): # Load crawler configurations from JSON file.
        try:
            with open(self.config_path, 'r') as file:
                data = json.load(file)
                self.blacklist = data.get('blacklist', {})
                self.whitelist = data.get('whitelist', {})
                logger.info(f"Loaded configuration with {len(self.blacklist)} blacklist and {len(self.whitelist)} whitelist entries")
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}. Using empty lists.")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON file: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading config: {e}")


    def reload_config(self): # Reload configuration from JSON file.
        self._load_config()
        return self.blacklist, self.whitelist


    def detect_ai_crawler(self, user_agent_string): # Detect AI crawlers based on User-Agent string.
        if not user_agent_string:
            return None
        # Check whitelist first
        for name, fragment in self.whitelist.items():
            if fragment.lower() in user_agent_string.lower():
                return None
        # Then check blacklist
        for name, fragment in self.blacklist.items():
            if fragment.lower() in user_agent_string.lower():
                return name
        return None


    def _block_ai_crawlers(self): # Middleware to block AI crawlers before any request.
        try:
            user_agent = request.headers.get('User-Agent', '')
            if not user_agent:
                return make_response(jsonify({"error": "Missing User-Agent"}), 400)
            
            crawler_name = self.detect_ai_crawler(user_agent)
            if crawler_name:
                logger.info(f"Blocked AI Crawler: {crawler_name} | UA: {user_agent} | IP: {request.remote_addr} | Path: {request.path}")
                return make_response(jsonify({"error": "Access Denied", "crawler": crawler_name}), 403)
            
            return None
            
        except Exception as e:
            logger.error(f"Error in blocking middleware: {e}")
            return make_response(jsonify({"error": "Internal Server Error"}), 500)


    def _robots_txt(self): # Route handler for /robots.txt to discourage all crawlers.
        return make_response(
            "User-agent: *\nDisallow: /", 
            200, 
            {'Content-Type': 'text/plain'}
        )


#-------------------- Example usage function -----------------------------------
"""
Create a basic Flask application with AI crawler blocking.
This is an example function to demonstrate usage.
"""

def create_app(config_path='blockedaicrawlers/ai_crawlers.json'):

    app = Flask(__name__)

    # Initialize limiter
    limiter = Limiter(key_func=get_remote_address)
    limiter.init_app(app)

    # Initialize AI blocker
    ai_blocker = FlaskAIBlocker(config_path=config_path)
    ai_blocker.init_app(app)

    # Example route with rate limiting
    @app.route('/')
    @limiter.limit("10 per minute")
    def index():
        return jsonify({
            "status": "ok",
            "message": "API is operational",
            "user_agent": request.headers.get("User-Agent", "")
        })
    
    # Admin route to reload configuration
    @app.route('/admin/reload-config', methods=['POST'])
    @limiter.limit("5 per minute")
    def admin_reload_config():
        ai_blocker.reload_config()
        return jsonify({"status": "success", "message": "Configuration reloaded"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
