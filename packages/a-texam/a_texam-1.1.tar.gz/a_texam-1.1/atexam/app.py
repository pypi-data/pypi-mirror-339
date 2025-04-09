from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from datetime import datetime
from functools import wraps
from atexam.models import db, Test, Question, Answer, Result, ResultDetail, User, RegistrationRequest
from flask import send_file, render_template
from io import BytesIO
from atexam.models import Attachment
from flask_socketio import SocketIO
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask import redirect, url_for, render_template, request
from flask_login import login_user
from flask_login import current_user
from flask_login import LoginManager
import pandas as pd
from werkzeug.utils import secure_filename
import os
import webbrowser
from threading import Timer
import time
import os, random
import socket

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '12345'
app.config['ADMIN_PASSWORD'] = 'Anvarjon@_.de'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

socketio = SocketIO(app)
registration_open = True

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'avi'}

db.init_app(app)
with app.app_context():
    db.create_all()

SERVER_START_TIME = time.time()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def open_browser():
    ip = get_ip_address()
    webbrowser.open(f"http://{ip}:5000")

@app.before_request
def check_user_auth():
    allowed_routes = ['login', 'register', 'admin_login', 'static', 'about']
    if request.endpoint in allowed_routes:
        return
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if not user:
            session.clear()
            flash("Пользователь не найден, пожалуйста, войдите заново.", "error")
            return redirect(url_for('login'))
        if 'login_time' in session and session['login_time'] < SERVER_START_TIME:
            session.clear()
            flash("Пожалуйста, войдите заново.", "error")
            return redirect(url_for('login'))
    else:
        flash("Пожалуйста, войдите в систему.", "error")
        return redirect(url_for('login'))

@app.before_request
def check_if_banned():
    allowed_routes = ['logout', 'banned']
    if current_user.is_authenticated and current_user.is_banned:
        if request.endpoint is None or (request.endpoint not in allowed_routes and not request.endpoint.startswith('static')):
            return redirect(url_for('banned'))

