import requests
import json
import mysql




from flask import Flask,jsonify,request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error
from password import my_password

app = Flask(__name__)
ma = Marshmallow(app)

class ScheduelSchema(ma.Schema):
    workout_type=fields.String(required=True)
    day=fields.String(required=True)
    member_id=fields.String(required=True)
    
    class Meta:
        fields=("workout_type","day","member_id")
               
scheduel_schema =ScheduelSchema()
scheduels_schema=ScheduelSchema(many=True)

#establishes connection to mySql
def get_db_connection():
    db_name ="gym_membership_sql_db"
    user ="root"
    password = "#Comco92505"
    host ="localhost"
    
    try:
        conn=mysql.connector.connect(
            database=db_name,
            user = user,
            password = password,
            host=host
        )
        print('Connected to MySql successfully')
        return conn
    except Error as e:
        print(f"Error:{e}")
        return None
    
#Gets all schedeles
@app.route('/')
def home():
    return "Welcome to the gym membership databse"

@app.route ("/scheduel",methods=["GET"])
def get_scheduel():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}),500
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM Scheduel"
        
        cursor.execute(query)
        
        scheduel = cursor.fetchall()
        
        return scheduels_schema.jsonify(scheduel)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error:""internal server error"}),500
       
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
 #adds new workout            
@app.route("/scheduel", methods = ["POST"])
def add_scheduel():
    try:
        scheduel_data =scheduel_schema.load (request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages),400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify ({"Error": "Database connection failed"}),500
        cursor = conn.cursor()
        
        new_scheduel =(scheduel_data['workout_type'],scheduel_data['day'],scheduel_data["member_id"])
        
        query ="INSERT INTO Scheduel (workout_type,day,member_id) VALUES(%s,%s,%s)"
        
        cursor.execute(query,new_scheduel)
        conn.commit()
        
        return jsonify({'message': 'New Schedule added succesfully'}),201
    except Error as e:
        print(f"Error:{e}")
        
        return jsonify({"error": "Internal Server Error"}),500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
#updates schedule info         
@app.route("/scheduel/<int:id>", methods=['PUT'])
def update_scheduel(id):
    try:
       scheduel_data = scheduel_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.message),400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error" "Database connection failed"}),500
        cursor = conn.cursor()
        
        update_scheduel = (scheduel_data ["workout_type"], scheduel_data ["day"],scheduel_data ["member_id"],id)
        
        query = 'UPDATE Scheduel SET workout_type = %s, day = %s, member_id = %s WHERE id = %s'
        
        cursor.execute(query,update_scheduel)
        conn.commit()
        
        return jsonify({"message" : "Schedule updated"}),201
    except Error as e:
        print (f'Error: {e}')
        
        return jsonify({"error":"Internal Server Error"}),500
    finally: 
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
#GETS schedule for a specific member

@app.route ("/scheduel/<int:id>",methods=["GET"])
def get_member_scheduel(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}),500
        cursor = conn.cursor(dictionary=True)
        
        member= (id,)
        
        query = "SELECT * FROM Scheduel WHERE Member_id = %s"
        
        cursor.execute(query,member)
        
        scheduel = cursor.fetchall()
        
        return scheduels_schema.jsonify(scheduel)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error:""internal server error"}),500
       
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
if __name__ =='__main__':
    app.run(debug=True)