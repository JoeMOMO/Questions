from flask import Flask, render_template, request,redirect,url_for,session
import config
from model import User,Question
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)



@app.route('/')
def index():
    content = {
        'questions' : Question.query.order_by('-time').all()
    }
    return render_template('index.html', **content)



@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        user = User.query.filter(User.telephone==telephone, User.password == password).first()

        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码不对，请重新登录！'



@app.route('/regist/', methods = ['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        telephone = request.form.get('telephone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()

        if user:
            return u'该手机号码已经注册！'
        else:
            if password1 != password2:
                return u'两次输入密码不一样！'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))



@app.route('/questions/', methods = ['GET', 'POST'])
@login_required
def questions():
    if request.method == 'GET':
        return render_template('questions.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        print(title)
        content = request.form.get('content')
        print(content)
        question = Question(title=title, content=content.encode('utf-8'))
        user_id = session.get('user_id')
        user = User.query.filter(User.id ==user_id).first()
        question.author = user

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
