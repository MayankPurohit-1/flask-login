from flask_restful import Resource
from flask import render_template, request, make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, \
    create_refresh_token, get_jwt_identity, \
    jwt_refresh_token_required, fresh_jwt_required, get_raw_jwt, get_jwt_claims, set_access_cookies, \
    set_refresh_cookies, unset_jwt_cookies
from werkzeug.security import safe_str_cmp

from Model.UserModel import User
from Blacklist import BLACKLIST
from Database.Connection import ConnectionModel


class User_Reg(Resource):
    def get(self):
        return make_response(render_template('register.html'), {"Content-Type": 'text/html'})

    def post(self):
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        usr = User(100, name, username, email, password)
        usr.user_registration()
        return "User Added Successfully"


class User_login(Resource):
    def get(self):
        return make_response(render_template('login.html'), {"Content-Type": 'text/html'})

    def post(self):
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        result = ConnectionModel.connect("user_info").find_one({"username": username})
        print(result)
        if not username:
            return jsonify({"message": "Username can't be kept empty"})

        if not password:
            return jsonify({"message": "password can't be kept empty"})

        if username and safe_str_cmp(result['password'], password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)

            # Set the JWT cookies in the response
            resp = jsonify({"login": True})
            print(type(resp))
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return make_response(resp)


class example(Resource):
    @jwt_required
    def get(self):
        curr = get_jwt_identity()
        return "hello,{}".format(curr)


class example_refresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        current = get_jwt_identity()
        access_token = create_access_token(identity=current, fresh=False)
        resp = jsonify({'refresh': True})
        set_access_cookies(resp, access_token)
        return make_response(resp), 200


class fresh_login(Resource):
    def post(self):
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if username != 'demo' or password != 'demo':
            return "bad request"
        new_token = create_access_token(identity=username, fresh=True)
        return new_token


class fresh_check(Resource):
    @fresh_jwt_required
    def get(self):
        username = get_jwt_identity()
        return {"message": "{} logged in with fresh token".format(username)}


class logout(Resource):
    def post(self):
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return make_response(resp)
        # username = get_jwt_identity()
        # jti = get_raw_jwt()['jti']
        # BLACKLIST.append(jti)
        # print(BLACKLIST)
        # # BLACKLIST.append(access_token)
        # return {"msg": "Logout successful!"}


class logout2(Resource):
    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        blacklist = get_jwt_claims()['blacklist']
        blacklist.add(jti)
        return jsonify({'msg': "successfully logout out!"})


