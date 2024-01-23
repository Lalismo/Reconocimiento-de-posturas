from fastapi import Cookie
from flask import render_template, redirect, session, url_for, flash
from app.forms import LoginForm
from . import auth
from app.firestore_service import get_user_by_id, user_put_data, get_type
from app.models import UserModel, UserData
from flask_login import login_user,login_required,logout_user, user_logged_out
from werkzeug.security import generate_password_hash, check_password_hash

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form' : login_form,
    } 
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        email = login_form.email.data
        phone = login_form.phone.data


        user_doc = get_user_by_id(username)
        
        if user_doc.to_dict() is not None:
            typeuser = get_type(username)
            print(user_doc.to_dict()['password'])
            print(password)
            # Ya se ha realizado el Login con anterioridad
            if check_password_hash(user_doc.to_dict()['password'], password):
                user_data = UserData(username, password, email, phone, typeuser)
                user = UserModel(user_data)
                flash(f'Bienvenido de nuevo {username}') # le cambie
                login_user(user)
                redirect(url_for('hello'))
            else:
                flash('La información no coincide')
        else:
            flash('El usuario no existe')
        
        return redirect(url_for('index', _external=True))

    return render_template('login.html', **context)

@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        email = signup_form.email.data
        phone = signup_form.phone.data
        typeuser = 2
        
        user_doc = get_user_by_id(username)
        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash, email, phone, typeuser)
            user_put_data(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash(f'Bienvenido {username}!') # le cambie 
            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe!')
    
    return render_template('signup.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Regresa pronto')
    return redirect(url_for('auth.login'))


