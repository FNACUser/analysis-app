from os import abort

from bokeh.embed import server_session
from bokeh.util.token import generate_session_id
from flask import (render_template, Blueprint, current_app)
from flask_login import login_required, current_user
import logging

bkhapps = Blueprint('bkhapps', __name__)
logger = logging.getLogger(__name__)


@bkhapps.route("/bokeh/ActorActor", methods=['GET'])
@login_required
def ActorActor():
    
    logged_user = {'id': current_user.id,
                   'name': current_user.username,
                   'main_role': current_user.roles[0].name
                   }

    script = server_session(url=current_app.config['BOKEH_URL'] + ':' + current_app.config['BOKEH_PORT'] + '/ActorActor',
                            headers={'logged_user': logged_user},
                            session_id=generate_session_id(secret_key=current_app.config['BOKEH_SECRET_KEY'],
                                                           signed=current_app.config['BOKEH_SIGN_SESSIONS']))
    return render_template("embed.html", script=script, title="Actor Actor", template="index")

@bkhapps.route("/bokeh/ActorKnowledge", methods=['GET'])
@login_required
def ActorKnowledge():
    
    logged_user = {'id': current_user.id,
                   'name': current_user.username,
                   'main_role': current_user.roles[0].name
                   }

    script = server_session(url=current_app.config['BOKEH_URL'] + ':' + current_app.config['BOKEH_PORT'] + '/ActorKnowledge',
                            headers={'logged_user': logged_user},
                            session_id=generate_session_id(secret_key=current_app.config['BOKEH_SECRET_KEY'],
                                                           signed=current_app.config['BOKEH_SIGN_SESSIONS']))
    return render_template("embed.html", script=script, title="Actor Conocimiento", template="index")

@bkhapps.route("/bokeh/Values", methods=['GET'])
@login_required
def Values():
    
    logged_user = {'id': current_user.id,
                   'name': current_user.username,
                   'main_role': current_user.roles[0].name
                   }

    script = server_session(url=current_app.config['BOKEH_URL'] + ':' + current_app.config['BOKEH_PORT'] + '/Values',
                            headers={'logged_user': logged_user},
                            session_id=generate_session_id(secret_key=current_app.config['BOKEH_SECRET_KEY'],
                                                           signed=current_app.config['BOKEH_SIGN_SESSIONS']))
    return render_template("embed.html", script=script, title="Valores", template="index")