from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from  pinglun import app
from model import User,Question, Comment

manage = Manager(app)

migrate = Migrate(app, db)

manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()