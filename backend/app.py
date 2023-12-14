from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user, login_required

load_dotenv()
jwt = JWTManager()
app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
jwt.init_app(app)

class Users(db.Model):
    __tablename__ = "Users"
    #id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, account, password, score, name):
        self.account = account
        self.set_password(password)
        self.score = score
        self.name = name

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password
    
    def __repr__(self):
        return 'account:%s, password:%s' % (self.account, self.password)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    input_format = db.Column(db.Text, nullable=False)
    output_format = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    user = Users.query.filter_by(account=account).first()
    print(user)
    print(account,password)
    if user and user.check_password(password):
        access_token = create_access_token(identity=account)
        return jsonify({
            'status': 0, 
            'access_token': access_token,
            'account': account
        })
    return jsonify({'status': 1}), 301

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    score = 0
    name = data.get('name')
    user = Users.query.filter_by(account=account).first()
    if user:
        return jsonify({'status': 1, 'message': 'Account already exists'}), 400

    # 創建新用戶
    new_user = Users(account, password, score, name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': 0, 'message': 'Account created successfully'}), 201

@app.route("/submit", methods=['POST'])
def submit():
    data = request.get_json()
    question_number = data.get('question_number')
    cpp_code = data.get('cpp_code')

    # 將程式碼寫入一個.cpp檔案
    with open('code.cpp', 'w') as file:
        file.write(cpp_code)

    # 編譯程式碼
    compile_result = subprocess.run(['g++', 'code.cpp', '-o', 'code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if compile_result.returncode != 0:
        return jsonify({'status': 1, 'message': 'Compilation error', 'error': compile_result.stderr.decode()}), 400

    # 執行程式碼並捕獲輸出
    run_result = subprocess.run(['./code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run_result.returncode != 0:
        return jsonify({'status': 1, 'message': 'Runtime error', 'error': run_result.stderr.decode()}), 400

    # 在這裡添加程式碼的評估邏輯
    run_result.stdout.decode()

    return jsonify({'status': 0, 'message': 'Code submitted successfully', 'output': run_result.stdout.decode()}), 201

if __name__ == "__main__":
    app.debug = True
    #db.create_all()  # 確保所有的資料表都已經被創建
    #users = Users.query.all()  # 查詢 Users 表中的所有資料
    #for user in users:
    #    print(user.account)  # 打印每個用戶的帳號
    app.run()
