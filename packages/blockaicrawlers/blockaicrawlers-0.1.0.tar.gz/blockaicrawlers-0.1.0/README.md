# 🤖 ConfusedAICrawlers

**ConfusedAICrawlers** is a lightweight Flask extension designed to detect and block AI web crawlers using their User-Agent strings.

It supports a customizable JSON configuration for blacklisting or whitelisting crawlers, integrates seamlessly with `flask-limiter` for rate limiting, and includes a simple admin route for reloading configurations without restarting your app.


## 🚀 Features

-  Block known AI crawlers by inspecting the `User-Agent` header.
-  Whitelist trusted crawlers (e.g., Googlebot).
-  Plug-and-play integration using a Flask Blueprint.
-  Optional `/robots.txt` route to discourage all crawlers.
-  JSON config file for flexible control.
-  Reload crawler configuration on the fly with an admin route.



## 📦 Installation

Install via pip:  ```pip install confusedaicrawlers```


## 🛠️ Usage

### 1. Basic Integration

```python
from flask import Flask
from confusedaicrawlers import FlaskAIBlocker

app = Flask(__name__)
ai_blocker = FlaskAIBlocker()  # Defaults to ai_crawlers.json
ai_blocker.init_app(app)

@app.route('/')
def index():
    return "Hello, human!"

if __name__ == '__main__':
    app.run()
```


### 2. With Flask-Limiter

```python
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from confusedaicrawlers import FlaskAIBlocker

app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

ai_blocker = FlaskAIBlocker(config_path="your_config_path.json")
ai_blocker.init_app(app)
```


## ⚙️ Configuration (JSON)

The extension expects a JSON file like this:

```json
{
  "blacklist": {
    "chatgpt": "ChatGPT",
    "openai": "OpenAI"
  },
  "whitelist": {
    "google": "Googlebot",
    "bing": "Bingbot"
  }
}
```

- **Blacklist:** Crawler fragments to block (case-insensitive).
- **Whitelist:** Allowed bots (checked first).


## 🔁 Admin Endpoint

Reload the config file at runtime without restarting the app:

```POST /admin/reload-config```

Response:

```json
{
  "status": "success",
  "message": "Configuration reloaded"
}
```

---

## 📁 Project Structure

```
confusedaicrawlers/
├── confusedaicrawlers/
│   ├── __init__.py
│   ├── blocker.py
│   └── ai_crawlers.json
├── tests/
│   └── test_blocker.py
├── README.md
├── pyproject.toml
├── requirements.txt
└── MANIFEST.in
```


## ✅ License

This project is licensed under the **MIT License**.


## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.
