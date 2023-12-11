from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from database.db_manager import DB_Manager
from flask_login import login_user, logout_user, login_required, current_user
from classes.User import User
from classes.Game import AI_Game
from classes.Board import Board
from classes.AIPlayer import AIPlayer
from classes.Block import Block
from classes.Player import Player
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

from extensions import socketio

lobby = Blueprint('lobby', __name__)

BOARDS = [Board()] * 10
PLAYER = []
GAME = [AI_Game(["red"], Board()), AI_Game([AIPlayer("red"),AIPlayer("blue"), AIPlayer("green"), AIPlayer("yellow")], BOARDS[2])]
GAMES = [None] * 10
COUNT = [0, 0]
COUNTER = 0
SEND_MATRIX_OLD = []


from functools import wraps
from flask import abort

def lobby_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user._lobby == 0:
            flash('You must join a lobby first.', 'warning')
            print("Nicht in Lobby")
            return redirect(url_for('lobby.join'))
        print("in_lobby")
        return func(*args, **kwargs)
    return decorated_function

@lobby.route('/lobby')
@login_required
def join():
    return render_template('join_lobby.html')

@lobby.route('/lobby', methods=['POST'])
@login_required
def join_post():
    user_id = session.get('user_id')
    lobby_id = request.form.get('number')
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    user_id = current_user._id
    db.update_user((user_id, "lobby", lobby_id))
    db.disconnect()
    join_room(lobby_id)
    return redirect(url_for('lobby.room'))

@lobby.route('/game')
@login_required
@lobby_required
def room():
    users = get_lobby_user()
    return render_template("game.html", lobby_id=current_user._lobby, users=users, board=None)

@lobby.route("/game/leave_lobby")
@login_required
@lobby_required
def room_leave_lobby():
    print("testotest")
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    user_id = current_user._id
    db.update_user((user_id, "lobby", 0))
    db.disconnect()
    return redirect(url_for('lobby.join'))

@lobby.route("/game/start")
@login_required
@lobby_required
def game_start():
    lobby = current_user._lobby - 1
    print(lobby)
    if lobby == 1:
        BOARDS[lobby] = Board()
        GAME[lobby] = AI_Game([AIPlayer("red"),AIPlayer("blue"), AIPlayer("green"), AIPlayer("yellow")], BOARDS[lobby])
        game = GAME[lobby]
        game.init_game()
        COUNT[lobby] = 0
        return render_template("board.html", board = game.board.matrix, name=current_user._name)

    if lobby == 0:
        BOARDS[lobby] = Board()
        users = get_lobby_user()
        for i in range(4 - len(users)):
            users.append("AI")
        colors = ["red", "blue", "green", "yellow"]
        random.shuffle(colors)
        random.shuffle(users)
        order = []
        players = []
        for idx, user in enumerate(users):
            if user == "AI":
                players.append(AIPlayer(colors[idx]))
            else:
                players.append(Player(colors[idx]))
            order.append((user, colors[idx]))

        GAME[lobby] = AI_Game(players, BOARDS[lobby])
        game = GAME[lobby]
        game.init_game()
        COUNT[lobby] = 0
        return render_template("user_board.html", board = game.board.matrix, order=order)
        
    return "Lobby not found (please use lobby 1 for usergame or 2 for ai game)"
# #neue version noch nicht lauffähig
# def game_start():
#     game = GAME[current_user._lobby - 1]
#     game.init_game()
#     number_human_players = get_users_in_lobby(current_user._lobby)
    
#     colors = ["green", "yellow", "red", "blue"]
    
#     if number_human_players <= 4:
#         players = [Player(colors[i]) for i in range(number_human_players)]
#         ai_players = [AIPlayer(color) for color in colors[number_human_players:]]
        
#         all_players = players + ai_players
        
#         GAME[current_user._lobby] = Game(all_players, BOARDS[current_user._lobby])
#     else:
#         print("Zu viele Spieler")
    
#     return render_template("board.html", board=game.board.matrix)


