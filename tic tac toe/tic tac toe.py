import random as rnd
import turtle
import pickle as pkl

# ---------- turtle setup ----------
window = turtle.Screen()
window.title("Tic Tac Toe")
window.bgcolor("white")

# ---------- game state ----------
p1_sign = None
p2_sign = None
turn = 1
board = [["", "", ""], ["", "", ""], ["", "", ""]]
game_over = False
mode = "PVP"   # "PVP" / "CPU_RANDOM" / ""CPU_STRAT"

P1_GIF = r"C:\Users\haraz\Downloads\messi_120.gif"
P2_GIF = r"C:\Users\haraz\Downloads\messi_cry.gif"
SAVE_FILE = "tictactoe_save.bin"
HISTORY_FILE = "games_history.txt"

#window.addshape(P1_GIF)
#window.addshape(P2_GIF)

win_pic = turtle.Turtle()
win_pic.hideturtle()
win_pic.penup()

input_mode = None  # "CLICK" / "COORDS"
showing_history = False

# ---------- pens ----------
status_pen = turtle.Turtle()
status_pen.hideturtle()
status_pen.penup()
status_pen.color("black")

title_pen = turtle.Turtle()
title_pen.hideturtle()
title_pen.penup()
title_pen.color("#2c3e50")


ui_pen = turtle.Turtle()
ui_pen.hideturtle()
ui_pen.penup()
ui_pen.speed(0)

board_pen = turtle.Turtle()
board_pen.hideturtle()
board_pen.speed(0)
board_pen.pensize(4)
board_pen.color("black")

mark_pen = turtle.Turtle()
mark_pen.hideturtle()
mark_pen.speed(0)
mark_pen.pensize(6)
mark_pen.color("black")

win_pen = turtle.Turtle()
win_pen.hideturtle()
win_pen.speed(0)
win_pen.pensize(8)
win_pen.color("green")

history_pen = turtle.Turtle()
history_pen.hideturtle()
history_pen.penup()
history_pen.color("black")
# ---------- board drawing ----------
BOARD_SIZE = 300
HALF = BOARD_SIZE / 2
CELL = BOARD_SIZE / 3

def draw_board():
    board_pen.clear()

    # frame
    board_pen.penup()
    board_pen.goto(-HALF, HALF)
    board_pen.pendown()
    for _ in range(4):
        board_pen.forward(BOARD_SIZE)
        board_pen.right(90)

    # vertical lines
    for x in (-HALF/3, HALF/3):
        board_pen.penup()
        board_pen.goto(x, HALF)
        board_pen.pendown()
        board_pen.goto(x, -HALF)

    # horizontal lines
    for y in (-HALF/3, HALF/3):
        board_pen.penup()
        board_pen.goto(-HALF, y)
        board_pen.pendown()
        board_pen.goto(HALF, y)

# ---------- UI helpers ----------
def inside(x, y, x1, y1, x2, y2):
    return x1 <= x <= x2 and y2 <= y <= y1

def draw_title():
    title_pen.clear()
    title_pen.goto(0, 260)
    title_pen.write(
        "TIC  TAC  TOE",
        align="center",
        font=("Arial", 28, "bold")
    )

def draw_button(x1, y1, x2, y2, text, color,bg_color=None):
    ui_pen.penup()
    ui_pen.goto(x1, y1)
    ui_pen.pendown()
    ui_pen.pencolor(color)
    ui_pen.fillcolor(bg_color)

    ui_pen.begin_fill()
    ui_pen.goto(x2, y1)
    ui_pen.goto(x2, y2)
    ui_pen.goto(x1, y2)
    ui_pen.goto(x1, y1)
    ui_pen.end_fill()

    ui_pen.penup()
    ui_pen.goto((x1 + x2) / 2, y2 + 10)
    ui_pen.pencolor(color)
    ui_pen.write(text, align="center", font=("Arial", 14, "bold"))

