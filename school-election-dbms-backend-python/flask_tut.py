import json
import psycopg2
import psycopg2.extras
import jwt
from flask import Flask, request
app = Flask(__name__)
connection = psycopg2.connect("dbname=dbmsproject user=dev")

@app.before_first_request
def startup_check():
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    #school db
    cur.execute('''
            CREATE TABLE IF NOT EXISTS schools (
            id serial PRIMARY KEY NOT NULL,
            name text NOT NULL,
            email text NOT NULL,
            password text NOT NULL
        );
    ''')

    #classes db
    cur.execute('''
        CREATE TABLE IF NOT EXISTS school_classes (
        id serial PRIMARY KEY NOT NULL,
        school_id int NOT NULL,
        name text NOT NULL,
        boys int NOT NULL,
        girls int NOT NULL
    );
    ''')

    #elections db
    cur.execute('''
        CREATE TABLE IF NOT EXISTS elections(
        id serial PRIMARY KEY NOT  NULL,
        school_id int NOT NULL,
        name text NOT NULL,
        presidential bool NOT NULL,
        genders int NOT NULL
    );
    ''')

    #candidates db
    cur.execute('''
        CREATE TABLE IF NOT EXISTS candidates(
        id serial PRIMARY KEY NOT NULL,
        name text NOT NULL,
        school_id int NOT NULL,
        election_id int NOT NULL,
        class_id int NOT NULL,
        gender int NOT NULL,
        symbol text NOT NULL
    );
    ''')

    #votes db
    cur.execute('''
        CREATE TABLE IF NOT EXISTS votes(
        id serial PRIMARY KEY NOT NULL,
        candidate_id int NOT NULL
    );
    ''')

    #voted db
    cur.execute('''
        CREATE TABLE IF NOT EXISTS voted(
        id serial PRIMARY KEY NOT NULL,
        voter_num int NOT NULL,
        class_id int NOT NULL
    );
    ''')

    connection.commit()
    cur.close()

#---------------------------------------------------------------------

@app.route('/signup',methods=['POST'])
def school_signup():
    data = request.json

    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('''
        INSERT INTO schools(name,email,password)
        VALUES(%s,%s,%s) RETURNING *;
    ''',
    (data["name"],data["email"],data["password"])
    )
    
    row = cur.fetchone()
    connection.commit()

    if row == None:
        return {
            "success" : False,
            "message" : "insert : failed in school_classes"
        }
    else:
        return {
            "success":True,
            "message": "success",
            "data":{
                "id": row[0],
                "name": row["name"],
                "email": row["email"],
                "password": row["password"]
                }
        }

#---------------------------------------------------------------------

@app.route('/login',methods=['POST'])
def school_login():
    data = request.json

    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('''
        SELECT * 
        FROM schools
        WHERE  email = %(email)s AND password = %(password)s;
    ''',
    data)
    

    school = cur.fetchone()
    
    if school == None:
        return {
                "success": False,
                "message": "login failed",
                }
    else:
        school_id = school[0]
        enc_token = jwt.encode({'id': school_id }, 'secret', algorithm='HS256')
        return {
                "success": True,
                "message": "Login success",
                "data": enc_token.decode("utf-8")         # token
               }

#---------------------------------------------------------------------

