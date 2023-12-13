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
from copy import deepcopy

from extensions import socketio

lobby = Blueprint('lobby', __name__)

BOARDS = [Board()] * 10
GAME = [AI_Game(["red"], Board()), AI_Game([AIPlayer("red"),AIPlayer("blue"), AIPlayer("green"), AIPlayer("yellow")], BOARDS[2])]
USERS = [{}, None]
ACTIVE_GAME = [False, False]
COUNT = [0, 0]                      # First round counter
SEND_MATRIX_OLD = [None, None]
GIVE_UP_COUNTER = [0, 0]
ORDER = [None, None]
FINISHED_GAME = [False, False]

from functools import wraps
from flask import abort

def lobby_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user._lobby == 0:
            return redirect(url_for('lobby.join'))
        return func(*args, **kwargs)
    return decorated_function

########################################################################################################################################
# LOBBY ACTIONS

@lobby.route('/lobby')
@login_required
def join():
    return render_template('join_lobby.html', user_authenticated = current_user.is_authenticated)



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

@lobby.route('/lobby/clear_lobby')
@login_required
def clear_lobby():
    lobby = current_user._lobby
    user_id = current_user._id
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    db.clear_lobby(lobby, user_id)
    db.disconnect()
    return redirect(url_for('lobby.room'))

@lobby.route('/game')
@login_required
@lobby_required
def room():
    users = get_lobby_user()
    return render_template("game.html", lobby_id=current_user._lobby, users=users, board=None, user_authenticated = current_user.is_authenticated)

@lobby.route("/game/leave_lobby")
@login_required
@lobby_required
def room_leave_lobby():
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

    if lobby == 1:
        FINISHED_GAME[lobby] = False
        BOARDS[lobby] = Board()
        GAME[lobby] = AI_Game([AIPlayer("red"),AIPlayer("blue"), AIPlayer("green"), AIPlayer("yellow")], BOARDS[lobby])
        game = GAME[lobby]
        game.init_game()
        COUNT[lobby] = 0
        return render_template("board.html", board = game.board.matrix, name=current_user._name, color = game.active_player.color)

    if lobby == 0:
        FINISHED_GAME[lobby] = False
        BOARDS[lobby] = Board()
        users = get_lobby_user()
        if len(users) > 4:
            users = users[:4]
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

        if not ORDER[lobby]:
            GAME[lobby] = AI_Game(players, BOARDS[lobby])
            game = GAME[lobby]
            game.init_game()
            COUNT[lobby] = 0
            ORDER[lobby] = order
            for user, color in order:
                USERS[lobby][user] = color
            return render_template("user_board.html", board = game.board.matrix, order=ORDER[lobby], color = game.active_player.color)
        
        game = GAME[lobby]
        COUNT[lobby] = 0
        return render_template("user_board.html", board = Board().matrix, order=ORDER[lobby], color=game.active_player.color)
        
    return "Lobby not found (please use lobby 1 for usergame or 2 for ai game)"


########################################################################################################################################
# USER GAME EVENTS

