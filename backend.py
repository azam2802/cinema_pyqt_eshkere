from flask import Flask, request, jsonify

app = Flask(__name__)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.history = []

class Movie:
    def __init__(self, title, showTime, cost):
        self.title = title
        self.showTime = showTime
        self.cost = cost

users = [User("admin", "admin")]
movies = []

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
    movie = Movie(title, showTime, cost)
    movies.append(movie)
    return jsonify({"message": "Фильм добавлен"}), 201

@app.route('/movies/getMovies', methods=['GET'])
def get_movies():
    return jsonify([movie.__dict__ for movie in movies]), 200

if __name__ == '__main__':
    app.run(debug=True)