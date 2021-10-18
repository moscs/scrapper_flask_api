from flask.cli import FlaskGroup

from server import app, db, Posts
from server.scrapper import trip_scrapper

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("scrapper")
def launch_scrapper():
    app.logger.info('Starting scrapper')
    trip_scrapper(db, app, Posts)

if __name__ == "__main__":
    cli()