from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app import db, app
from models import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user, LoginManager, current_user


auth = Blueprint('auth', __name__, template_folder='templates')

# Flask-Login object
login_manager = LoginManager()
login_manager.login_view = 'auth.login' 
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    ''' Is required by Flask-login, details in docs '''
    return User.query.get(int(user_id))


@auth.route('/login', methods=('GET', 'POST'))
def login():
    ''' Retrieves data from form and tries to log user in '''
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        # Retrieve  user obj from DB, if doesn't exist - it equals to None
        user = User.query.filter(User.username==username).first()

        # If wrong username or pwd -> flash error msg
        if not user or not check_password_hash(user.password, password):
            flash('Incorrect Username or Password. Please try again.')
        else:
            login_user(user, remember=remember)
            return redirect(url_for('index'))

    # If GET request - just render template
    return render_template('login.html')


@auth.route('/register', methods=('GET', 'POST'))
def register():
    ''' Retrieves data from form and tries to register user '''

    if request.method == 'POST':
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))
        secret_q = request.form.get('secret_q')
        secret_q_ans = request.form.get('secret_q_ans')

        try:
            new_user = User(username=username, password=password,
                            secret_q=secret_q, secret_q_ans=secret_q_ans)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            flash('Something went wrong. Please try again...')

    # if get request - just render template
    return render_template('register.html')


@auth.route('/logout')
def logout():
    ''' If user is logged in - loggs him out '''
    logout_user()
    return redirect(url_for('index'))


@auth.route('/_reset_pwd')
def reset_pwd():
    
    data = {
        'status': 'success',
        'done': False
    }

    username = request.args.get('username')
    step = request.args.get('step')

    user = User.query.filter(User.username==username).first()

    if step == '1':
        if user:
            data['secret_q'] = user.secret_q
            data['done'] = True
    elif step == '2':
        answer = request.args.get('secret_q_ans')
        if answer == user.secret_q_ans:
            data['done'] = True
    elif step == '3':
        new_password = request.args.get('new_pwd')
        user.password = generate_password_hash(new_password)
        db.session.commit()
        data['done'] = True


    return jsonify(data)

@auth.route('/_new_password')
def new_password():
    old_password = request.args.get('old_password')
    new_password = request.args.get('new_password')
    user = User.query.filter(User.username==current_user.username).first()
    if check_password_hash(user.password, old_password):
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@auth.route('/get_secret')
def get_secret():
    ''' returns the secret question the given user '''
    username = request.args.get('username')
    return User.query.filter(User.username==username).secret_q


@auth.route('/check_secret')
def check_secret():
    ''' checks whether the given answer for a secret_q is valid '''
    username = request.args.get('username')
    secret_q_ans = request.args.get('username')
    return User.query.filter(User.username==username).secret_q_ans == secret_q_ans


@auth.route('/change_pass')
def change_pass():
    ''' change password '''
    username = request.args.get('username')
    new_password = request.args.get('new_password')
    return User.query.filter(User.username==username).password = generate_password_hash(new_password)

# business logic
# use get_secret  to get secret_q of the specific user
# use check_secret to chech whether the given answer if valid for a given user
# use change_pass to change pass to the new one
# in-view logic: we give a secret question to user, then we check the answer with check_secret, if check_secret return True - then we change_pass
#