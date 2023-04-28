from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import member_model
from flask import flash 
import re

class Game:
    db = "gameroom_db"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.member_id = data['member_id']
        self.member = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO games (title, description, member_id) VALUES (%(title)s, %(description)s, %(member_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def playing(cls):
        query = """SELECT * FROM games LEFT JOIN members ON games.member_id = members.id"""
        results = connectToMySQL(cls.db).query_db(query)
        gamers = []
        for video_game in results:
            game = cls(video_game)
            player_data = {
                'id' : video_game['members.id'],
                'f_name' : video_game['f_name'],
                'l_name' : video_game['l_name'],
                'email' : video_game['email'],
                'password' : video_game['password'],
                'created_at' : video_game['members.created_at'],
                'updated_at' : video_game['members.updated_at']
            }
            game.member = member_model.Member(player_data)
            gamers.append(game)
        return gamers
    
    @classmethod
    def one_game(cls, id):
        query = "SELECT * FROM games WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        return cls(results[0])
    
    @classmethod
    def edit_info(cls, data):
        query = "UPDATE games SET title = %(title)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_info(cls, id):
        query = "DELETE FROM games WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, {'id': id})
    
    @staticmethod
    def game_validator(game_info):
        is_vaild = True
        if len (game_info['title']) < 2:
            flash('Enter Game Title')
            is_vaild = False
        if len (game_info['description']) < 2:
            flash('Enter The Description Of The Game')
            is_vaild = False
        return is_vaild

