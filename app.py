from flask import Flask, request, make_response, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret0'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # url/route?token=mklnnjnkjn

        if not token:
            return jsonify({'message': 'Token is missing'}), 403

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms='HS256')
        except:
            return jsonify({'message': 'Token is invalid'}), 405

        return f(*args, **kwargs)
    return decorated


@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this'})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is only available for people with token'})


@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=1)}, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})

    return make_response('Could not verify!!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)