@socketio.on('user_set_block')
def set_block(data):
    print(data)
    game = GAME[current_user._lobby - 1]
    color = game.active_player.color

    block_matrix = data["block_matrix"]

    for idx1, x in enumerate(block_matrix):
        for idx2, y in enumerate(x):
            if y == False:
                block_matrix[idx1][idx2] = None


    block = Block(block_matrix, color)
    print(color)
    print(data["x"], data["y"], block.block_matrix)
    if game.board.is_first_move_valid(data["x"], data["y"], block):
        print("IS_VALID")
        game.active_player.player_insert(data["block"], data["y"], data["x"])
        game.get_next_active_player()

        send_matrix = [["X" for _ in range(20)] for _ in range(20)]
        for idx1, row in enumerate(game.board.matrix):
            for idx2, y in enumerate(row):
                if y:
                    send_matrix[idx1][idx2] = y
        socketio.emit('update_board', {'board': send_matrix})

        return "Hi"
    print("IS_NOT_VALID")
    return "Hi"

@socketio.on('zug_gemacht')
def handle_zug(zug):
    global COUNTER
    global SEND_MATRIX_OLD
    print("hallo")
    print(zug)
    lobby = current_user._lobby - 1
    game = GAME[current_user._lobby - 1]
    COUNT[lobby] = COUNT[lobby] + 1
    if COUNT[lobby] <=4:
        game.play_game(True)
    else:
        game.play_game(False)
    
    #print(game.board.matrix)
    send_matrix = [["X" for _ in range(20)] for _ in range(20)]
    for idx1, row in enumerate(game.board.matrix):
        for idx2, y in enumerate(row):
            if y:
                send_matrix[idx1][idx2] = y
    
    if SEND_MATRIX_OLD == send_matrix:
        COUNTER += 1
    else: 
        COUNTER = 0

    print(COUNTER)

    
    SEND_MATRIX_OLD = send_matrix
    #print(send_matrix)
    socketio.emit('update_board', {'board': send_matrix})
    if len(game.active_player.blocks) == 0:
        print("Player wins!")

    if COUNTER == 4:
        winner = game.calculate_points()
        print(f"{winner} wins the game!")
        

    game.get_next_active_player()
    return "Hi"



@socketio.on('set_block_user_game')
def handle_zug(zug):
    lobby = current_user._lobby - 1
    game = GAME[current_user._lobby - 1]
    if not isinstance(game.active_player, AIPlayer):
        flash("Kein AI Spieler")
        game.get_next_active_player()
        return "Kein AI Spieler"

    COUNT[lobby] = COUNT[lobby] + 1
    if COUNT[lobby] <=4:
        game.play_game(True)
    else:
        game.play_game(False)
    
    send_matrix = [["X" for _ in range(20)] for _ in range(20)]
    for idx1, row in enumerate(game.board.matrix):
        for idx2, y in enumerate(row):
            if y:
                send_matrix[idx1][idx2] = y
 
    socketio.emit('update_board', {'board': send_matrix})
    if len(game.active_player.blocks) == 0:
        print("Player wins!")
    
    game.get_next_active_player()
    return "Hi"


@socketio.on('send_message')
def handle_message(message):
    print("testott")
    print(message)
    email = current_user._email
    msg = f"{email}: {message}"
    socketio.emit('chat_message', msg)
    return "Hi"



@socketio.on('join_room')
def join_room(lobby_id):
    user_id = session.get('user_id')
    print(user_id, lobby_id)
    socketio.emit('join_lobby', {'user_id': user_id}, room=lobby_id)
    return 'Joined lobby'


# def get_users_in_lobby(lobby_id):
#     # Annahme: Es gibt ein Attribut 'lobby' in der User-Klasse, das die Lobby-ID speichert.
#     users_in_lobby = User.query.filter_by(lobby=lobby_id).all()
#     return users_in_lobby


def get_lobby_user():
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    loaded_users = db.get_users_in_lobby(current_user._lobby)
    users = []
    for user in loaded_users:
        users.append(user[0])
    db.disconnect()
    return users