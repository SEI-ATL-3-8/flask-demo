from sqlalchemy import exc as db_errors

from flask import Flask, request, jsonify
app = Flask(__name__)

import os

from dotenv import load_dotenv
load_dotenv()
if os.environ.get('ENV') == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')

import models
models.db.init_app(app)

# @app.route('/', methods=["GET", "POST", "PUT", "DELETE"])
def root():
    print(f"!!! {request.method}")
    return "hello from root!"
app.route('/', methods=["GET", "POST", "PUT", "DELETE"])(root)


def param(id):
    return f"you said {id}"
app.route('/param/<string:id>')(param)

def post_test():
    print(request.json["bing"])
    print(request.headers["Authorization"])
    return "post_test"
app.route('/post_test', methods=["POST"])(post_test)

def json_test():
    return {
        "json": "test"
    }
app.route('/json_test')(json_test)

def user_test():
    if request.method == "GET":
        users = models.User.query.all()
        return jsonify(users=[u.to_json() for u in users])
    elif request.method == "POST":
        try:
            user = models.User(email=request.json["email"], password=request.json["password"])
            models.db.session.add(user)
            models.db.session.commit()
            return user.to_json()
        except db_errors.IntegrityError as e:
            return { "error": "Email is taken" }, 400
app.route('/user_test', methods=["GET", "POST"])(user_test)

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port, debug=True)


