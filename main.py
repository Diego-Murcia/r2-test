from flask import Flask

from app.rest.library_controller import library_blueprint

app = Flask(__name__)

app.register_blueprint(library_blueprint, url_prefix='/backend/v1/library')

if __name__ == '__main__':
    app.run()
