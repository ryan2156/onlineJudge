from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, decode_token
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os
import subprocess
from flask_login import login_user, current_user, login_required
from werkzeug.utils import secure_filename

load_dotenv()
jwt = JWTManager()
app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = 'abc'
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
    
    def update_score(self, new_score):
        self.score = new_score
        db.session.commit()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    input_format = db.Column(db.Text, nullable=False)
    output_format =   db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

@app.route("/grr", methods=['POST'])
def grr():
    data = request.get_json()
    account = data.get('account')
    access_token = create_access_token(identity=account)
    payload = decode_token(access_token)
    print(payload['sub'])
    print(create_access_token(identity=account))

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    user = Users.query.filter_by(account=account).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=account)
        payload = decode_token(access_token)
        print(payload['sub'])
        return jsonify({
            'status': 0, 
            'access_token': access_token,
            'account': account
        }), 200
    return jsonify({'status': 1}), 301

# 新增`auth`藍圖
auth_bp = Blueprint('/auth', __name__)
# 新增`/api/auth`路由進行token驗證
@auth_bp.route('/auth', methods=['POST'])
@jwt_required(optional=True) # 使用@jwt_required裝飾器保護此路由
def auth():
    data = request.get_json()
    print(data)
    token = data.get('token')
    account = data.get('account')
    print("origin: ",account)
    print("verify: ", decode_token(token)['sub'])
    
    # 驗證token
    if(account == decode_token(token)['sub']):  
        return jsonify({'status': 0, 'token': token}), 200
    else:
        return jsonify({'status': 1}), 401

# 將藍圖註冊到app
app.register_blueprint(auth_bp)

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    score = 0
    name = data.get('name')
    user = Users.query.filter_by(account=account).first()
    if user:
        return jsonify({'status': 1, 'message': 'Account already exists'}), 409

    # 創建新用戶
    new_user = Users(account, password, score, name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': 0, 'message': 'Account created successfully'}), 201

def evaluate_submission(question, user):
    err_code = 0
    command = ["python", f"uploads/Q{question}.py"]
    #import answer part
    with open(f"input/Q{question}.txt", 'r') as input_file:
        #file_content = input_file.read()
        #print(file_content)
        line = input_file.readline()
        print(line)
        while line:
            try:
                result = subprocess.run(command, input=line, stdout=subprocess.PIPE, text=True)
                output = result.stdout.strip() if result.stdout is not None else ""
                error_output = result.stderr.strip() if result.stderr is not None else ""
                print(error_output)
                if error_output:
                    print(error_output)
                    err_code = 1
                with open(f"uploads/Q{question}.txt", 'a') as output_file:
                    output_file.write(output)
                    output_file.write("\n")
                line = input_file.readline()
            except Exception as e:
                err_code = 1
                print(e)

    os.remove(f"uploads/Q{question}.py") #刪掉檔案

    with open(f"answer/Q{question}.txt", 'r', encoding='utf-8') as file1:
        content1 = file1.readlines()

    with open(f"uploads/Q{question}.txt", 'r', encoding='utf-8') as file2:
        content2 = file2.readlines()
    print(err_code)
    if content1 == content2 and err_code == 0:
        os.remove(f"uploads/Q{question}.txt")
        user.update_score(100)
        print("Success")
        return 0
    else:
        os.remove(f"uploads/Q{question}.txt")
        return 1
     #刪掉檔案

@app.route("/submit", methods=['POST'])
def submit():
    try:
        #print(123)
        #print(request.data.decode('utf-8'))
        #print(request.headers)
        data = request.get_json()
        token = data['headers']['Authorization']
        print(decode_token(token)['sub'])
        user = Users.query.filter_by(account=decode_token(token)['sub']).first()
        question_id = 1
        #question_id = request.form['ques_id']
        question_filename = f"Q{question_id}.py"  # 假设是 Python 代码
        print(123)
        code_str = data['code']
        #print(code_blob)

        #code_file_path = os.path.join("uploads", question_filename)
        with open(f"uploads/Q{question_id}.py", 'w') as code_file:
            code_file.write(code_str)

        if evaluate_submission(question_id, user) == 0:
            return jsonify({'status': 0,'message': 'Success'}), 200
        else:
            return jsonify({'status': 1,'message': 'Success'}), 201

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.debug = True
    #db.create_all()  # 確保所有的資料表都已經被創建
    #users = Users.query.all()  # 查詢 Users 表中的所有資料
    #for user in users:
    #    print(user.account)  # 打印每個用戶的帳號
    app.run()
