from flask import Flask

from start.posts.views import posts_blueprint
from start.api.views import api_blueprint
from start import logger

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

logger.create_logger()

app.register_blueprint(posts_blueprint)
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run()


