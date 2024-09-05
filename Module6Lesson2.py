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

class MembersSchema(ma.Schema):
    name=fields.String(required=True)
    age=fields.String(required=True)
    
    class Meta:
        fields=("name","age")
               
member_schema =MembersSchema()
members_schema=MembersSchema(many=True)

#makes connection with mySql
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

#Gets all the members info
@app.route('/')
def home():
    return "Welcome to the gym membership databse"

@app.route ("/members",methods=["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}),500
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM Members"
        
        cursor.execute(query)
        
        members = cursor.fetchall()
        
        return members_schema.jsonify(members)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error:""internal server error"}),500
       
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
 #adds new members           
@app.route("/members", methods = ["POST"])
def add_members():
    try:
        member_data = member_schema.load (request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages),400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify ({"Error": "Database connection failed"}),500
        cursor = conn.cursor()
        
        new_member =(member_data['name'],member_data['age'])
        
        query ="INSERT INTO Members (name,age) VALUES(%s,%s)"
        
        cursor.execute(query,new_member)
        conn.commit()
        
        return jsonify({'message': 'New member added succesfully'}),201
    except Error as e:
        print(f"Error:{e}")
        
        return jsonify({"error": "Internal Server Error"}),500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
#updates member info         
@app.route("/members/<int:id>", methods=['PUT'])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.message),400
    
    try:
        conn =get_db_connection()
        if conn is None:
            return jsonify({"error" "Database connection failed"}),500
        cursor = conn.cursor()
        
        updated_member = (member_data ["name"], member_data ["age"],id)
        
        query = 'UPDATE Members SET name = %s, age = %s WHERE id = %s'
        
        cursor.execute(query,updated_member)
        conn.commit()
        
        return jsonify({"message" : "Member updated"}),201
    except Error as e:
        print (f'Error: {e}')
        
        return jsonify({"error":"Internal Server Error"}),500
    finally: 
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
   #deletes member         
@app.route("/members/<int:id>", methods=['DELETE'])
def delete_member(id):
    
    try:
        conn =get_db_connection()
        if conn is None:
            return jsonify({"error" "Database connection failed"}),500
        cursor = conn.cursor()
        member_to_remove=(id,)
        cursor.execute("SELECT * FROM Members where id =%s", member_to_remove)
        customer=cursor.fetchone()
        if not customer:
            return jsonify({"error":"Member not found"}),404
        
        query ="DELETE FROM Members WHERE id = %s"
        cursor.execute(query,member_to_remove)
        conn.commit()
        
        return jsonify({"message" : "Member removed successfully"}),200
    except Error as e:
        print (f'Error: {e}')
        
        return jsonify({"error":"Internal Server Error"}),500
    finally: 
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
                               
if __name__ =='__main__':
    app.run(debug=True)
            
        
                
    
    
    
    

    