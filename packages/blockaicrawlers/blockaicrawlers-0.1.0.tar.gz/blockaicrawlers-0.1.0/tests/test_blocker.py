import pytest
from flask import Flask
from blockedaicrawlers import FlaskAIBlocker

@pytest.fixture
def test_app():
    app = Flask(__name__)
    ai_blocker = FlaskAIBlocker(config_path='blockedaicrawlers/ai_crawlers.json')
    ai_blocker.init_app(app)

    @app.route('/')
    def index():
        return "Welcome!"

    return app

def test_block_non_ai_crawler(test_app):
    client = test_app.test_client()
    response = client.get('/', headers={'User-Agent': 'ChatGPT-UserAgent-Spoof'})
    assert response.status_code == 403
    assert b"Access Denied" in response.data

def test_allow_whitelisted_bot(test_app):
    client = test_app.test_client()
    response = client.get('/', headers={'User-Agent': 'Googlebot'})
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_missing_user_agent(test_app):
    client = test_app.test_client()
    response = client.get('/', headers={})
    assert response.status_code == 400
