from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Scientist, Planet, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

# @app.route('/')
# def index():
#     response = make_response(
#         {"message": "Hello Scientists!"}
#     )
#     return response

class Scientists(Resource):
    def get(self):
        scientists = []
        for scientist in Scientist.query.all():
            scientist_dict = {
                "id": scientist.id,
                "name": scientist.name,
                "field_of_study": scientist.field_of_study,
                "avatar": scientist.avatar
            }
            scientists.append(scientist_dict)

        response = make_response(
            scientists,
            200
        )
        return response
    
    def post(self):
        pass

api.add_resource(Scientists, '/scientists')

class ScientistsByID(Resource):
    def get(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({
                "error": "Scientist not found"
            }, 404)
        response = make_response(
            scientist.to_dict(rules = ('planets',)),
            200
        )
        return response

    def patch(self, id):
        pass
    def delete(self, id):
        pass
api.add_resource(ScientistsByID, '/scientists/<int:id>')

# class Planets(Resource):
#     def get(self):
#         pass
# api.add_resource(Planets, '/planets')

# class Missions(Resource):
#     def post(self):
#         data = request.get_json()
#         try:
#             new_mission = Mission(
#                 name=data['name'],
#                 scientist_id=data['scientist_id'],
#                 planet_id=data['planet_id']
#             )
#             db.session.add(new_mission)
#             db.session.commit()
#         except Exception as e:
#             message = {
#                 "errors": ["validation errors"]
#             }
#             return make_response(
#                 message, 422
#             )
#         return make_response(new_mission.to_dict(), 201)
# api.add_resource(Missions, '/missions')
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
