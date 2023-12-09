from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from database.db_manager import DB_Manager
from flask_login import login_user, logout_user, login_required, current_user
from classes.User import User
from classes.Game import AI_Game, Game
from classes.Board import Board
from classes.Player import Player
from classes.AIPlayer import AIPlayer
from flask_socketio import SocketIO, emit, join_room, leave_room

from extensions import socketio

lobby = Blueprint('lobby', __name__)

BOARDS = [Board()] * 10
PLAYER = []
GAME = [AI_Game(["red"], Board()), AI_Game([AIPlayer("red"),AIPlayer("blue")], BOARDS[2])]
GAMES = [None] * 10
COUNT = [0]


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
    #emit('join_lobby', {'user_id': user_id}, room=lobby_id)
    #eturn 'Joined lobby'
    return redirect(url_for('lobby.room'))

@lobby.route('/game')
@login_required
@lobby_required
def room():
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    loaded_users = db.get_users_in_lobby(current_user._lobby)
    users = []
    for user in loaded_users:
        users.append(user[0])
    db.disconnect()
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
    game = GAME[current_user._lobby - 1]
    game.init_game()
    number_human_players = get_users_in_lobby(current_user._lobby)
    
    colors = ["green", "yellow", "red", "blue"]
    
    if number_human_players <= 4:
        players = [Player(colors[i]) for i in range(number_human_players)]
        ai_players = [AIPlayer(color) for color in colors[number_human_players:]]
        
        all_players = players + ai_players
        
        GAME[current_user._lobby] = Game(all_players, BOARDS[current_user._lobby])
    else:
        print("Zu viele Spieler")
    
    return render_template("board.html", board=game.board.matrix)


@socketio.on('zug_gemacht')
def handle_zug(zug):
    print("hallo")
    print(zug)
    game = GAME[current_user._lobby - 1]
    COUNT[0] = COUNT[0] + 1
    if COUNT[0] <=2:
        game.play_game(True)
    else:
        game.play_game(False)
    
    print(game.board.matrix)
    send_matrix = [["X" for _ in range(20)] for _ in range(20)]
    for idx1, row in enumerate(game.board.matrix):
        for idx2, y in enumerate(row):
            if y:
                send_matrix[idx1][idx2] = y
    print(send_matrix)
    socketio.emit('update_board', {'board': send_matrix})

    if len(game.active_player.blocks) == 0:
        return "Player wins!"
    
    if zug == (0, 0, False, 0):
        counter +=1 
    else:
        counter = 0

    if counter == 4:
        winner = game.calculate_points()
        return f"{winner} wins the game!"
        

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


# @socketio.on('send_message')
# def handle_message(message):
#     print("testott")
#     print(message)
#     email = current_user._email
#     msg = f"{email}: {message}"
#     socketio.emit('chat_message', msg, room=lobby_id)
#     return "Hi"



@socketio.on('join_room')
def join_room(lobby_id):
    user_id = session.get('user_id')
    print(user_id, lobby_id)
    socketio.emit('join_lobby', {'user_id': user_id}, room=lobby_id)
    return 'Joined lobby'



def get_users_in_lobby(lobby_id):
    # Annahme: Es gibt ein Attribut 'lobby' in der User-Klasse, das die Lobby-ID speichert.
    users_in_lobby = User.query.filter_by(lobby=lobby_id).all()
    return users_in_lobby

