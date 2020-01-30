from flask_restful import Api
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, get_jwt_claims
from Resources.UserResource import User_Reg, User_login, example, example_refresh, fresh_login, fresh_check, logout, \
    logout2

from Blacklist import BLACKLIST
app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_SECRET_KEY'] = "master_key"
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api = Api(app)
jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub-status': 42,
        'msg': "the {} token has expired.".format(token_type)
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    # print(decrypted_token)
    return decrypted_token['jti'] in BLACKLIST


api.add_resource(User_Reg, '/register')
api.add_resource(User_login, '/login')
api.add_resource(example, '/example')
api.add_resource(example_refresh, '/refresh')
api.add_resource(fresh_login, '/fresh-login')
api.add_resource(fresh_check, '/check')
api.add_resource(logout, '/logout')
api.add_resource(logout2, '/logout2')
app.run(debug=True)
