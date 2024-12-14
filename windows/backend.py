from flask import Flask, request, jsonify
from collections import defaultdict

app = Flask(__name__)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.history = defaultdict(list)

    def addHistory(self, movie, showTime):
        self.history[movie].append(showTime)

class Movie:
    def __init__(self, title, cost):
        self.title = title
        self.showTime = ["10:00", "12:00", "14:00", "16:00", "18:00"]
        self.cost = cost
        self.seats = len(self.showTime) * 48

    def addShowTime(self, showTime):
        if showTime not in self.showTime:
            self.showTime.append(showTime)

admin = User("admin", "admin")
user1 = User("user1", "user1")
user2 = User("user2", "user2")

users = [admin, user1, user2]
movies = [Movie("Movie 1", 330), Movie("Movie 2", 250)]

admin.addHistory("Movie 1", "10:00")
admin.addHistory("Movie 1", "12:00")
admin.addHistory("Movie 1", "13:00")
user1.addHistory("Movie 1", "12:00")
user2.addHistory("Movie 1", "14:00")
user2.addHistory("Movie 1", "15:00")
user2.addHistory("Movie 2", "17:00")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Логин и пароль обязательны"}), 400

    username = data['username']
    password = data['password']
    if any(user.username == username for user in users):
        return jsonify({"message": "Логин уже занят"}), 400

    user = User(username, password)
    users.append(user)
    return jsonify({"message": "Пользователь зарегистрирован"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Логин и пароль обязательны"}), 400

    username = data['username']
    password = data['password']
    for user in users:
        if user.username == username and user.password == password:
            return jsonify({"message": "Успешная авторизация"}), 200

    return jsonify({"message": "Неправильные логин или пароль"}), 401

@app.route('/movies/addMovie', methods=['POST'])
def add_movie():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('showTime') or not data.get('cost'):
        return jsonify({"message": "Название, время и стоимость обязательны"}), 400

    title = data['title']
    showTime = data['showTime']
    cost = data['cost']
    
    # Создаем фильм без стандартных сеансов
    movie = Movie(title, cost)
    movie.showTime = []  # Удаляем стандартные времена
    for time in showTime:
        movie.addShowTime(time)  # Добавляем только переданные сеансы
    
    movies.append(movie)
    return jsonify({"message": "Фильм добавлен"}), 201


@app.route('/movies/getMovies', methods=['GET'])
def get_movies():
    return jsonify([movie.__dict__ for movie in movies]), 200

@app.route('/movies/addShowTime', methods=['POST'])
def add_show_time():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('showTime'):
        return jsonify({"message": "Название и время обязательны"}), 400

    title = data['title']
    showTime = data['showTime']
    movie = next((m for m in movies if m.title == title), None)
    if movie:
        movie.addShowTime(showTime)
        return jsonify({"message": "Сеанс добавлен"}), 201
    else:
        return jsonify({"message": "Фильм не найден"}), 404

@app.route('/movies/names', methods=['GET'])
def get_movie_names():
    return jsonify([movie.title for movie in movies]), 200

@app.route('/movies/getMovieInfo', methods=['POST'])
def get_movie_info():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({"message": "Название фильма обязательно"}), 400
    info = defaultdict(list)
    for user in users:
        if user.history.get(data['title'], None):
            info[user.username] = user.history[data['title']]
    return jsonify(info), 200

@app.route('/movies/delete/<string:title>', methods=['DELETE'])
def delete_movie(title):
    global movies
    movie_to_delete = next((m for m in movies if m.title == title), None)
    if movie_to_delete:
        movies.remove(movie_to_delete)
        return jsonify({"message": "Фильм удален"}), 200
    else:
        return jsonify({"message": "Фильм не найден"}), 404


if __name__ == '__main__':
    app.run(debug=True)
