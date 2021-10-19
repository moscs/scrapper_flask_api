import jwt
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from api.models.models import Posts, Users
from functools import wraps


db = SQLAlchemy()

# Endpoints
def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']

      if not token:
         return jsonify({'message': 'a valid token is missing'})

      try:
         data = jwt.decode(token, os.getenv("SECRET", 'Th1s1ss3cr3t'))
         current_user = Users.query.filter_by(public_id=data['public_id']).first()
      except:
         return jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator


def signup_user():  
 data = request.get_json()  

 hashed_password = generate_password_hash(data['password'], method='sha256')
 
 new_user = Users(name=data['name'], password=hashed_password, admin=False) 
 db.session.add(new_user)  
 db.session.commit()    

 return jsonify({'message': 'registered successfully'})



def login_user(): 
 
  auth = request.authorization   

  if not auth or not auth.username or not auth.password:  
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

  user = Users.query.filter_by(name=auth.username).first()   
     
  if check_password_hash(user.password, auth.password):  
     token = jwt.encode({'public_id': str(user.public_id), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
     return jsonify({'token' : token}) 

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


#@token_required
def get_threats():
   
   posts = Posts.query.all()

   output = []
   for post in posts:

         post_data = {}
         post_data['author'] = post.author
         post_data['date'] = post.date
         post_data['body'] = post.body
         output.append(post_data)

   return jsonify({'list_of_posts' : output})

