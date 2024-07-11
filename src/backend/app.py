from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

from packaging import version

import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'secret123'
    app.config['JWT_SECRET_KEY'] = 'secret1234'

    CORS(
        app,
        resources={r"*": {"origins": ["*"]}},
        allow_headers=["Authorization", "Content-Type", "app-version"],
        methods=["GET", "POST", "OPTIONS"],
        max_age=86400
    )

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    def check_app_version():
        @app.before_request
        def check_version():
            app_version = request.headers.get('app-version')
            if app_version and version.parse(app_version) < version.parse('1.2.0'):
                return jsonify({
                    'message': 'Please update your client application to the latest version.',
                    'current_version': app_version,
                    'required_version': '1.2.0'
                }), 426  # 426 Upgrade Required

        return None
    
    app.before_request(check_app_version())


    @app.route('/')
    def index():
        return jsonify({'status': 200})

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(
                identity={'username': user.username})
            session['auth_token'] = access_token
            session['username'] = user.username
            return jsonify({'token': access_token}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

    @app.route('/user', methods=['GET'])
    @jwt_required()
    def user():
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user['username']).first()
        if user:
            return jsonify({
                'id': user.id,
                'username': user.username
            }), 200
        return jsonify({'message': 'User not found'}), 404
    
    @app.route('/logout', methods=['GET'])
    @jwt_required()
    def logout():
        current_user = get_jwt_identity()
        if session.get('username', None) == current_user['username']:
            session.pop('username', None)
            session.pop('auth_token', None)
        return jsonify({'message': 'User logged out succesfully'}), 200

    return app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


if __name__ == '__main__':
    app = create_app()
    app.run(port=3002, debug=True)
