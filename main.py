from game import Game
from DataBase.database import conn

if __name__ == '__main__':
    try:
        app=Game()
        app.run()
    finally:
        conn.close()