def get_id_from_header():
    
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    enc_id = request.headers["Authorization"]
    dec_id = enc_id.split(" ")[1]
    
    school_id_json = None
    
    try:
        school_id_json = jwt.decode(dec_id, 'secret', algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        pass

    if school_id_json == None:
        return None
    else:
        return school_id_json["id"]

#---------------------------------------------------------------------

@app.route('/profile',methods=['GET'])
def school_profile():

    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    req_school_id=get_id_from_header()  
    if req_school_id == None:
        return ({"success": False, "message": "Token error"}, 401)  

    cur.execute('''
        SELECT * 
        FROM schools
        WHERE  id = %s;
    ''',
    (req_school_id,))

    school = cur.fetchone()
    return {
            "success": True,
            "message": "Login Successful",
            "data": {
                    "id": school[0],
                    "name": school[1],
                    "email": school[2],
                    "password": school[3],
                    }
            }
#---------------------------------------------------------------------
#error
@app.route('/classes',methods=['GET'])
def get_classes():
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    req_school_id = get_id_from_header()
    if req_school_id == None:
        return ({"success": False, "message": "Token error"}, 401)  


    cur.execute('''
        SELECT * 
        FROM school_classes
        WHERE school_id = %s;
        ''',
        (req_school_id,)
    )

    classes_list = []
    selected_rows = cur.fetchall()

    for row in selected_rows:

        ob = {}
        ob["id"] = row[0]
        ob["school_id"] = row[1]
        ob["name"] = row[2]
        ob["boys"] = row[3]
        ob["girls"] = row[4]

        classes_list.append(ob)
    
    return {
            "success" : True,
            "message" : "Classes selected successfully",
            "data" : classes_list 
            }

#---------------------------------------------------------------------

@app.route('/classes',methods=['POST'])
def add_classes():
    
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    req_school_id = get_id_from_header()
    if req_school_id == None:
        return ({"success": False, "message": "Token error"}, 401)  


    data = request.json

    cur.execute('''
        INSERT INTO school_classes(school_id,name,boys,girls)
        VALUES( %s,%s,%s,%s) RETURNING *;
    ''',
    (req_school_id,data["name"],data["boys"],data["girls"])
    )

    row = cur.fetchone()
    connection.commit()

    if row == None:
        return {
            "success" : False,
            "message" : "insert : failed in school_classes"
        }
    return {
            "success" : True,
            "message" : "class added successfully",
            "data" : {
                "id": row[0],
                "school_id" : req_school_id,
                "name" : row["name"],
                "boys" : row["boys"],
                "girls" : row["girls"],
                }
        }

#---------------------------------------------------------------------

@app.route('/classes/<int:id>',methods=['PUT'])
def update_classes(id):

    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    data = request.json

    req_school_id = get_id_from_header()
    if req_school_id == None:
        return ({"success": False, "message": "Token error"}, 401)  


    cur.execute('''
        UPDATE school_classes
        SET name = %s,
            boys = %s ,
            girls = %s
        WHERE id = %s
        RETURNING *;
    ''',
    (data["name"],data["boys"],data["girls"],id)
    )

    row = cur.fetchone()
    connection.commit()

    if row == None:
        return {
            "success" : False,
            "message" : "Update : id not found in school_classes"
        }
    else:    
        return {
                "success" : True,
                "message" : "table updated successfully",
                "data" : {
                    "id" : id,
                    "school_id" : req_school_id,
                    "name" : row["name"],
                    "boys" : row["boys"],
                    "girls" : row["girls"],
                }
        }

#---------------------------------------------------------------------

@app.route('/classes/<int:id>',methods=['DELETE'])
def delete_classes(id):  

    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    req_school_id = get_id_from_header()
    if req_school_id == None:
        return ({"success": False, "message": "Token error"}, 401)  


    cur.execute('''
        DELETE FROM school_classes
        WHERE id = %s
        RETURNING *;
    ''',
    (id,)
    )

    row = cur.fetchone()
    connection.commit()

    if row == None:
        return {
            "success" : False,
            "message" : "delete: id not found in school_classes"
        }
    else:
        return {
                "success" : True,
                "message" : "row deleted successfully",
                "data" : {
                    "id" : id,
                    "school_id" : req_school_id,
                    "name" : row["name"],
                    "boys" : row["boys"],
                    "girls" : row["girls"],
                }
        }

#---------------------------------------------------------------------
#error
@app.route('/elections',methods=['GET'])
def get_election_details():

    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    req_school_id = get_id_from_header()
    if req_school_id == None:
        return ({"success": False, "message": "Token error"}, 401)  


    cur.execute('''
        SELECT *
        FROM elections
        WHERE school_id = %s;
    ''',
    (req_school_id,)
    )

    selected_rows = cur.fetchall()
    print(selected_rows)

    elecitons_list = []
    
    for row in selected_rows:

        #print("row",row)
        ob = {}

        ob["id"] = row[0]
        ob["school_id"] = row[1]
        ob["name"] = row[2]
        ob["presedential"] = row[3]
        ob["genders"] = row[4]

        #print("ob",ob)

        elecitons_list.append(ob) 
        #print(elecitons_list)

    return {
            "success" : True,
            "message" : "list fetched successfully",
            "data" : elecitons_list
        }

#---------------------------------------------------------------------

@app.route('/elections',methods=['POST'])
def add_elections():
    
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    req_school_id = get_id_from_header()
    if req_school_id == None:
        return ({"success": False, "message": "Token error"}, 401)  


    data = request.json

    cur.execute('''
        INSERT INTO elections(school_id,name,presidential,genders)
        VALUES( %s,%s,%s,%s) RETURNING *;
    ''',
    (req_school_id,data["name"],data["presidential"],data["genders"])
    )

    row = cur.fetchone()
    connection.commit()

    if row == None:
        return {
            "success" : False,
            "message" : "insert :  operaiton not success"
        }
    else:
        return {
                "success" : True,
                "message" : "election details added successfully",
                "data" : {
                    "id": row[0],
                    "school_id" : req_school_id,
                    "name" : row["name"],
                    "presidential" : row["presidential"],
                    "genders" : row["genders"],
                    }
            }

#---------------------------------------------------------------------


@app.route('/elections/<int:id>',methods=['PUT'])
def update_elections(id):

    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    data = request.json

    req_school_id = get_id_from_header()
    if req_school_id == None:
        return ({"success": False, "message": "Token error"}, 401)  


    cur.execute('''
        UPDATE elections
        SET name = %s ,
            presidential = %s,
            genders = %s
        WHERE id = %s
        RETURNING *;
    ''',
    (data["name"],data["presidential"],data["genders"],id)
    )

    row = cur.fetchone()
    connection.commit()

    if row == None:
        return {
            "success" : False,
            "message" : "Update : id not found in elections"
        }
    else:
        return {
                "success" : True,
                "message" : "table updated successfully",
                "data" : {
                    "id" : id,
                    "school_id" : req_school_id,
                    "name" : row["name"],
                    "presidential" : row["presidential"],
                    "genders" : row["genders"],
                }
        }

#---------------------------------------------------------------------

@app.route('/elections/<int:id>',methods=['DELETE'])
def delete_elections(id):  

    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    req_school_id = get_id_from_header()
    if req_school_id == None:
        return ({"success": False, "message": "Token error"}, 401)  


    cur.execute('''
        DELETE FROM elections
        WHERE id = %s RETURNING *
    ''', (id,)
    )

    row = cur.fetchone()
    connection.commit()

    if row == None:
        return {
            "success" : False,
            "message" : "Delete : id not found in elections"
        }
    else:
        return {
                "success" : True,
                "message" : "row deleted successfully",
                "data" : {
                    "id" : id,
                    "school_id" : req_school_id,
                    "name" : row["name"],
                    "presidential" : row["presidential"],
                    "genders" : row["genders"],
                }
        }
