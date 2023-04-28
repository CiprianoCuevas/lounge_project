from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

user_regex = re.compile(r'^[a-zA-Z]')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(r'^[a-zA-Z0-9]')

class Member:
    db = "gameroom_db"
    def __init__(self, data):
        self.id = data['id']
        self.f_name = data['f_name']
        self.l_name = data['l_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.member = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO members(f_name, l_name, email, password) VALUES (%(f_name)s, %(l_name)s, %(email)s, %(password)s)"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def display_all_member(cls):
        query = "SELECT * FROM members"
        results = connectToMySQL(cls.db).query_db(query)
        members = []
        for member in results:
            members.append(cls(member))
        return members
    
    @classmethod
    def show_member(cls, data):
        query = "SELECT * FROM members WHERE email= %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        if len(results)<1:
            return False
        return cls(results[0])
    
    @classmethod
    def show_gamer(cls, id):
        query = "SELECT * FROM members WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, {'id':id})
        return cls(results[0])
    
    @staticmethod
    def validator(member_info):
        is_valid = True
        query = "SELECT * FROM members WHERE email = %(email)s;"
        results = connectToMySQL(Member.db).query_db(query, member_info)
        if not user_regex.match(member_info['f_name']):
            flash("Enter Your First Name")
            is_valid = False
        if not user_regex.match(member_info['l_name']):
            flash("Enter Your last Name")
            is_valid = False
        if not email_regex.match(member_info['email']):
            flash('Enter Your Email/Password')
            is_valid = False
        if Member.show_member({'email': member_info['email']}):
            flash('Please Login Member')
            is_valid = False
        if not password_regex.match(member_info['password']):
            flash('Please Enter Correct Information')
            is_valid = False
        if member_info['confirm_password'] != member_info['password']:
            flash('Enter You Information Again')
            is_valid = False
        return is_valid
