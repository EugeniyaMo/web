class UsersModel:
    """Сущность пользователей"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(20) UNIQUE,
                             password_hash VARCHAR(128),
                             email VARCHAR(20),
                             is_admin INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, email, is_admin=False):
        """Вставка новой записи"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email, is_admin) 
                          VALUES (?,?,?,?)''',
                       (user_name, password_hash, email, int(is_admin)))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name):
        """Проверка, есть ли пользователь в системе"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        row = cursor.fetchone()
        return (True, row[2], row[0]) if row else (False,)

    def get(self, user_id):
        """Возврат пользователя по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех пользователей"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows


class CinemasModel:
    """Сущность кинотеатров"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cinemas 
                            (cinema_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(20) UNIQUE,
                             address VARCHAR(128)
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, address):
        """Добавление кинотеатра"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO cinemas 
                          (name, address) 
                          VALUES (?,?)''',
                       (name, address))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """Поиск кинотеатра по названию"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cinemas WHERE name = ?",
                       name)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, cinema_id):
        """Запрос кинотеатра по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM dealers WHERE dealer_id = ?", (str(cinema_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех кинотеатров"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM cinemas")
        rows = cursor.fetchall()
        return rows

    def delete(self, cinema_id):
        """Удаление кинотеатров"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM cinemas WHERE cinema_id = ?''', (str(cinema_id)))
        cursor.close()
        self.connection.commit()


class FilmsModel:
    """Сущность фильмов"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS films 
                            (film_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(20),
                             year INTEGER,
                             country VARCHAR(50),
                             genre VARCHAR(20),
                             rating VARCHAR(20),
                             cinema INTEGER
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, year, country, genre, rating, cinema):
        """Добавление фильма"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO films 
                          (name, year, country, genre, rating, cinema) 
                          VALUES (?,?,?,?,?)''',
                       (name, str(year), country, genre, str(rating), cinema))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """Поиск фильма по названию"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM films WHERE name = ?",
                       name)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, film_id):
        """Поиск фильма по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM films WHERE film_id = ?", (str(film_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех фильмов"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, year, film_id FROM films")
        rows = cursor.fetchall()
        return rows

    def delete(self, film_id):
        """Удаление фильма"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM films WHERE film_id = ?''', (str(film_id)))
        cursor.close()
        self.connection.commit()

    def get_by_yaer(self, start_year, end_year):
        """Запрос фильмов по году"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT model, year, film_id FROM films WHERE year >= ? AND year <= ?", (str(start_year), str(end_year)))
        row = cursor.fetchall()
        return row

    def get_by_cinema(self, cinema_id):
        """Запрос автомобилей по дилерскому центру"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, year, film_id FROM films WHERE cinema = ?", (str(cinema_id)))
        row = cursor.fetchall()
        return row
