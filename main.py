import os

from flask import Flask, send_file, jsonify, request

app = Flask(__name__)

# Simple representation of the Tic Tac Toe board: 0-8 represent the cells.
# 0: empty, 1: Player X, 2: Player O.
# Use a global variable to store the game state.
game_state = {}

def check_win(player):
    """Checks if the given player has won the game."""
    # Check rows
    for i in range(0, 9, 3):
        if game_state['board'][i] == game_state['board'][i+1] == game_state['board'][i+2] == player:
            return True
    # Check columns
    for i in range(3):
        if game_state['board'][i] == game_state['board'][i+3] == game_state['board'][i+6] == player:
            return True
    # Check diagonals
    if game_state['board'][0] == game_state['board'][4] == game_state['board'][8] == player:
        return True
    if game_state['board'][2] == game_state['board'][4] == game_state['board'][6] == player:
        return True
    return False

def check_draw():
    """Checks if the game is a draw."""
    return 0 not in game_state['board']

def initialize_game():
    """Initializes a new game."""
    global game_state
    game_state = {
        "board": [0] * 9,
        "current_player": 1,  # 1 for Player X, 2 for Player O
        "status": "playing"
    }

# Initialize the game when the application starts
initialize_game()

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route("/board", methods=["GET"])
def get_board(): 
 """Returns the current state of the game board and current player.""" 
    return jsonify(game_state)

@app.route("/move", methods=["POST"])

    """Handles a player's move."""
    global game_state

    # Check if the game is still playing
    if game_state['status'] != 'playing':
        return jsonify({"status": "game finished", "message": "Please reset the game"})

    data = request.json
    cell = data.get('index')

    if cell is None or not (0 <= cell < 9) or game_state['board'][cell] != 0:
        return jsonify({"status": "invalid move", "message": "Invalid move."})


    
        game_state['board'][cell] = game_state['current_player']

    if check_win(game_state['current_player']):
            game_state['status'] = 'win'
            game_state['winner'] = game_state['current_player']
            game_state['message'] = f"Player {game_state['current_player']} wins!"
    elif check_draw():
            game_state['status'] = 'draw'
            game_state['message'] = "It's a draw!"
            game_state['current_player'] = 3 - game_state['current_player']  # Switch player (1 becomes 2, 2 becomes 1)
            return jsonify(game_state)
    else:
        return jsonify({"status": "invalid move"})

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