@app.route('/banned')
def banned():
    if not current_user.is_authenticated or not current_user.is_banned:
        return redirect(url_for('index'))
    return render_template('banned.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Пожалуйста, войдите в систему для доступа к этой странице", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("Требуется пароль администратора", "error")
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
@login_required
def index():
    tests = Test.query.filter_by(is_hidden=False).all()
    username = session.get('username')
    attempts_info = {}
    for test in tests:
        if test.max_attempts:
            attempts_taken = Result.query.filter_by(user=username, test_id=test.id).count()
            remaining_attempts = test.max_attempts - attempts_taken
            attempts_info[test.id] = {"attempts_taken": attempts_taken, "remaining_attempts": remaining_attempts}
        else:
            attempts_info[test.id] = None
    show_modal = session.pop('just_logged_in', False)
    show_attempt_limit_modal = session.pop('show_attempt_limit_modal', False)
    now = datetime.now()
    return render_template('index.html', tests=tests, show_modal=show_modal,
                           show_attempt_limit_modal=show_attempt_limit_modal,
                           attempts_info=attempts_info, now=now)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == app.config.get('ADMIN_PASSWORD'):
            session['is_admin'] = True
            flash("Вход выполнен успешно", "success")
            return redirect(url_for('admin_tests'))
        else:
            flash("Неверный пароль", "error")
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash("Вы вышли из админ панели", "success")
    return redirect(url_for('admin_login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not registration_open:
        flash("Регистрация на данный момент закрыта", "warning")
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        if not username or not password:
            flash("Заполните все поля", "error")
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first() or RegistrationRequest.query.filter_by(username=username).first():
            flash("Пользователь с таким именем уже существует", "error")
            return redirect(url_for('register'))

        if username.lower() == 'admin' and password == 'Anvarjon@_.de':
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Администратор успешно зарегистрирован", "success")
            return redirect(url_for('login'))

        new_request = RegistrationRequest(username=username)
        new_request.set_password(password)
        db.session.add(new_request)
        db.session.commit()
        flash("Ваша заявка отправлена на подтверждение администратором", "success")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/admin/registration_requests')
@admin_required
def registration_requests():
    requests = RegistrationRequest.query.order_by(RegistrationRequest.created_at.desc()).all()
    return render_template('registration_requests.html', requests=requests)

@app.route('/admin/registration_requests/<int:req_id>/<action>', methods=['POST'])
@admin_required
def process_request(req_id, action):
    req = RegistrationRequest.query.get_or_404(req_id)
    if action == 'approve':
        new_user = User(username=req.username)
        new_user.password_hash = req.password_hash
        new_user.password_plain = req.password_plain
        db.session.add(new_user)
        flash(f"Пользователь {req.username} одобрен и добавлен", "success")
    elif action == 'reject':
        flash(f"Заявка {req.username} отклонена", "warning")
    else:
        flash("Неверное действие", "error")
        return redirect(url_for('registration_requests'))

    db.session.delete(req)
    db.session.commit()
    return redirect(url_for('registration_requests'))


@app.route('/admin/toggle_registration', methods=['POST'])
@admin_required
def toggle_registration():
    global registration_open
    registration_open = not registration_open
    flash("Регистрация " + ("открыта" if registration_open else "закрыта"), "success")
    return redirect(url_for('registration_requests'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            session['user_id'] = user.id
            session['username'] = user.username
            session['login_time'] = time.time()
            session['logged_in'] = True
            session['just_logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash("Неверное имя пользователя или пароль", "error")
            return redirect(url_for('login'))
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    flash("Вы вышли из системы", "success")
    return redirect(url_for('login'))

@app.route('/test/<int:test_id>', methods=['GET'])
@login_required
def test_page(test_id):
    test = Test.query.get_or_404(test_id)
    if test.is_hidden:
        flash("Данный тест недоступен.", "warning")
        return redirect(url_for('index'))
    if test.scheduled_time and datetime.now() < test.scheduled_time:
        return redirect(url_for('index'))
    if test.max_attempts:
        attempts = Result.query.filter_by(user=session.get('username'), test_id=test.id).count()
        if attempts >= test.max_attempts:
            session['show_attempt_limit_modal'] = True
            return redirect(url_for('index'))
    session_key = f"test_{test_id}_question_order"
    current_question_ids = [q.id for q in test.questions]
    if session_key in session:
        saved_ids = session[session_key]
        new_ids = [qid for qid in current_question_ids if qid not in saved_ids]
        if new_ids:
            saved_ids.extend(new_ids)
            session[session_key] = saved_ids
        question_ids = session[session_key]
    else:
        question_ids = current_question_ids.copy()
        random.shuffle(question_ids)
        session[session_key] = question_ids
    questions_dict = {q.id: q for q in test.questions}
    ordered_questions = [questions_dict[qid] for qid in question_ids if qid in questions_dict]
    return render_template('test.html', test=test, questions=ordered_questions)

@app.route('/submit_test/<int:test_id>', methods=['POST'])
@login_required
def submit_test(test_id):
    test = Test.query.get_or_404(test_id)
    total_score = 0
    user = session.get('username', 'Anonymous')
    result = Result(user=user, test_id=test.id, score=0, date_completed=datetime.utcnow())
    db.session.add(result)
    db.session.flush()
    session_key = f"test_{test_id}_question_order"
    question_ids = session.get(session_key, [])
    seen = set()
    unique_question_ids = []
    for qid in question_ids:
        if qid not in seen:
            unique_question_ids.append(qid)
            seen.add(qid)
    for question_id in unique_question_ids:
        question = Question.query.get(question_id)
        if not question:
            continue
        selected_answer_id = request.form.get(str(question.id))
        selected_answer = Answer.query.get(int(selected_answer_id)) if selected_answer_id else None
        if selected_answer and selected_answer.is_correct:
            total_score += question.points
            is_correct = True
        else:
            is_correct = False
        detail = ResultDetail(result_id=result.id, question_id=question.id,
                              user_answer_id=selected_answer.id if selected_answer else None,
                              is_correct=is_correct)
        db.session.add(detail)
    result.score = total_score
    db.session.commit()
    return redirect(url_for('result_page', result_id=result.id))

@app.route('/result/<int:result_id>')
@login_required
def result_page(result_id):
    result = Result.query.get_or_404(result_id)
    correct_count = sum(1 for detail in result.details if detail.is_correct)
    total_questions = len(result.details)
    incorrect_count = total_questions - correct_count
    return render_template('result.html', result=result, correct_count=correct_count, incorrect_count=incorrect_count)

@app.route('/history/<username>')
@login_required
def history(username):
    results = Result.query.filter_by(user=username).all()
    return render_template('history.html', results=results, username=username)

@app.route('/admin/tests')
@admin_required
def admin_tests():
    tests = Test.query.all()
    return render_template('admin_tests.html', tests=tests)

@app.context_processor
def inject_registration_status():
    return dict(registration_open=registration_open)

@app.route('/admin/toggle_test/<int:test_id>', methods=['POST'])
@admin_required
def toggle_test(test_id):
    test = Test.query.get_or_404(test_id)
    test.is_hidden = not test.is_hidden
    db.session.commit()
    flash(f"Тест {'скрыт' if test.is_hidden else 'отображается'}", "success")
    return redirect(url_for('admin_tests'))

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Пользователь удалён", "success")
    return redirect(url_for('admin_users'))

@app.route('/admin/delete_all_users', methods=['POST'])
@admin_required
def delete_all_users():
    current_admin_id = session.get('user_id')
    try:
        num_deleted = User.query.filter(User.id != current_admin_id).delete(synchronize_session=False)
        db.session.commit()
        flash(f"Удалено пользователей: {num_deleted}", "success")
    except Exception as e:
        db.session.rollback()
        flash("Ошибка при удалении пользователей.", "danger")
    return redirect(url_for('admin_users'))

@app.route('/admin/add_test', methods=['GET', 'POST'])
@admin_required
def add_test():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        scheduled_time_str = request.form.get('scheduled_time')
        if scheduled_time_str:
            scheduled_time = datetime.strptime(scheduled_time_str, "%Y-%m-%dT%H:%M")
        else:
            scheduled_time = None
        duration = int(request.form.get('duration', 30))
        max_attempts = request.form.get('max_attempts')
        if max_attempts and max_attempts.isdigit():
            max_attempts = int(max_attempts)
        else:
            max_attempts = None
        display_mode = request.form.get('display_mode', 'single')
        test = Test(title=title, description=description, scheduled_time=scheduled_time,
                    duration=duration, max_attempts=max_attempts, display_mode=display_mode)
        db.session.add(test)
        db.session.commit()
        return redirect(url_for('admin_tests'))
    return render_template('add_test.html')

@app.route('/admin/edit_test/<int:test_id>', methods=['GET', 'POST'])
@admin_required
def edit_test(test_id):
    test = Test.query.get_or_404(test_id)
    if request.method == 'POST':
        test.title = request.form.get('title')
        test.description = request.form.get('description')
        scheduled_time_str = request.form.get('scheduled_time')
        if scheduled_time_str:
            test.scheduled_time = datetime.strptime(scheduled_time_str, "%Y-%m-%dT%H:%M")
        else:
            test.scheduled_time = None
        test.duration = int(request.form.get('duration', test.duration))
        max_attempts = request.form.get('max_attempts')
        if max_attempts and max_attempts.isdigit():
            test.max_attempts = int(max_attempts)
        else:
            test.max_attempts = None
        test.display_mode = request.form.get('display_mode', 'single')
        db.session.commit()
        return redirect(url_for('admin_tests'))
    return render_template('edit_test.html', test=test)

@app.route('/admin/delete_test/<int:test_id>', methods=['POST'])
@admin_required
def delete_test(test_id):
    test = Test.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    return redirect(url_for('admin_tests'))

@app.route('/admin/add_question/<int:test_id>', methods=['GET', 'POST'])
@admin_required
def add_question(test_id):
    test = Test.query.get_or_404(test_id)
    if request.method == 'POST':
        question_text = request.form.get('question_text')
        points = int(request.form.get('points', 0))
        question = Question(test_id=test.id, question_text=question_text, points=points)
        db.session.add(question)
        db.session.commit()


        answers = []
        for i in range(1, 5):
            answer_text = request.form.get(f'answer{i}')
            if answer_text:
                answers.append(answer_text)
        correct_answer = int(request.form.get('correct_answer', 1))
        for idx, answer_text in enumerate(answers, start=1):
            is_correct = (idx == correct_answer)
            answer = Answer(question_id=question.id, answer_text=answer_text, is_correct=is_correct)
            db.session.add(answer)
        db.session.commit()


        files = request.files.getlist('attachments')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                file_type = file.content_type
                attachment = Attachment(question_id=question.id, file_path='uploads/' + filename, file_type=file_type)
                db.session.add(attachment)
        db.session.commit()

        return redirect(url_for('admin_tests'))
    return render_template('add_question.html', test=test)

@app.route('/admin/edit_question/<int:question_id>', methods=['GET', 'POST'])
@admin_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        question.question_text = request.form.get('question_text')
        question.points = int(request.form.get('points', 0))

        answers_texts = []
        for i in range(1, 5):
            answer_text = request.form.get(f'answer{i}')
            if answer_text:
                answers_texts.append(answer_text)
        correct_answer = int(request.form.get('correct_answer', 1))

        for ans in question.answers:
            db.session.delete(ans)
        db.session.commit()

        for idx, answer_text in enumerate(answers_texts, start=1):
            is_correct = (idx == correct_answer)
            answer = Answer(question_id=question.id, answer_text=answer_text, is_correct=is_correct)
            db.session.add(answer)
        db.session.commit()


        delete_ids = request.form.getlist('delete_attachments')
        for att_id in delete_ids:
            attachment = Attachment.query.get(att_id)
            if attachment:
                file_path = os.path.join(app.root_path, 'static', attachment.file_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
                db.session.delete(attachment)
        db.session.commit()

        files = request.files.getlist('attachments')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                file_type = file.content_type
                attachment = Attachment(question_id=question.id, file_path='uploads/' + filename, file_type=file_type)
                db.session.add(attachment)
        db.session.commit()

        flash("Вопрос успешно обновлен", "success")
        return redirect(url_for('admin_tests'))
    return render_template('edit_question.html', question=question)

@app.route('/admin/results')
@admin_required
def admin_results():
    results = Result.query.order_by(Result.date_completed.desc()).all()
    return render_template('admin_results.html', results=results)

@app.route('/admin/result_detail/<int:result_id>')
@admin_required
def admin_result_detail(result_id):
    result = Result.query.get_or_404(result_id)
    details = result.details
    correct_count = sum(1 for detail in details if detail.is_correct)
    total_questions = len(details)
    incorrect_count = total_questions - correct_count
    return render_template('admin_result_detail.html', result=result, details=details,
                           correct_count=correct_count, incorrect_count=incorrect_count)

@app.route('/admin/result_detail/<int:result_id>/export_excel')
@admin_required
def export_excel(result_id):
    result = Result.query.get_or_404(result_id)
    details = result.details
    data = []
    for detail in details:
        data.append({
            "ID Вопроса": detail.question.id,
            "Текст вопроса": detail.question.question_text,
            "Ответ пользователя": detail.user_answer.answer_text if detail.user_answer else "Нет ответа",
            "Правильный ответ": detail.question.correct_answer.answer_text if detail.question.correct_answer else "Не задан",
            "Результат": "Correct" if detail.is_correct else "Incorrect"
        })
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Результаты')
    output.seek(0)

    filename = f"result_{result.id}.xlsx"
    return send_file(output, download_name=filename, as_attachment=True)

@app.route('/admin/delete_result/<int:result_id>', methods=['POST'])
@admin_required
def delete_result(result_id):
    result = Result.query.get_or_404(result_id)
    db.session.delete(result)
    db.session.commit()
    flash("Результат теста удалён", "success")
    return redirect(url_for('admin_results'))

@app.route('/admin/delete_all_results', methods=['POST'])
@admin_required
def delete_all_results():
    results = Result.query.all()
    for result in results:
        db.session.delete(result)
    db.session.commit()
    flash("Вся история тестов удалена", "success")
    return redirect(url_for('admin_results'))

@app.errorhandler(404)
def page_not_found(error):
    flash("Страница не найдена", "warning")
    return redirect(url_for('index'))

@app.route('/delete_question/<int:question_id>', methods=['POST'])
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    for attachment in question.attachments:
        file_path = os.path.join(app.root_path, 'static', attachment.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    test_id = question.test_id
    db.session.delete(question)
    db.session.commit()
    flash('Вопрос успешно удалён', 'success')
    return redirect(url_for('test_questions', test_id=test_id))

class DeleteForm(FlaskForm):
    submit = SubmitField('Удалить вопрос')

@app.route('/test_questions/<int:test_id>')
def test_questions(test_id):
    test = Test.query.get_or_404(test_id)
    delete_form = DeleteForm()
    return render_template('test_questions.html', test=test, form=delete_form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin/toggle_ban/<int:user_id>', methods=['POST'])
@admin_required
def toggle_ban(user_id):
    user = User.query.get_or_404(user_id)
    user.is_banned = not user.is_banned
    db.session.commit()
    flash(f"Пользователь {user.username} {'забанен' if user.is_banned else 'разбанен'}.", 'info')
    return redirect(url_for('admin_users'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        Timer(1, open_browser).start()
    socketio.run(app, host="0.0.0.0", debug=True)
