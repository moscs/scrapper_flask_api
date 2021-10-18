import uuid
import jwt
import datetime
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from . import scrapper


# Flask config
app = Flask(__name__)

app.config.from_object("server.config.Config")
db = SQLAlchemy(app)

# DB Models
class Users(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
     name = db.Column(db.String(50))
     password = db.Column(db.String(512))
     admin = db.Column(db.Boolean)

class Posts(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(50))
     date = db.Column(db.Date)
     author = db.Column(db.String(50))
     body = db.Column(db.String)

# Scrapper schedule
scheduler = BackgroundScheduler()
scheduler.configure({'apscheduler.daemon': False})
scheduler.start()
trigger = CronTrigger(hour=6, minute=0)
scheduler.add_job(scrapper.trip_scrapper, trigger, args=(db, app, Posts))


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
         data = jwt.decode(token, app.config.SECRET_KEY)
         current_user = Users.query.filter_by(public_id=data['public_id']).first()
      except:
         return jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator


@app.route('/register', methods=['GET', 'POST'])
def signup_user():  
 data = request.get_json()  

 hashed_password = generate_password_hash(data['password'], method='sha256')
 
 new_user = Users(name=data['name'], password=hashed_password, admin=False) 
 db.session.add(new_user)  
 db.session.commit()    

 return jsonify({'message': 'registered successfully'})



@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
 
  auth = request.authorization   

  if not auth or not auth.username or not auth.password:  
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

  user = Users.query.filter_by(name=auth.username).first()   
     
  if check_password_hash(user.password, auth.password):  
     token = jwt.encode({'public_id': str(user.public_id), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
     return jsonify({'token' : token}) 

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})



@token_required
@app.route('/threats', methods=['GET'])
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