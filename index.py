from flask import Flask, session, redirect, render_template, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import UsersModel, FilmsModel, CinemasModel
from forms import LoginForm, RegisterForm, AddFilmForm, SearchYearForm, SearchCinemaForm, AddCinemaForm
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
UsersModel(db.get_connection()).init_table()
FilmsModel(db.get_connection()).init_table()
CinemasModel(db.get_connection()).init_table()


@app.route('/')
@app.route('/index')
def index():
    """
    Главная страница
    :return:
    Основная страница сайта, либо редирект на авторизацю
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] == 'admin':
        return render_template('index_admin.html', username=session['username'])
    # если обычный пользователь, то его на свою
    films = FilmsModel(db.get_connection()).get_all()
    return render_template('film_user.html', username=session['username'], title='Просмотр базы', films=films)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница авторизации
    :return:
    переадресация на главную, либо вывод формы авторизации
    """
    form = LoginForm()
    if form.validate_on_submit():  # ввели логин и пароль
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        # проверяем наличие пользователя в БД и совпадение пароля
        if user_model.exists(user_name)[0] and check_password_hash(user_model.exists(user_name)[1], password):
            session['username'] = user_name  # запоминаем в сессии имя пользователя и кидаем на главную
            return redirect('/index')
        else:
            flash('Пользователь или пароль не верны')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    """
    Выход из системы
    :return:
    """
    session.pop('username', 0)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Форма регистрации
    """
    form = RegisterForm()
    if form.validate_on_submit():
        # создать пользователя
        users = UsersModel(db.get_connection())
        if form.user_name.data in [u[1] for u in users.get_all()]:
            flash('Такой пользователь уже существует')
        else:
            users.insert(user_name=form.user_name.data, email=form.email.data,
                         password_hash=generate_password_hash(form.password_hash.data))
            # редирект на главную страницу
            return redirect(url_for('index'))
    return render_template("register.html", title='Регистрация пользователя', form=form)


"""Работа с фильмами"""


@app.route('/film_admin', methods=['GET'])
def film_admin():
    """
    Вывод всей информации об всех автомобилях
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    # если обычный пользователь, то его на свою
    films = FilmsModel(db.get_connection()).get_all()
    return render_template('film_admin.html',
                           username=session['username'],
                           title='Просмотр фильмов',
                           films=films)


@app.route('/add_film', methods=['GET', 'POST'])
def add_film():
    """
    Добавление фильма
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        return redirect('index')
    form = AddFilmForm()
    available_cinemas = [(i[0], i[1]) for i in CinemasModel(db.get_connection()).get_all()]
    form.cinema_id.choices = available_cinemas
    if form.validate_on_submit():
        # создать фильм
        films = FilmsModel(db.get_connection())
        films.insert(name=form.name.data,
                    year=form.year.data,
                    country=form.country.data,
                    genre=form.genre.data,
                    rating=form.rating.data,
                    cinema=form.cinema_id.data)
        # редирект на главную страницу
        return redirect(url_for('film_admin'))
    return render_template("add_film.html", title='Добавление фильма', form=form)


@app.route('/film/<int:film_id>', methods=['GET'])
def film(film_id):
    """
    Вывод всей информации о фильме
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если не админ, то его на главную страницу
    '''if session['username'] != 'admin':
        return redirect(url_for('index'))'''
    # иначе выдаем информацию
    film = FilmsModel(db.get_connection()).get(film_id)
    cinema = CinemasModel(db.get_connection()).get(film[5])
    return render_template('film_info.html',
                           username=session['username'],
                           title='Просмотр информации о фильме',
                           film=film,
                           cinema=cinema[1])


@app.route('/search_price', methods=['GET', 'POST'])
def search_price():
    """
    Запрос фильмов, удовлетворяющих определенному году
    """
    form = SearchYearForm()
    if form.validate_on_submit():
        # получить все фильмы по определенным годам
        films = FilmsModel(db.get_connection()).get_by_year(form.start_year.data, form.end_year.data)
        # редирект на страницу с результатами
        return render_template('film_user.html', username=session['username'], title='Просмотр базы', films=films)
    return render_template("search_year.html", title='Подбор по годам', form=form)


@app.route('/search_cinema', methods=['GET', 'POST'])
def search_cinema():
    """
    Запрос фильмов в определенном кинотеатре
    """
    form = SearchCinemaForm()
    available_cinemas = [(i[0], i[1]) for i in CinemasModel(db.get_connection()).get_all()]
    form.cinema_id.choices = available_cinemas
    if form.validate_on_submit():
        #
        films = FilmsModel(db.get_connection()).get_by_cinema(form.cinema_id.data)
        # редирект на главную страницу
        return render_template('film_user.html', username=session['username'], title='Просмотр базы', films=films)
    return render_template("search_cinema.html", title='Подбор по году', form=form)


'''Работа с кинотеатром'''


@app.route('/cinema_admin', methods=['GET'])
def cinema_admin():
    """
    Вывод всей информации об всех кинотеатрах
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    # иначе это админ
    cinemas = CinemasModel(db.get_connection()).get_all()
    return render_template('cinema_admin.html',
                           username=session['username'],
                           title='Просмотр кинотеатров',
                           cinemas=cinemas)


@app.route('/cinema/<int:cinema_id>', methods=['GET'])
def cinema(cinema_id):
    """
    Вывод всей информации о кинотеатре
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если не админ, то его на главную страницу
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    # иначе выдаем информацию
    cinema = CinemasModel(db.get_connection()).get(cinema_id)
    return render_template('cinema_info.html',
                           username=session['username'],
                           title='Просмотр информации о кинотеатре',
                           cinema=cinema)


@app.route('/add_cinema', methods=['GET', 'POST'])
def add_cinema():
    """
    Добавление кинотеатра и вывод на экран информации о нем
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] == 'admin':
        form = AddCinemaForm()
        if form.validate_on_submit():
            # создать дилера
            cinemas = CinemasModel(db.get_connection())
            cinemas.insert(name=form.name.data, address=form.address.data)
            # редирект на главную страницу
            return redirect(url_for('index'))
        return render_template("add_cinema.html", title='Добавление кинотеатра', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
