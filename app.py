from flask import Flask
from flask_login import LoginManager
from classes.User import User
from database.db_manager import DB_Manager
from extensions import socketio

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db = DB_Manager("database/kundendatenbank.sql", "users")
        db.connect()
        data = db.get_mail_and_name_by_id(user_id)
        if not data:
            return None
        lobby = db.get_lobby(user_id)
        db.disconnect()                                  
        return User(int(user_id), data[0], data[1], lobby[0])


    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from lobby import lobby as lobby_blueprint
    app.register_blueprint(lobby_blueprint)
    
    from game import game as game_blueprint
    app.register_blueprint(game_blueprint)

    socketio.init_app(app)
    #app.register_blueprint(socketio_blueprint, url_prefix='/socketio')
    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
    #app.run(host='localhost', port=5000, debug=True)