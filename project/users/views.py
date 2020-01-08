#################
#### imports ####
#################

from flask import flash, redirect, render_template, request, \
    url_for, Blueprint   # pragma: no cover
from flask_login import login_user, \
    login_required, logout_user   # pragma: no cover

from .forms import LoginForm, RegisterForm # pragma: no cover
from project import db # pragma: no cover
from project.models import User, bcrypt # pragma: no cover

################
#### config ####
################

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
) # pragma: no cover

################
#### routes ####
################
# функция-обработчик запросов к форме входа:
# на POST-запрос проверяет присланные логин и пароль и вводит пользователя в систему
# на GET-запрос выводит страницу входа в систему
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(
                user.password, request.form['password']
            ):
                login_user(user)
                flash('You were logged in. Go Crazy.')
                return redirect(url_for('home.home'))

            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


# функция-обработчик запросов на выход из системы:
# требует, чтобы текущий пользователь был авторизован
# выводит пользователя в систему
@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('home.home'))


# функция-обработчик запросов к форме регистрации:
# на POST-запрос проверяет присланные данные, регистрирует и вводит пользователя в систему
# на GET-запрос выводит страницу регистрации
@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home.home'))
    return render_template('register.html', form=form)