# user inserts a block
@socketio.on('user_set_block')
def set_block(data):
    lobby = current_user._lobby - 1
    game = GAME[current_user._lobby - 1]
    color = game.active_player.color

    if not USERS[lobby][current_user._email] == color:
        return 

    block_matrix = data["block_matrix"]

    for idx1, x in enumerate(block_matrix):
        for idx2, y in enumerate(x):
            if y == False:
                block_matrix[idx1][idx2] = None


    block = Block(block_matrix, color)
    COUNT[lobby] = COUNT[lobby] + 1
    if COUNT[lobby] <=4:
        if game.board.is_first_move_valid(data["y"], data["x"], block):
            game.active_player.player_insert(data["block"], data["y"], data["x"])
        
            game.get_next_active_player()

            remaining_blocks = deepcopy(game.active_player.blocks)
            remaining_list = remaining_blocks.keys()
            for i in range(1,22):
                if i not in remaining_list:
                    remaining_blocks[i] = 0
                else:
                    remaining_blocks[i] = remaining_blocks[i].block_matrix


            send_matrix = [["X" for _ in range(20)] for _ in range(20)]
            for idx1, row in enumerate(game.board.matrix):
                for idx2, y in enumerate(row):
                    if y:
                        send_matrix[idx1][idx2] = y
            
            SEND_MATRIX_OLD[lobby] = send_matrix
            color = game.active_player.color
            if isinstance(game.active_player, AIPlayer):
                user_frontend = "AI"
            else:
                for user in USERS[lobby]:
                    if USERS[lobby][user] == color:
                        user_frontend = user
            socketio.emit('update_board', {'board': send_matrix, 'blocks': remaining_blocks, 'color': game.active_player.color, 'user': user_frontend})
            return "Hi"
        else:
            COUNT[lobby] = COUNT[lobby]-1

    
    
    else:
        if game.board.is_move_valid(data["y"], data["x"], block):
            game.active_player.player_insert(data["block"], data["y"], data["x"])

            send_matrix = [["X" for _ in range(20)] for _ in range(20)]
            for idx1, row in enumerate(game.board.matrix):
                for idx2, y in enumerate(row):
                    if y:
                        send_matrix[idx1][idx2] = y

            SEND_MATRIX_OLD[lobby] = send_matrix

            if len(game.active_player.blocks) == 0:
                ranking = []
                all_players = game.finished_players + game.players
                for player in all_players:
                    points = player.calc_points()
                    ranking.append((points, player.color))
                ranking.sort(key=lambda x: x[0])
                ranking = ranking[::-1]
                ORDER[lobby] = None
                USERS[lobby] = {}
                SEND_MATRIX_OLD[lobby] = None
                socketio.emit('finish_game', ranking)
                return 
           

            game.get_next_active_player()

            remaining_blocks = deepcopy(game.active_player.blocks)
            remaining_list = remaining_blocks.keys()
            for i in range(1,22):
                if i not in remaining_list:
                    remaining_blocks[i] = 0
                else:
                    remaining_blocks[i] = remaining_blocks[i].block_matrix

            if isinstance(game.active_player, AIPlayer):
                user_frontend = "AI"
            else:
                for user in USERS[lobby]:
                    if USERS[lobby][user] == game.active_player.color:
                        user_frontend = user
            
            socketio.emit('update_board', {'board': send_matrix, 'blocks': remaining_blocks, 'color': game.active_player.color, 'user': user_frontend})
            return "Hi"
        else:
            COUNT[lobby] = COUNT[lobby]-1

    return "Hi"


@socketio.on('set_block_user_game')
def handle_zug(zug):
    lobby = current_user._lobby - 1
    game = GAME[current_user._lobby - 1]

    if not isinstance(game.active_player, AIPlayer):
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
    
    if send_matrix == SEND_MATRIX_OLD[lobby]:
        
        surrender_color = game.active_player.color
        game.get_next_active_player()
        for i in range(len(game.players) - 1, -1, -1):
            if game.players[i].color == surrender_color:
                surrendering_player = game.players.pop(i)
        
        points = surrendering_player.calc_points()
        game.finished_players.append(surrendering_player)
        if len(game.finished_players) == 4:
            ranking = []
            for player in game.finished_players:
                points = player.calc_points()
                ranking.append((points, player.color))
            ranking.sort(key=lambda x: x[0])
            ranking = ranking[::-1]
            socketio.emit('finish_game', ranking)
            ORDER[lobby] = None
            USERS[lobby] = {}
            SEND_MATRIX_OLD[lobby] = None
        return 

    SEND_MATRIX_OLD[lobby] = send_matrix

    if len(game.active_player.blocks) == 0:
        ranking = []
        all_players = game.finished_players + game.players
        for player in all_players:
            points = player.calc_points()
            ranking.append((points, player.color))
        ranking.sort(key=lambda x: x[0])
        ranking = ranking[::-1]      
        socketio.emit('finish_game', ranking)
        ORDER[lobby] = None
        USERS[lobby] = {}
        SEND_MATRIX_OLD[lobby] = None
        FINISHED_GAME[lobby] = True  

        return 

    game.get_next_active_player()

    remaining_blocks = deepcopy(game.active_player.blocks)
    remaining_list = remaining_blocks.keys()
    for i in range(1,22):
        if i not in remaining_list:
            remaining_blocks[i] = 0
        else:
            remaining_blocks[i] = remaining_blocks[i].block_matrix

    if isinstance(game.active_player, AIPlayer):
        user_frontend = "AI"
    else:
        for user in USERS[lobby]:
            if USERS[lobby][user] == game.active_player.color:
                user_frontend = user    

    socketio.emit('update_board', {'board': send_matrix, 'blocks': remaining_blocks, 'color': game.active_player.color, 'user': user_frontend})   
    return "Hi"



