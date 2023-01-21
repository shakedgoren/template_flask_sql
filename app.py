import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
 
class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    age = db.Column(db.Integer)
 
    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age
 
@app.route('/students', methods = ['GET', 'POST'])
@app.route('/students/<id>', methods = ['DELETE', 'PUT'])
def studentsCrud(id=-1):
    if request.method == 'GET':
        res=[]
        for student in students.query.all():
            res.append({"id":student.id,"name":student.name,"city":student.city,"age":student.age})
        return(json.dumps(res))
    if request.method == 'POST':
        request_data = request.get_json()
        name= request_data['name']
        city = request_data['city']
        age= request_data['age']
        newStudent= students(name,city,age)
        db.session.add (newStudent)
        db.session.commit()
        return[]
    if request.method == 'DELETE':
        db.session.delete(students.query.get(id))
        db.session.commit()
        return{}
    if request.method == 'PUT':
        updStu=students.query.get(id)
        request_data = request.get_json()
        print(request_data)
        updStu.name =request_data['name']
        updStu.city =request_data['city']
        updStu.age =request_data['age']
        db.session.commit()
        return{}
   
if __name__ == '__main__':
    with app.app_context():db.create_all()
    app.run(debug = True)
