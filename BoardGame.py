from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Game state
current_player = 1
scores = {1: 0, 2: 0}
board_state = [None] * 12  # Store the state of the board

@app.route('/')
def index():
    return render_template('index.html', scores=scores)

@app.route('/add_tile/<int:tile_index>')
def add_tile(tile_index):
    global current_player
    if board_state[tile_index] is None:  # Only allow placement if the tile is empty
        color = 'green' if current_player == 1 else 'blue'
        board_state[tile_index] = color  # Update the board state
        if check_win(color):
            scores[current_player] += 1  # Increment the score for the current player
            return jsonify(color=color, winner=current_player)
        current_player = 2 if current_player == 1 else 1  # Switch player
    return jsonify(color=color, winner=None)

@app.route('/reset')
def reset():
    global current_player, scores, board_state
    current_player = 1
    scores = {1: 0, 2: 0}
    board_state = [None] * 12  # Reset the board state
    return jsonify(success=True)

def check_win(color):
    # Check for win conditions (e.g., rows of three)
    for i in range(10):  # Check from index 0 to 9 (to fit in rows)
        if board_state[i] == color and board_state[i + 1] == color and board_state[i + 2] == color:
            return True
    return False

if __name__ == "__main__":
    app.run(debug=True)