@socketio.on('give_up')
def surrender():
    lobby = current_user._lobby - 1
    game = GAME[current_user._lobby - 1]
    color = game.active_player.color
    COUNT[lobby] = COUNT[lobby] + 1
    surrender_color = USERS[lobby][current_user._email] 
    if surrender_color == color:
        game.get_next_active_player()
    
    for i in range(len(game.players) - 1, -1, -1):
        if game.players[i].color == surrender_color:
            surrendering_player = game.players.pop(i)
    
    points = surrendering_player.calc_points()
    game.finished_players.append(surrendering_player)
    if len(game.finished_players) == 4:
        ranking = []
        for player in game.finished_players:
            points = player.calc_points()
            ranking.append((points, player.color))
        ranking.sort(key=lambda x: x[0])
        ranking = ranking[::-1]
        ORDER[lobby] = None
        USERS[lobby] = {}
        SEND_MATRIX_OLD[lobby-1] = None
        socketio.emit('finish_game', ranking)
    return

@socketio.on('send_message')
def handle_message(message):
    email = current_user._email
    msg = f"{email}: {message}"
    socketio.emit('chat_message', msg)
    return "Hi"


@socketio.on('user_rotate_block')
def rotate_block(block_id):
    block_id = int(block_id) + 1
    lobby = current_user._lobby - 1
    game = GAME[current_user._lobby - 1]
    color = game.active_player.color

    if not USERS[lobby][current_user._email] == color:
        return 

    game.active_player.blocks[block_id].rotate()

    remaining_blocks = deepcopy(game.active_player.blocks)
    remaining_list = remaining_blocks.keys()
    for i in range(1,22):
        if i not in remaining_list:
            remaining_blocks[i] = 0
        else:
            remaining_blocks[i] = remaining_blocks[i].block_matrix

    if isinstance(game.active_player, AIPlayer):
        user_frontend = "AI"
    else:
        for user in USERS[lobby]:
            if USERS[lobby][user] == game.active_player.color:
                user_frontend = user

    send_matrix = [["X" for _ in range(20)] for _ in range(20)]
    for idx1, row in enumerate(game.board.matrix):
        for idx2, y in enumerate(row):
            if y:
                send_matrix[idx1][idx2] = y  

    socketio.emit('update_board', {'board': send_matrix, 'blocks': remaining_blocks, 'color': game.active_player.color, 'user': user_frontend})   
    return "Hi"

@socketio.on('user_reflect_block')
def reflect_block(block_id):
    block_id = int(block_id) + 1
    lobby = current_user._lobby - 1
    game = GAME[current_user._lobby - 1]
    color = game.active_player.color

    if not USERS[lobby][current_user._email] == color:
        return 

    game.active_player.blocks[block_id].reflect()

    remaining_blocks = deepcopy(game.active_player.blocks)
    remaining_list = remaining_blocks.keys()
    for i in range(1,22):
        if i not in remaining_list:
            remaining_blocks[i] = 0
        else:
            remaining_blocks[i] = remaining_blocks[i].block_matrix

    if isinstance(game.active_player, AIPlayer):
        user_frontend = "AI"
    else:
        for user in USERS[lobby]:
            if USERS[lobby][user] == game.active_player.color:
                user_frontend = user

    send_matrix = [["X" for _ in range(20)] for _ in range(20)]
    for idx1, row in enumerate(game.board.matrix):
        for idx2, y in enumerate(row):
            if y:
                send_matrix[idx1][idx2] = y  

    socketio.emit('update_board', {'board': send_matrix, 'blocks': remaining_blocks, 'color': game.active_player.color, 'user': user_frontend})   
    return "Hi"