# button rectangles
R = (-90, 190, 100, 150)          # Restart
C = (160, 210, 290, 170)         # CPU Random
S = (160, 160, 290, 120)         # CPU Strategic
SV = (-290, 210, -160, 170)          # SAVE GAME
LD = (-290, 160,  -160, 120)           # LOAD GAME
CI = (160, 110, 290, 70)   # COORD INPUT
HY = (-290, 110, -160, 70)   # HISTORY


def draw_ui():
    ui_pen.clear()
    draw_button(*R, "RESTART", "white","black")
    bg_c = "red" if mode == "CPU_RANDOM" else "black"
    draw_button(*C, "RANDOM", "white", "red")

    bg_s = "blue" if mode == "CPU_STRAT" else "black"
    draw_button(*S, "STRATEGIC", "white", "blue")
    draw_button(*SV, "SAVE GAME", "white", "#27ae60")
    draw_button(*LD, "LOAD GAME", "white", "#2980b9")
    draw_button(*CI, "COORD INPUT", "white", "#8e44ad")
    draw_button(*HY, "HISTORY", "white", "#f39c12")


def draw_status(msg=None):
    status_pen.clear()
    status_pen.goto(0, 220)

    if msg is not None:
        status_pen.write(msg, align="center", font=("Arial", 18, "bold"))
        return

    if p1_sign is None:
        status_pen.write("tic tac toe game",
                         align="center", font=("Arial", 18, "bold"))
    else:
        status_pen.write(f"P1: {p1_sign.upper()} | P2: {p2_sign.upper()} | Turn: Player {turn}",
                         align="center", font=("Arial", 18, "bold"))

#def show_win_picture(gif_file):
    #win_pic.clearstamps()
    #win_pic.shape(gif_file)
    #win_pic.goto(0, -260)
    #win_pic.showturtle()
    #win_pic.stamp()


#def hide_win_picture():
    #win_pic.clearstamps()
    #win_pic.hideturtle()

# ---------- game logic ----------
def empty_space():
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                return True
    return False

def check_winner():
    lines = []

    # rows
    for r in range(3):
        lines.append(board[r])

    # cols
    for c in range(3):
        lines.append([board[0][c], board[1][c], board[2][c]])

    # diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line[0] != "" and line[0] == line[1] == line[2]:
            return line[0]

    if not empty_space():
        return "draw"

    return None
def winning_line():
    # rows
    for r in range(3):
        if board[r][0] != "" and board[r][0] == board[r][1] == board[r][2]:
            return (r, 0), (r, 2)

    # cols
    for c in range(3):
        if board[0][c] != "" and board[0][c] == board[1][c] == board[2][c]:
            return (0, c), (2, c)

    # diagonals
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return (0, 0), (2, 2)

    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return (0, 2), (2, 0)

    return None

def draw_win_line(line):

    (r1, c1), (r2, c2) = line
    x1, y1 = cell_center(r1, c1)
    x2, y2 = cell_center(r2, c2)

    win_pen.penup()
    win_pen.goto(x1, y1)
    win_pen.pendown()
    win_pen.goto(x2, y2)
    win_pen.penup()


def next_turn():
    global turn
    turn = 2 if turn == 1 else 1

