from flask import Flask
from api.models.models import db, Posts
from api.routes.threat_bp import threats_bp
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from . scrapper import trip_scrapper
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('api.config.Config')
db.init_app(app)

app.register_blueprint(threats_bp)


# Scrapper schedule
scheduler = BackgroundScheduler()
scheduler.configure()
scheduler.start()
trigger = CronTrigger(hour=6, minute=0)
scheduler.add_job(trip_scrapper, trigger, args=(db, app, Posts))