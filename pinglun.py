from flask import Flask, render_template, request,redirect,url_for,session
import config
from model import User,Question,Comment
from exts import db
from decorators import login_required
from sqlalchemy import or_

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

@app.route('/comment/',methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('comment-content')
    question_id = request.form.get('question_id')

    comment = Comment(content= content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    question = Question.query.filter(Question.id == question_id).first()
    comment.question = question

    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('detail', question_id = question_id))

@app.route('/search/')
def search():
    search_str = request.args.get('q')
    question = Question.query.filter(or_(Question.title.contains(search_str), Question.content.contains(search_str))).order_by('-time')
    if question:
        return render_template('index.html', questions = question)

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

@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
   # question_model.content = question_model.content.replace(" ","&nbsp;").replace("/\n|\r\n","<br>")
    return render_template('detail.html', question_model = question_model)

@app.route('/logout/')
def logout():
    session.clear()
    return  redirect(url_for('login'))


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

@app.context_processor
def my_context_processor():
    if session.get('user_id'):
        user = User.query.filter(User.id == session.get('user_id')).first()
        return {'user': user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
