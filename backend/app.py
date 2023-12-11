from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from models.users import Users, db

from dotenv import load_dotenv
import os
load_dotenv() # 引入環境變數設定

jwt = JWTManager()

# 跨域連線、jwt初始化
app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["ENV"] = "development"
app.config["DEBUG"] = True
jwt.init_app(app)

# 資料庫設定
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    print(data)
    
    user = Users.query.filter_by(account=account).first()

    # 检查用户是否存在以及密码是否正确
    if(user and user.check_password(password)):
        # 创建 JWT 访问令牌
        access_token = create_access_token(identity=account)
        return jsonify({
            'status': 0, 
            'access_token': access_token
        })
    return jsonify({'status': 0}), 402
    


if __name__ == "__main__":
    app.run()