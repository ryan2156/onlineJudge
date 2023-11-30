from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS

jwt = JWTManager()

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = 'adc'
app.config["ENV"] = "development"
app.config["DEBUG"] = True

jwt.init_app(app)


@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if(username == 'a' and password == 'b'):
        access_token = create_access_token(identity=username)
        return jsonify({'success': True, 'access_token': access_token})
    
    return jsonify({'success': False}), 401
    


if __name__ == "__main__":
    app.run()