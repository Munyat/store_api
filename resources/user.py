from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from blocklist import BLOCKLIST

from models import UserModel
from schemas import UserSchema


blp = Blueprint("User", __name__, description="Operations on Users")


@blp.route('/register')
class Register(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(name=user_data["name"])
        user.hash_password(user_data["password"])

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            abort(409, message=str(e))

        return {"message": "user created successfully"}, 201


@blp.route('/login')
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(name=user_data["name"]).first()
        if user and user.verify_password(user_data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        else:
            abort(401, message="Invalid credentials")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "user deleted"}, 200