def cell_from_click(x, y):
    # checks if ,inside the  board?
    if not (-HALF <= x <= HALF and -HALF <= y <= HALF):
        return None

    col = int((x + HALF) // CELL)
    row = int((HALF - y) // CELL)

    if 0 <= row <= 2 and 0 <= col <= 2:
        return row, col
    return None

def cell_center(row, col):
    cx = -HALF + (col + 0.5) * CELL
    cy = HALF - (row + 0.5) * CELL
    return cx, cy

def draw_x(cx, cy):
    s = CELL * 0.28
    mark_pen.penup()
    mark_pen.goto(cx - s, cy + s)
    mark_pen.pendown()
    mark_pen.goto(cx + s, cy - s)
    mark_pen.penup()
    mark_pen.goto(cx - s, cy - s)
    mark_pen.pendown()
    mark_pen.goto(cx + s, cy + s)
    mark_pen.penup()

def draw_o(cx, cy):
    r = CELL * 0.28
    mark_pen.penup()
    mark_pen.goto(cx, cy - r)
    mark_pen.pendown()
    mark_pen.circle(r)
    mark_pen.penup()

def place_mark(row, col, sign):
    cx, cy = cell_center(row, col)
    if sign == "x":
        draw_x(cx, cy)
    else:
        draw_o(cx, cy)

def play_move_by_xy(x, y):
    global game_over

    if game_over:
        return

    if mode in ("CPU_RANDOM", "CPU_STRAT") and turn == 2:
        return

    rc = cell_from_click(x, y)
    if rc is None:
        return

    row, col = rc
    if board[row][col] != "":
        return

    current_sign = p1_sign if turn == 1 else p2_sign
    board[row][col] = current_sign
    place_mark(row, col, current_sign)

    result = check_winner()
    if result == "draw":
        game_over = True
        record_game_result("draw")
        draw_status("Draw! Press RESTART")
        return

    if result in ("x", "o"):
        game_over = True
        record_game_result(result)
        line = winning_line()
        if line:
            draw_win_line(line)

        winner_player = 1 if p1_sign == result else 2
        if winner_player == 1:
            draw_status("YOU WIN! Press RESTART")
            #show_win_picture(P1_GIF)
        else:
            draw_status("YOU LOSE! Press RESTART")
            #show_win_picture(P2_GIF)
        return

    next_turn()
    draw_status()
    computer_move()
def play_move_by_coords():
    global game_over

    if game_over:
        return

    if mode in ("CPU_RANDOM", "CPU_STRAT") and turn == 2:
        return

    row = window.textinput("Row Input", "Enter row (0-2):")
    if row is None:
        return

    col = window.textinput("Column Input", "Enter column (0-2):")
    if col is None:
        return

    if not row.isdigit() or not col.isdigit():
        draw_status("Invalid input!")
        return

    row = int(row)
    col = int(col)

    if row not in (0,1,2) or col not in (0,1,2):
        draw_status("Row/Col must be 0-2")
        return

    if board[row][col] != "":
        draw_status("Cell already taken")
        return

    current_sign = p1_sign if turn == 1 else p2_sign
    board[row][col] = current_sign
    place_mark(row, col, current_sign)

    result = check_winner()
    if result == "draw":
        game_over = True
        record_game_result("draw")
        draw_status("Draw! Press RESTART")
        return

    if result in ("x", "o"):
        game_over = True
        record_game_result(result)
        line = winning_line()
        if line:
            draw_win_line(line)
        draw_status("Game Over! Press RESTART")
        return

    next_turn()
    draw_status()
    computer_move()

def computer_move():#random player
    global game_over

    if mode not in ("CPU_RANDOM", "CPU_STRAT"):
        return
    if game_over or turn != 2:
        return
    if not empty_space():
        return

    if mode == "CPU_RANDOM":
        empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
        row, col = rnd.choice(empty_cells)
    else:
        rc = strategic_move(cpu=p2_sign, human=p1_sign)
        if rc is None:
            return
        row, col = rc

    board[row][col] = p2_sign
    place_mark(row, col, p2_sign)

    result = check_winner()
    if result == "draw":
        game_over = True
        record_game_result("draw")
        draw_status("Draw! Press RESTART")
        return
    if result in ("x", "o"):
        game_over = True
        record_game_result(result)
        line = winning_line()
        if line:
            draw_win_line(line)
        draw_status("Computer wins! Press RESTART")
        return

    next_turn()
    draw_status()


def strategic_move(cpu, human):#staregic player
    empties = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
    if not empties:
        return None

    def win_after(sign, r, c):
        board[r][c] = sign
        res = check_winner()
        board[r][c] = ""
        return res == sign

    def is_fork(sign, r, c):
        board[r][c] = sign
        cnt = 0
        for (rr, cc) in [(a, b) for a in range(3) for b in range(3) if board[a][b] == ""]:
            if win_after(sign, rr, cc):
                cnt += 1
        board[r][c] = ""
        return cnt >= 2

    # 1) win
    for (r, c) in empties:
        if win_after(cpu, r, c):
            return (r, c)

    # 2) block
    for (r, c) in empties:
        if win_after(human, r, c):
            return (r, c)

    # 3) fork
    for (r, c) in empties:
        if is_fork(cpu, r, c):
            return (r, c)

    # 4) block fork
    opp_forks = [(r, c) for (r, c) in empties if is_fork(human, r, c)]
    if opp_forks:
        return opp_forks[0]

    # 5) center
    if board[1][1] == "":
        return (1, 1)

    # 6) opposite corner
    opposite = [((0,0),(2,2)), ((2,2),(0,0)), ((0,2),(2,0)), ((2,0),(0,2))]
    for (a, b) in opposite:
        ar, ac = a
        br, bc = b
        if board[ar][ac] == human and board[br][bc] == "":
            return (br, bc)

    # 7) corners
    for (r, c) in [(0,0),(0,2),(2,0),(2,2)]:
        if board[r][c] == "":
            return (r, c)

    # 8) sides
    for (r, c) in [(0,1),(1,0),(1,2),(2,1)]:
        if board[r][c] == "":
            return (r, c)

    return empties[0]

# ---------- Save / Load (Binary) ----------

def save_game_state(board, turn, p1_name, p2_name, p1_sign, p2_sign, mode=None):
    data = {
        "board": board,
        "turn": turn,
        "p1_name": p1_name,
        "p2_name": p2_name,
        "p1_sign": p1_sign,
        "p2_sign": p2_sign,
        "mode": mode
    }
    with open(SAVE_FILE, "wb") as f:
        pkl.dump(data, f)

def load_game_state():
    try:
        with open(SAVE_FILE, "rb") as f:
            return pkl.load(f)
    except FileNotFoundError:
        return None

def delete_saved_game():
    with open(SAVE_FILE, "wb") as f:
        pkl.dump(None, f)

# ---------- History (Text CSV) ----------

def append_game_history(p1_name, p2_name, winner_name):
    line = f"{p1_name},{p2_name},{winner_name}\n"
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def read_history_lines():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

def print_history():
    lines = read_history_lines()
    print("---- history of tic tac toe ----")
    for i, line in enumerate(lines, start=1):
        parts = line.split(",")
        if len(parts) == 3:
            p1, p2, w = parts
            print(f"{i}. {p1} vs {p2} | win: {w}")
        else:
            print(f"{i}. {line}")

p1_name = "Player1"
p2_name = "Player2"

def redraw_marks_from_board():
    mark_pen.clear()
    win_pen.clear()
    #hide_win_picture()

    for r in range(3):
        for c in range(3):
            if board[r][c] in ("x", "o"):
                place_mark(r, c, board[r][c])

def apply_loaded_state(loaded):

    global board, turn, p1_sign, p2_sign, mode, game_over

    if loaded is None:
        draw_status("No saved game found")
        return

    if loaded is None or loaded == {}:
        draw_status("No saved game found")
        return

    if loaded is None:
        draw_status("No saved game found")
        return

    if loaded is None:
        draw_status("No saved game found")
        return

    if loaded is None:
        return

    if loaded is None:
        return

    if loaded is None:
        return

    if loaded is None:
        return

    if loaded is None:
        return

    # --- load fields safely ---
    if loaded is None:
        return

    if loaded is None:
        draw_status("No saved game found")
        return

    # load dict
    board = loaded.get("board", board)
    turn = loaded.get("turn", turn)
    p1_sign = loaded.get("p1_sign", p1_sign)
    p2_sign = loaded.get("p2_sign", p2_sign)
    mode = loaded.get("mode", mode)

    game_over = False

    draw_board()
    draw_ui()
    redraw_marks_from_board()
    draw_status("Game loaded!")

def record_game_result(result_sign):

    if result_sign == "draw":
        append_game_history(p1_name, p2_name, "Tie")
    elif result_sign == p1_sign:
        append_game_history(p1_name, p2_name, p1_name)
    elif result_sign == p2_sign:
        append_game_history(p1_name, p2_name, p2_name)

def show_history_screen():
    global showing_history
    showing_history = True
    board_pen.clear()
    mark_pen.clear()
    win_pen.clear()
    #hide_win_picture()
    history_pen.clear()
    draw_ui()
    draw_status("HISTORY")

    lines = read_history_lines()
    if not lines:
        history_pen.goto(0, 50)
        history_pen.write("No History yet", align="center", font=("Arial", 18, "bold"))
        return

    lines = lines[-10:]

    y = 100
    for i, line in enumerate(lines, start=1):
        history_pen.goto(-140, y)
        history_pen.write(f"{i}. {line}", align="left", font=("Arial", 14, "normal"))
        y -= 24

# ---------- game actions ----------
def reset_game(): #reset the game
    global p1_sign, p2_sign, turn, board, game_over,mode,showing_history

    board = [["", "", ""], ["", "", ""], ["", "", ""]]

    p1_sign = "x"
    p2_sign = "o"
    turn = 1
    showing_history = False
    game_over = False
    mode="PVP"
    mark_pen.clear()
    win_pen.clear()
    #hide_win_picture()
    draw_ui()
    draw_status()
    draw_board()
    history_pen.clear()


def  on_click(x, y): # the click system that operates the game
        global game_over, mode ,showing_history

        if showing_history:
            if inside(x, y, *R):
                reset_game()
            return

        if inside(x, y, *CI):
            play_move_by_coords()
            return

        if inside(x, y, *R):
            reset_game()
            return


        if inside(x, y, *C):
            mode = "CPU_RANDOM" if mode != "CPU_RANDOM" else "PVP"
            draw_ui()
            draw_status()
            computer_move()
            return

        if inside(x, y, *S):
            mode = "CPU_STRAT" if mode != "CPU_STRAT" else "PVP"
            draw_ui()
            draw_status()
            computer_move()
            return

        if inside(x, y, *SV):
            save_game_state(board, turn, p1_name, p2_name, p1_sign, p2_sign, mode)
            draw_status("Game saved!")
            return

            # LOAD
        if inside(x, y, *LD):
            loaded = load_game_state()
            apply_loaded_state(loaded)
            return

        if inside(x, y, *HY):
            show_history_screen()
            return

        if game_over:
            return

        if mode in ("CPU_RANDOM", "CPU_STRAT") and turn == 2:
            return
        rc = cell_from_click(x, y)
        if rc is None:
            return

        row, col = rc
        if board[row][col] != "":
            return

        current_sign = p1_sign if turn == 1 else p2_sign
        board[row][col] = current_sign
        place_mark(row, col, current_sign)

        result = check_winner()
        if result == "draw":
            game_over = True
            record_game_result("draw")
            draw_status("Draw! Press RESTART")
            return
        if result in ("x", "o"):
            game_over = True
            record_game_result(result)
            line = winning_line()
            if line:
               draw_win_line(line)
            winner_player = 1 if p1_sign == result else 2
            if winner_player== 1:
                draw_status("YOU WIN! Press RESTART")
                #show_win_picture(P1_GIF)
            else:
                draw_status("YOU LOSE! Press RESTART")
                #show_win_picture(P2_GIF)
            return

        next_turn()
        draw_status()
        computer_move()



# ---------- start ----------
draw_ui()
draw_title()
reset_game()
window.onclick(on_click)
turtle.done()

