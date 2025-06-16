from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from .. import db
from ..models import User, ActionLog
from ..forms import LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(KULLANICIADI=form.username.data).first()
        if user and user.check_password(form.password.data) and user.AKTIF:
            login_user(user, remember=form.remember_me.data)
            user.SONGIRISTARIHI = db.func.current_timestamp()
            db.session.add(ActionLog(user=user.KULLANICIADI, action='login'))
            db.session.commit()
            flash('Giri\u015f ba\u015far\u0131l\u0131', 'success')
            next_page = request.args.get('next') or url_for('main.index')
            return redirect(next_page)
        else:
            flash('Hatal\u0131 kullan\u0131c\u0131 veya \u015fifre', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    from flask_login import current_user
    db.session.add(ActionLog(user=current_user.KULLANICIADI, action='logout'))
    db.session.commit()
    logout_user()
    flash('\u00c7\u0131k\u0131\u015f yap\u0131ld\u0131', 'info')
    return redirect(url_for('auth.login'))
