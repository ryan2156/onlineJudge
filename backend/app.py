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

@app.route("/submit", methods=['POST'])
def submit():
    print(request.headers['ques_id'])
    code_blob = request.data
    print(code_blob.decode('utf-8'))
    #print(request.files)
    #if 'file' not in request.files:
    #    return jsonify({'error': 'No file part'}), 888

    #file = request.files['file']
    question = request.form['ques_id']
    #token = decode_token(request.form['Authorization'])['sub']
    print(question)
    #user = Users.query.filter_by(account=token).first()
    code_str = code_blob.decode('utf-8')
    print(code_str)
    #if file.filename == '':
    #    return jsonify({'error': 'No selected file'}), 405

    #filename = secure_filename(file.filename)
    #upload_folder = os.path.join(os.getcwd(), 'uploads')
    #os.makedirs(upload_folder, exist_ok=True) #確保資料夾存在
#
    #file_path = os.path.join(upload_folder, file.filename)
    #file.save(file_path)
#
    #command = ["python", file.filename]
    ##import answer part
    #with open(f"input/Q{question}.txt", 'r') as input_file:
    #    #file_content = input_file.read()
    #    #print(file_content)
    #    line = input_file.readline()
    #    while line:
    #        result = subprocess.run(command, input=line, stdout=subprocess.PIPE, text=True)
    #        output = result.stdout.strip()
    #        with open(f"uploads/Q{question}.txt", 'a') as output_file:
    #            output_file.write(output)
    #            output_file.write("\n")
    #        line = input_file.readline()
#
    #os.remove(file_path) #刪掉檔案
#
    #with open(f"answer/Q{question}.txt", 'r', encoding='utf-8') as file1:
    #    content1 = file1.readlines()
#
    #with open(f"uploads/Q{question}.txt", 'r', encoding='utf-8') as file2:
    #    content2 = file2.readlines()
#
    #if content1 == content2:
    #    user.update_score(100)
    #    print("Success")
#
    #return jsonify({'message': 'Success'}), 200
    #
#    data = request.get_json()
#    question_number = data.get('question_number')
#    cpp_code = data.get('cpp_code')
#
#    # 將程式碼寫入一個.cpp檔案
#    with open('code.cpp', 'w') as file:
#        file.write(cpp_code)
#
#    # 編譯程式碼
#    compile_result = subprocess.run(['g++', 'code.cpp', '-o', 'code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    if compile_result.returncode != 0:
#        return jsonify({'status': 1, 'message': 'Compilation error', 'error': compile_result.stderr.decode()}), 400
#
#    # 執行程式碼並捕獲輸出
#    run_result = subprocess.run(['./code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    if run_result.returncode != 0:
#        return jsonify({'status': 1, 'message': 'Runtime error', 'error': run_result.stderr.decode()}), 400
#
#    # 在這裡添加程式碼的評估邏輯
#    run_result.stdout.decode()
#
#    return jsonify({'status': 0, 'message': 'Code submitted successfully', 'output': run_result.stdout.decode()}), 201




if __name__ == "__main__":
    app.debug = True
    #db.create_all()  # 確保所有的資料表都已經被創建
    #users = Users.query.all()  # 查詢 Users 表中的所有資料
    #for user in users:
    #    print(user.account)  # 打印每個用戶的帳號
    app.run()
