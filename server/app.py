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
        data = request.get_json()

        new_scientist = Scientist(
            id=data['id'],
            name=data['name'],
            field_of_study=data['field_of_study'],
            avatar=data['avatar']
        )

        db.session.add(new_scientist)
        db.session.commit()
        return make_response(new_scientist.to_dict(), 201)
api.add_resource(Scientists, '/scientists')

class ScientistsByID(Resource):
    def get(self, id):
        scientist = Scientist.query.filter_by(id=id).first()

        if not scientist:
            return make_response({
                "errors": ["validation errors"]
            }, 404)

        scientist_dict = {
            "id": scientist.id,
            "name": scientist.name,
            "field_of_study": scientist.field_of_study,
            "avatar": scientist.avatar 
            # "planets": scientist.planets
        }

        response = make_response(
            scientist_dict,
            202
        )
        return response

    def patch(self, id):
        scientist = Scientist.query.filter_by(id=id).first()

        for attr in request.form:
            setattr(scientist, attr, request.form.get(attr))

        db.session.add(scientist)
        db.session.commit()

        scientist_dict = {
            "name": scientist.name,
            "field_of_study": scientist.field_of_study,
            "avatar": scientist.avatar
        }

        response = make_response(
            scientist_dict,
            202
        )
        return response



    # def delete(self, id):
    #     scientist = Scientist.query.filter_by(id=id).first()
    #     if not scientist:
    #         return make_response({
    #             "error": "Scientist not found"}, 404
    #         )
    #     try:
    #         db.session.delete(scientist)
    #         db.session.commit()
    #     except Exception as e:
    #         return make_response(
    #             {
    #                 "errors": [e.__str__()]
    #             },
    #             422
    #         )
    #     return make_response(
    #         "",
    #         200
     #   )
api.add_resource(ScientistsByID, '/scientists/<int:id>')


class Missions(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_mission = Mission(
                name=data['name'],
                scientist_id=data['scientist_id'],
                planet_id=data['planet_id']
            )
            db.session.add(new_mission)
            db.session.commit()
        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message, 422
            )
        return make_response(new_mission.planet.to_dict(), 201)
    
api.add_resource(Missions, '/missions')

class Planets(Resource):
    def get(self):
        planets = []
        for planet in Planet.query.all():
            planet_dict = {
                "id": planet.id,
                "name": planet.name,
                "distance_from_earth": planet.distance_from_earth,
                "nearest_star": planet.nearest_star,
                "image": planet.image
            }
            planets.append(planet_dict)

        response = make_response(
            planets,
            200
        )
        return response

api.add_resource(Planets, '/planets')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
