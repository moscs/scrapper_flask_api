from api.webapp import app
from api.scrapper import trip_scrapper
from flask_migrate import Migrate
from api.models.models import db, Posts
from flask.cli import FlaskGroup

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    app.logger.info('Init db')
    db.init_app(app)
    app.logger.info('migrate db')
    migrate = Migrate(app, db)
    app.logger.info('create all')
    db.create_all()

@cli.command("scrapper")
def launch_scrapper():
    app.logger.info('Starting scrapper')
    trip_scrapper(db, app, Posts)

if __name__ == "__main__":
    cli()