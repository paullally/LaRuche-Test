import os
import json
from flask import Flask, render_template, session, request, redirect
from flask import url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

# Defining variables database and MongoDB url
app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME')
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
#""" takes in json file and adds users to database"""
#with open("users.json") as json_file:
 # data = json.load(json_file)
#for d in data:
 # mongo.db.users.insert_one(d)


@app.route('/', methods=['POST','GET'])
def index():
  if request.method =='POST':
    user= {"first_name":request.form["first"],
    "last_name":request.form["last"]}
    try:
      mongo.db.users.insert_one(user)
      return redirect('/')
    except:
      return 'There was an error adding user'

  else:
    users=mongo.db.users.find()
    return render_template('index.html',users=users)

@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    mongo.db.users.remove({'_id': ObjectId(user_id)})
    return redirect('/')

@app.route('/edit_user/<user_id>')
def edit_user(user_id):
    this_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template('edituser.html', user=this_user)
  
@app.route('/update_users/<user_id>', methods=["POST"])
def update_users(user_id):
    users = mongo.db.users
    users.update({'_id': ObjectId(user_id)},
                 {
        'first_name': request.form.get('first'),
        'last_name':request.form.get('last'),
        
    })
    return redirect('/')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)