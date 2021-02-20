from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_avatars import Avatars
import logging
from logging.handlers import SMTPHandler
from flask_mail import Mail
from flask_moment import Moment
from flask_uploads import configure_uploads, IMAGES, UploadSet, UploadNotAllowed
from sqlalchemy import MetaData

app = Flask(__name__)
app.config.from_object(Config)

images = UploadSet('images', IMAGES)
configure_uploads(app,images)

bootstrap = Bootstrap(app)


db = SQLAlchemy(app)


migrate = Migrate(app,db, render_as_batch=True)

login = LoginManager(app)
login.login_view='login' #points to the url_for('login') to handle the view

avatars=Avatars(app)

mail = Mail(app)

moment = Moment(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr = 'no-reply@' + app.config['MAIL_SERVER'],
            toaddrs = app.config['ADMINS'], subject = "HoVuXomMoi Failure",
            credentials=auth,
            secure=secure

        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


from app import routes, models, errors



