import turtle as trtl


screen = trtl.Screen()


# Turtle for displaying current turn
turn_pen = trtl.Turtle()
turn_pen.hideturtle()
turn_pen.penup()


# Create turtles
grid_pen = trtl.Turtle()
grid_pen.speed(0)
grid_pen.penup()
grid_pen.hideturtle()
grid_pen.pensize(3)


marks_pen = trtl.Turtle()   # used to write X/O marks; clearing this will remove marks
marks_pen.hideturtle()
marks_pen.penup()


msg_pen = trtl.Turtle()     # used to display messages (win/draw)
msg_pen.hideturtle()
msg_pen.penup()


# Define grid parameters
square_size = 100
start_x = -150
start_y = 150


# Draw vertical lines
for i in range(1, 3):
    grid_pen.goto(start_x + i * square_size, start_y)
    grid_pen.pendown()
    grid_pen.goto(start_x + i * square_size, start_y - 3 * square_size)
    grid_pen.penup()


# Draw horizontal lines
for i in range(1, 3):
    grid_pen.goto(start_x, start_y - i * square_size)
    grid_pen.pendown()
    grid_pen.goto(start_x + 3 * square_size, start_y - i * square_size)
    grid_pen.penup()


# Game state
player_1 = "X"
player_2 = "O"
current_player = player_1
board = [""] * 9  # 3x3 board flattened
game_over = False
# New data structure to track each player's move queue
move_queues = {}




def coord_to_index(x, y):
    """Convert screen x,y to board index (0..8). Return None if outside grid."""
    rel_x = x - start_x
    rel_y = start_y - y  # invert y because start_y is top
    # Check if the click is outside the grid boundaries
    if rel_x < 0 or rel_x >= 3 * square_size or rel_y < 0 or rel_y >= 3 * square_size:
        return None
    # Calculate column and row based on relative x and y
    col = int(rel_x // square_size)
    row = int(rel_y // square_size)
    # Return the corresponding index in the flattened board
    return row * 3 + col




def index_to_center(idx):
    """Return the (x,y) center of a square given its index."""
    # Calculate row from index
    row = idx // 3
    # Calculate column from index
    col = idx % 3
    # Center the drawing based on just calculated row and column
    cx = start_x + col * square_size + square_size / 2
    cy = start_y - row * square_size - square_size / 2
    return cx, cy


'''
Essentially just draws the X or O at the correct position in the center of the square based on the approximation of where the user clicked
'''
def draw_mark(idx, mark):
    cx, cy = index_to_center(idx)
    marks_pen.goto(cx, cy - 30)  # adjust vertical to better center the text
    marks_pen.write(mark, align="center", font=("Arial", 48, "bold"))




def redraw_marks():
    """Clear and redraw all marks according to the `board` state."""
    marks_pen.clear()
    for i, m in enumerate(board):
        if m != "":
            draw_mark(i, m)


'''
The code must check for a winner after each move. It needs to know the winning combos so if you make a
bunch of cases we can check if any chosen tiles match a winning combo to end the game
'''
def check_winner():
    """Return 'X' or 'O' if there's a winner, or None otherwise."""
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
# Check to make sure in each of the values of a b and c the letters aren't empty and have the same letter value, if they do you return the winning letter
    for a, b, c in wins:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    return None


# Allows abstraction to occur, I can now reset the game state easily as well as remove any stored data
def reset_game():
    global board, current_player, game_over
    board = [""] * 9
    current_player = player_1
    game_over = False
    marks_pen.clear()
    msg_pen.clear()
    # reset per-player move queues
    move_queues[player_1] = []
    move_queues[player_2] = []
    show_turn()


# Make a function to handle showing messages abstracts
def show_message(text):
    msg_pen.color("black")
    msg_pen.clear()
    msg_pen.goto(0, start_y - 3 * square_size - 30)
    msg_pen.write(text, align="center", font=("Arial", 18, "normal"))


# Show whose turn it is in indigo
def show_turn():
    turn_pen.clear()
    turn_pen.color("skyblue")
    turn_pen.goto(0, start_y + 30)
    turn_pen.write(f"{current_player}'s turn to go!", align="center", font=("Arial", 50, "bold"))


'''
Handle click events
If any issues such as game over or the area clicked isnt on the grid or the square is already taken, ignore the click.
However if the click is valid, place the current player's mark on the board and record the move in their move queue.
'''
def handle_click(x, y):
    global current_player, game_over
    if game_over:
        return
    idx = coord_to_index(x, y)
    if idx is None:
        return
    if board[idx] != "":
        return  # square already taken
    # Ensure move_queues exist (first run)
    if player_1 not in move_queues:
        move_queues[player_1] = []
    if player_2 not in move_queues:
        move_queues[player_2] = []


    # place mark and record move
    board[idx] = current_player
    move_queues[current_player].append(idx)


    # If player now has more than 3 tiles, remove their earliest one
    if len(move_queues[current_player]) > 3:
        old_idx = move_queues[current_player].pop(0)
        # clear the old tile from the board
        board[old_idx] = ""


    # redraw all marks to reflect any removals
    redraw_marks()


    # check for winner after the move
    winner = check_winner()
    if winner is not None:
        game_over = True
        show_message(f"{winner} wins! Resetting game...")
        # reset after a short delay (2000 ms)
        screen.ontimer(reset_game, 2000)
        return


    # switch player
    current_player = player_2 if current_player == player_1 else player_1
    show_turn()






# Wire click handler
screen.onscreenclick(handle_click)






screen.mainloop()
