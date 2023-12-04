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
    account = data.get('account')
    password = data.get('password')
    print(data)
    if(account == 'a' and password == 'b'):
        access_token = create_access_token(identity=account)
        return jsonify({
            'status': 0, 
            'access_token': access_token
        })
    
    return jsonify({'status': 1}), 402
    


if __name__ == "__main__":
    app.run()