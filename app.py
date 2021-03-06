from flask import Flask
from flask_restful import Api
from resources.item import Item, ItemList
from db import db
import os


def get_database_url():
    data_base_url = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    return data_base_url.replace("postgres", "postgresql")


def create_app():
    app = Flask(__name__, static_url_path='')
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api = Api(app)
    api.add_resource(ItemList, '/items')
    api.add_resource(Item, '/items/<item_id>')
    @app.before_first_request

    def create_tables():
        db.create_all()

    @app.route('/')
    def root():
        return app.send_static_file('index.html')
    return app


def init_db(app):
    db.init_app(app)


app = create_app()
init_db(app)


if __name__ == '__main__':
    app.run(debug=True, port=443)
