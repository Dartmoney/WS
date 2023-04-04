from . import db_session
from .solo_zayavki import Solo_zayavka
from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from .informationUser import InformationUser


def abort_if_zayavka_not_found(zayavka_id):
    session = db_session.create_session()
    zayavka = session.query(Solo_zayavka).get(zayavka_id)
    if not zayavka:
        abort(404, message=f"Zayavka {zayavka_id} not found")


class Zayavka_Resource(Resource):
    def get(self, zayavka_id):
        abort_if_zayavka_not_found(zayavka_id)
        session = db_session.create_session()
        zayavka = session.query(Solo_zayavka).get(zayavka_id)
        return jsonify({'zayavka': zayavka.to_dict()})

    def delete(self, zayavka_id):
        abort_if_zayavka_not_found(zayavka_id)
        session = db_session.create_session()
        zayavka = session.query(Solo_zayavka).get(zayavka_id)
        session.delete(zayavka)
        session.commit()

    def put(self, zayavka_id):
        abort_if_zayavka_not_found(zayavka_id)
        session = db_session.create_session()
        zayavka = session.query(Solo_zayavka).get(zayavka_id)
        zayavka.odobrena = True
        session.add(zayavka)
        session.commit()
        return jsonify({'zayavka': zayavka.to_dict()})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)


class Zayavka_list_Resource(Resource):
    def get(self):
        session = db_session.create_session()
        zayavki = session.query(Solo_zayavka).all()
        return jsonify({'zayavki': [item.to_dict() for item in zayavki]})
