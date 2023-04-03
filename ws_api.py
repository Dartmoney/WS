import flask
from data.user import User
from data import db_session
from flask import jsonify
from data.solo_zayavki import Solo_zayavka
blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(Solo_zayavka).all()
    return jsonify(
        {
            'zayavki':
                [item.to_dict()
                 for item in news]
        }
    )