@socketio.on('user_is_move_valid')
def is_move_valid(data):
    lobby = current_user._lobby - 1
    game = GAME[lobby]

    y = data["y"]
    x = data["x"]
    block_idx = data["block"]

    block = game.active_player.blocks[block_idx]

    res = game.board.is_move_valid(y, x, block)
    socketio.emit('move_valid_response', res)
    return "-"

########################################################################################################################################
### AI GAME EVENTS

# AI sets block
@socketio.on('zug_gemacht')
def handle_zug(zug):
    global SEND_MATRIX_OLD
  
    lobby = current_user._lobby - 1

    if FINISHED_GAME[lobby]:
        return

    game = GAME[current_user._lobby - 1]
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
    
 
    if send_matrix == SEND_MATRIX_OLD[lobby]:
        
        surrender_color = game.active_player.color
        game.get_next_active_player()
        for i in range(len(game.players) - 1, -1, -1):
            if game.players[i].color == surrender_color:
                surrendering_player = game.players.pop(i)
        
        points = surrendering_player.calc_points()
        game.finished_players.append(surrendering_player)
        if len(game.finished_players) == 4:
            FINISHED_GAME[lobby] = True
            ranking = []
            for player in game.finished_players:
                points = player.calc_points()
                ranking.append((points, player.color))
            ranking.sort(key=lambda x: x[0])
            ranking = ranking[::-1]
            socketio.emit('finish_ai_game', ranking)
            game.finished_players=[]
            ORDER[lobby] = None
            USERS[lobby] = {}
            SEND_MATRIX_OLD[lobby] = None
            GAME[lobby] = None
            return
    
    SEND_MATRIX_OLD[lobby] = send_matrix
   

    game.get_next_active_player()

    remaining_blocks = deepcopy(game.active_player.blocks)
    remaining_list = remaining_blocks.keys()
    for i in range(1,22):
        if i not in remaining_list:
            remaining_blocks[i] = 0
        else:
            remaining_blocks[i] = remaining_blocks[i].block_matrix

    if isinstance(game.active_player, AIPlayer):
        user_frontend = "AI"
    else:
        for user in USERS[lobby]:
            if USERS[lobby][user] == game.active_player.color:
                user_frontend = user    
    

    socketio.emit('update_ai_board', {'board': send_matrix, 'blocks': remaining_blocks, 'color': game.active_player.color, 'user': user_frontend})   
    return "Hi"




########################################################################################################################################
## Further Functions

@socketio.on('join_room')
def join_room(lobby_id):
    user_id = session.get('user_id')
    socketio.emit('join_lobby', {'user_id': user_id}, room=lobby_id)
    return 'Joined lobby'

@socketio.on('disconnect')
def user_disconnect():
    lobby = current_user._lobby - 1
    try:
        surrender()
    except:
        pass
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    db.update_user((current_user._id, "lobby", 0))
    db.disconnect()
    if not get_lobby_user(lobby + 1):
        FINISHED_GAME[lobby] = True
        ORDER[lobby] = None
        USERS[lobby] = {}
        SEND_MATRIX_OLD[lobby] = None
        GAME[lobby] = None
        
    logout_user()

    return 'Joined lobby'

def get_lobby_user(lobby = None):
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    if not lobby:
        loaded_users = db.get_users_in_lobby(current_user._lobby)
    else:
        loaded_users = db.get_users_in_lobby(lobby)
    users = []
    for user in loaded_users:
        users.append(user[0])
    db.disconnect()
    return users

def finish_game(lobby):
    ORDER[lobby-1] = None
    USERS[lobby-1] = {}
    SEND_MATRIX_OLD[lobby-1] = None
    return

def update_highscore(ranking):
    pass