#################
#### imports ####
#################

from flask import render_template, Blueprint, \
    request, flash, redirect, url_for, abort   # pragma: no cover
from flask_login import login_required, current_user   # pragma: no cover

from .forms import MessageForm   # pragma: no cover
from project import db   # pragma: no cover
from project.models import BlogPost   # pragma: no cover
from sqlalchemy import desc  # pragma: no cover

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)   # pragma: no cover


################
#### routes ####
################

# функция-обработчик запросов к главной странице
# на POST-запрос добавляет присланные пользователями сообщения
# на GET-запрос выводит главную страницу со списком сообщений
@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    try:
        error = None
        form = MessageForm(request.form)
        if form.validate_on_submit():
            new_message = BlogPost(
                form.title.data,
                form.description.data,
                current_user.id
            )
            db.session.add(new_message)
            db.session.commit()
            flash('New entry was successfully posted. Thanks.')
            return redirect(url_for('home.home'))
        else:
            posts = db.session.query(BlogPost).order_by(desc(BlogPost.id))
            return render_template(
                'index.html', posts=posts, form=form, error=error)
    except:
        return abort(401)

