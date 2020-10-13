from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sites.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Sites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(32), unique=True)
    site_risk = db.Column(db.String(32))

    def __init__(self, site_name, site_risk):
        self.site_name = site_name
        self.site_risk = site_risk


class SiteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'site_name', 'site_risk')


site_schema = SiteSchema()
sites_schema = SiteSchema(many=True)


class SiteManager(Resource):
    @staticmethod
    def get():
        try:
            id = request.args['id']
        except Exception as _:
            id = None

        if not id:
            users = Sites.query.all()
            return jsonify(sites_schema.dump(users))
        user = site_schema.query.get(id)
        return jsonify(sites_schema.dump(user))

    @staticmethod
    def post():
        site_name = request.json['site']
        site_risk = request.json['password']

        site = Sites(site_name, site_risk)
        db.session.add(site)
        db.session.commit()

        return jsonify({
            'Message': f'Site {site_name}  inserted.'
        })







