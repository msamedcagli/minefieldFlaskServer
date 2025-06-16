from flask import Flask, jsonify, request, render_template
from game_engine import Game

app = Flask(__name__)
game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/click', methods=['POST'])
def click():
    data = request.json
    game.reveal_cell(data['x'], data['y'])
    return jsonify(game.get_state())

@app.route('/flag', methods=['POST'])
def flag():
    data = request.json
    game.toggle_flag(data['x'], data['y'])
    return jsonify(game.get_state())

@app.route('/state', methods=['GET'])
def state():
    return jsonify(game.get_state())

# İşte yeni endpoint:
@app.route('/reset', methods=['POST'])
def reset():
    game.reset_game()
    return jsonify(game.get_state())

if __name__ == '__main__':
    app.run(debug=True)
