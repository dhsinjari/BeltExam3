from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Pie:
    db_name='exam'
    def __init__(self,data):
        self.id = data['id'],
        self.name = data['name'],
        self.crust = data['crust'],
        self.filling = data['filling'],        
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def get_pie_by_id(cls, data):
        query= 'SELECT * FROM pies LEFT JOIN users on pies.user_id = users.id WHERE pies.id = %(pie_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def getAllPies(cls):
        query= 'SELECT * FROM pies ;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        pies= []
        if results:
            for row in results:
                pies.append(row)
            return pies
        return pies

    @classmethod
    def getAllPiesFromUser(cls, data):
        query= 'SELECT * FROM pies where pies.user_id=%(user_id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        pies= []
        if results:
            for row in results:
                pies.append(row)
            return pies
        return pies



    @classmethod
    def get_user_by_email(cls, data):
        query= 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]

    @classmethod
    def create_pie(cls,data):
        query = 'INSERT INTO pies (name,filling,crust,user_id) VALUES (%(name)s,%(filling)s,%(crust)s,%(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM pies WHERE id=%(pie_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_pie(cls,data1):
        query = 'UPDATE pies SET name=%(name)s,filling=%(filling)s,crust=%(crust)s,user_id=%(user_id)s WHERE pies.id=%(pie_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data1)


    @classmethod
    def get_logged_user_voted_pies(cls, data):
        query = 'SELECT pie_id as id FROM votes LEFT JOIN users on votes.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        piesVoted = []
        for row in results:
            piesVoted.append(row['id'])
        return piesVoted
    
    @classmethod
    def getPiesVotes(cls, data):
        query = 'SELECT votes.pie_id as id FROM pies LEFT JOIN votes on votes.pie_id = pies.id WHERE pie_id = %(pie_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        piesVoted = []
        for row in results:
            piesVoted.append(row['id'])
        return piesVoted

    @classmethod
    def addVote(cls, data):
        query= 'INSERT INTO votes (pie_id, user_id) VALUES ( %(pie_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeVote(cls, data):
        query= 'DELETE FROM votes WHERE pie_id = %(pie_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)



    @staticmethod
    def validate_pie(pie):
        is_valid = True
        if len(pie['name']) < 1:
            flash("All fields are required.", 'empty')
            is_valid = False

        if len(pie['filling']) < 1:
            flash("All fields are required.", 'empty')
            is_valid = False
        
        if len(pie['crust']) < 1:
            flash("All fields are required.", 'empty')
            is_valid = False
        return is_valid