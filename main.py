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
    return jsonify(game_state)

@app.route("/move", methods=["POST"])
def make_move():
    """Handles a player's move."""
    global game_state

    # Check if the game is still playing
    if game_state['status'] != 'playing':
        return jsonify({"status": "game finished", "message": "Please reset the game"})

    data = request.json
    cell = data.get('index')

    print(f"Received move for cell: {cell}")

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
    else:
        # Set the message for the next player's turn
        game_state['current_player'] = 3 - game_state['current_player']  # Switch player (1 becomes 2, 2 becomes 1)
        player_char = 'X' if game_state['current_player'] == 1 else 'O'
        game_state['message'] = f"Player {player_char}'s turn"

    # Convert numerical board representation to 'X', 'O', or '' for the frontend
    response_data = {'board': ['' if cell == 0 else 'X' if cell == 1 else 'O' for cell in game_state['board']], 'message': game_state.get('message', ''), 'status': game_state['status'], 'winner': game_state.get('winner'), 'draw': game_state.get('draw')}
    return jsonify(response_data)

@app.route("/reset", methods=["POST"])
def reset_game():
    """Resets the game state."""
    initialize_game()
    return jsonify({"status": "reset succeeded"})
def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    main()
