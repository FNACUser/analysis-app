

from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_security.utils import hash_password
from flask_security import Security
from flask_seeder import FlaskSeeder
# import defaultapp.loggers
from sqlalchemy import exc
# Bokeh && Tornado
from tornado.ioloop import IOLoop
from threading import Thread

from bokeh.server.server import Server
from bokeh.util.logconfig import basicConfig
import click

#Logger

import logging
import os

from defaultapp.config import Config
from defaultapp.miscelaneous import mail, bcrypt
from defaultapp.models import db, User, Role, user_datastore, IRA_Organization_areas

from defaultapp.bkhapps.common.Utilities import generate_random_string
# from defaultapp.bkhapps.encuestas.oahubIRASurveyMain import run_ira_forms
# from defaultapp.bkhapps.analisis.heatmap_final import heatmap
# from defaultapp.bkhapps.analisis.sql_narrativas import narrativas
# from defaultapp.bkhapps.aem.oihub_AEM_hm import aem
# from defaultapp.bkhapps.aem.oihub_IRA_load_n_colegio import mysql_to_neo4j_ETL
# from defaultapp.bkhapps.evaluacion.alcaparros_evaluacion_individual_plots import eval_individual
# from defaultapp.bkhapps.evaluacion.alcaparros_evaluacion_total_plots import eval_total
# from defaultapp.bkhapps.affini_scripts.BM.oihub_BM_Main import BM_launch
from defaultapp.bkhapps.ActorActor_IRA.oihub_AA_IRA_NWM1_Q1 import AA_IRA_launch
from defaultapp.bkhapps.ActorKnowledge_IRA.domecq_conocimientos_plots import AK_IRA_launch
from defaultapp.bkhapps.CVF_IRA.oihub_CVF_Model import CVF_launch

#from defaultapp.bkhapps.analisis.CVF_analysis import run_CVF_analysis


# from logging.config import dictConfig

# db = SQLAlchemy()
# bcrypt = Bcrypt()
# login_manager = LoginManager()
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'error'
# mail = Mail()


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py

    basicConfig(level=Config.BOKEH_DEBUG_LEVEL)

    if Config.FLASK_ENV == 'production':
        server = Server(
            {'/ActorActor': AA_IRA_launch,
             '/ActorKnowledge': AK_IRA_launch,
             '/Values': CVF_launch
             },
            io_loop=IOLoop(),
            port=int(Config.BOKEH_PORT),
            allow_websocket_origin=[Config.BOKEH_URL.replace('https://', '') + ":80",
                                    Config.BOKEH_URL.replace('https://', '') + ":443"],
            sign_sessions=Config.BOKEH_SIGN_SESSIONS,
            generate_session_ids=False,
            secret_key=Config.BOKEH_SECRET_KEY,
            ssl_certfile=Config.SSL_CERT_FILE,
            ssl_keyfile=Config.SSL_KEY_FILE
        )
    else:
        server = Server(
            {'/ActorActor': AA_IRA_launch,
             '/ActorKnowledge': AK_IRA_launch,
             '/Values': CVF_launch
             },
            io_loop=IOLoop(),
            port=int(Config.BOKEH_PORT),
            allow_websocket_origin=[Config.BOKEH_URL.replace('http://', '') + ":5000",
                                    "127.0.0.1:5000"],
            sign_sessions=Config.BOKEH_SIGN_SESSIONS,
            generate_session_ids=False,
            secret_key=Config.BOKEH_SECRET_KEY,
            ssl_certfile='',
            ssl_keyfile='',

        )

    server.start()
    server.io_loop.start()


def setLogger(app):

    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')

    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = log_file, level=logging.ERROR)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler(log_file)
    fileHandler.setLevel(logging.ERROR)
    fileHandler.setFormatter(formatter)

    app.logger.addHandler(fileHandler)
    app.logger.info("Logging is set up.")


def create_app():
    app = Flask(__name__)

    # @app.after_request
    # def add_header(r):
    #     """
    #     Add headers to both force latest IE rendering engine or Chrome Frame,
    #     and also to cache the rendered page for 10 minutes.
    #     """
    #     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #     r.headers["Pragma"] = "no-cache"
    #     r.headers["Expires"] = "0"
    #     r.headers['Cache-Control'] = 'public, max-age=0'
    #     return r

    setLogger(app)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    migrate = Migrate(app, db)

    seeder = FlaskSeeder()
    seeder.init_app(app, db)

    from defaultapp.bkhapps.routes import bkhapps
    from defaultapp.users.routes import users
    from defaultapp.posts.routes import posts
    from defaultapp.main.routes import main
    from defaultapp.errors.handlers import errors

    app.register_blueprint(bkhapps)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # security

    # with app.app_context():
    Security(app, datastore=user_datastore)

    # Starts Bokeh Workers

    Thread(target=bk_worker).start()

    # custom commands

    @click.command(name="crear_usuario")
    @with_appcontext
    @click.argument("name", nargs=1)
    @click.argument("email", nargs=1)
    @click.argument("area", nargs=1)
    @click.argument("roles", nargs=-1)
    def crear_usuario(name, email, area, roles):
        try:

            model_area = IRA_Organization_areas.query.filter_by(Organization_area=area).first()

            if model_area:
                id_area = model_area.id_organization_area
            else:
                id_area = None

            new_user = user_datastore.create_user(username=name, email=email, id_organization_area=id_area,
                                                  password=hash_password(generate_random_string()))
            db.session.add(new_user)
            for role in roles:
                click.echo(f"role {role}")
                r = Role.query.filter_by(name=role).first()
                user_datastore.add_role_to_user(new_user, r)

            db.session.commit()
        except exc.IntegrityError as ei:
            print('Duplicidad de Email, usuario ya existe!')

        except Exception as ee:
            print('Se presentó un problema con la creación del usuario!')
            print(ee)

    @click.command(name="eliminar_usuario")
    @with_appcontext
    @click.argument("email", nargs=1)
    def eliminar_usuario(email):
        user = User.query.filter_by(email=email).first()
        user_datastore.delete_user(user)
        db.session.commit()

    @click.command(name="agregar_roles_usuario")
    @with_appcontext
    @click.argument("email", nargs=1)
    @click.argument("roles", nargs=-1)
    def agregar_roles_usuario(email, roles):
        user = User.query.filter_by(email=email).first()
        if (user):
            for role in roles:
                click.echo(f"role {role} fue agregado al usuario")
                r = Role.query.filter_by(name=role).first()
                user_datastore.add_role_to_user(user, r)

            db.session.commit()
        else:
            print('usuario no existe!')

    @click.command(name="remover_roles_usuario")
    @with_appcontext
    @click.argument("email", nargs=1)
    @click.argument("roles", nargs=-1)
    def remover_roles_usuario(email, roles):
        user = User.query.filter_by(email=email).first()
        if (user):
            for role in roles:
                click.echo(f"role {role} fue removido del usuario")
                r = Role.query.filter_by(name=role).first()
                user_datastore.remove_role_from_user(user, r)

            db.session.commit()
        else:
            print('usuario no existe!')
            
            
    @click.command(name="migrate_data_to_neo4j")
    @with_appcontext
    def migrate_data_to_neo4j():
       return  mysql_to_neo4j_ETL()

    # CLI User/Role management
    app.cli.add_command(crear_usuario)
    app.cli.add_command(eliminar_usuario)
    app.cli.add_command(agregar_roles_usuario)
    app.cli.add_command(remover_roles_usuario)
    
    app.cli.add_command(migrate_data_to_neo4j)

    return app
