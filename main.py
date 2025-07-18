from server.app import app
from server.config import get_config

if __name__ == "__main__":
    config = get_config()
    app.run(host="0.0.0.0", port=5000, debug=config.server.debug)

