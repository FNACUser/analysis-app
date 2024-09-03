from datetime import datetime
from flask import current_app
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json

db = SQLAlchemy()
ma = Marshmallow()

########################################################################################################################################################################
#                               SQLAlchemy Models
########################################################################################################################################################################


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('users.id',ondelete='CASCADE')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    documentID = db.Column(db.String(50), unique=True, nullable=True)
    id_redmine = db.Column(db.String(100), nullable=True)
    active = db.Column(db.Boolean)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True,passive_deletes=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    confirmed_at = db.Column(db.DateTime)

    id_organization_area = db.Column(db.Integer,
                                     db.ForeignKey(
                                         'IRA_Organization_areas.id_organization_area'),
                                     nullable=True)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic',passive_deletes=True))

    adjacency_forms = db.relationship(
        'IRA_Adjacency_input_form', backref=db.backref('users', lazy=True,passive_deletes=True))

    culture_input_forms = db.relationship(
        'CVF_Culture_input_form', backref=db.backref('users', lazy=True,passive_deletes=True))

    nodes = db.relationship(
        'IRA_Nodes', backref=db.backref('users', lazy=True,passive_deletes=True))

    # narratives = db.relationship(
    #     'IRA_Narratives', backref=db.backref('users', lazy=True))

    school_roles = db.relationship(
        "DW_UsersSchoolRolesPivot", back_populates="user")
    grades_sections_subjects = db.relationship(
        "DW_UsersGradesSectionsSubjectsPivot", back_populates="user")

    # interacting_persons = db.relationship('IRA_Employees_interactions', backref=db.backref('users', lazy=True))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def has_role(self, role):
        return role in self.roles

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.documentID}')"


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

    def toJson(self):
        return json.dumps({'role': self.name}).decode('utf-8')


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


questions_vs_networks_modes = \
    db.Table('questions_vs_networks_modes',
             db.Column('id_question', db.Integer,
                       db.ForeignKey('IRA_Questions.id_question')),
             db.Column('id_network_mode', db.Integer,
                       db.ForeignKey('IRA_Networks_modes.id_network_mode')))

cycles_vs_networks_modes = \
    db.Table('cycles_vs_networks_modes',
             db.Column('id_cycle', db.Integer,
                       db.ForeignKey('IRA_Cycles.id_cycle')),
             db.Column('id_network_mode', db.Integer,
                       db.ForeignKey('IRA_Networks_modes.id_network_mode')))


nodes_vs_networks_modes = \
    db.Table('nodes_vs_networks_modes',
             db.Column('id_node', db.Integer,
                       db.ForeignKey('IRA_Nodes.id_node')),
             db.Column('id_network_mode', db.Integer,
                       db.ForeignKey('IRA_Networks_modes.id_network_mode')))


# -----------------------------------------------------------------------------------------------------------
# IRA models
# -----------------------------------------------------------------------------------------------------------

class IRA_Adjacency_input_form(db.Model):
    __tablename__ = 'IRA_Adjacency_input_form'
    id_adjacency_input_form = db.Column(db.String(15), primary_key=True)
    id_employee = db.Column(db.Integer,
                            db.ForeignKey('users.id',ondelete='CASCADE'),
                            nullable=False)
    id_cycle = db.Column(db.Integer,
                         db.ForeignKey('IRA_Cycles.id_cycle'),
                         nullable=False)

    id_network_mode = \
        db.Column(db.Integer,
                  db.ForeignKey('IRA_Networks_modes.id_network_mode'),
                  nullable=False)

    Is_concluded = db.Column(db.Boolean, nullable=False)

    responses = db.relationship('IRA_Responses',
                                backref=db.backref('adjacency_input_form',
                                                   lazy=True))

    db.UniqueConstraint('id_employee', 'id_cycle', 'id_network_mode',
                        name='uix_1')

    def __repr__(self):
        return f"IRA_Adjacency_input_form('{self.id_adjacency_input_form}'," \
               f"'{self.id_employee}','{self.id_cycle}','{self.id_network_mode}'," \
               f"'{self.Is_concluded}')"


class IRA_Cycles(db.Model):
    __tablename__ = 'IRA_Cycles'
    id_cycle = db.Column(db.Integer, primary_key=True)
    Cycle_es = db.Column(db.String(100), nullable=False)
    Cycle_en = db.Column(db.String(100), nullable=False)
    Initial_date = db.Column(db.DateTime, nullable=False)
    End_date = db.Column(db.DateTime, nullable=False)
    Is_active = db.Column(db.Boolean, nullable=False)

    networks_modes = db.relationship('IRA_Networks_modes',
                                     secondary=cycles_vs_networks_modes,
                                     backref=db.backref('cycles',
                                                        lazy='dynamic'))

    adjacency_forms = db.relationship('IRA_Adjacency_input_form',
                                      backref=db.backref('cycle', lazy=True))

    culture_input_forms = db.relationship('CVF_Culture_input_form',
                                          backref=db.backref('cycle', lazy=True))

    # responses=db.relationship('IRA_Responses',
    #                             backref=db.backref('cycle',lazy=True))

    def __repr__(self):
        return f"IRA_Cycles('{self.id_cycle}', '{self.Cycle_es}','{self.Cycle_en}'" \
               f"'{self.Initial_date}','{self.End_date}','{self.Is_active}')"


class IRA_Employees_interactions(db.Model):
    __tablename__ = 'IRA_Employees_interactions'
    __table_args__ = (
        db.UniqueConstraint('id_cycle', 'id_responding_employee',
                            'id_interacting_employee', name='unique_cycle_responding_interacting'),
    )

    id_employee_interaction = db.Column(db.Integer, primary_key=True)

    id_cycle = db.Column(db.Integer,
                         db.ForeignKey('IRA_Cycles.id_cycle'),
                         nullable=True)
    id_responding_employee = \
        db.Column(db.Integer,
                  db.ForeignKey('users.id',ondelete='CASCADE'),
                  nullable=True)
    id_interacting_employee = \
        db.Column(db.Integer,
                  db.ForeignKey('users.id',ondelete='CASCADE'),
                  nullable=True)

    def __repr__(self):
        return f"IRA_Employees_interactions('{self.id_employee_interaction}'," \
               f"'{self.id_cycle}','{self.id_responding_employee}'," \
               f"'{self.id_interacting_employee}')"


class IRA_Networks(db.Model):
    __tablename__ = 'IRA_Networks'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    form_type = db.Column(db.String(50), nullable=False)

    networks_modes = db.relationship('IRA_Networks_modes',
                                     backref=db.backref('network', lazy=True))

    def __repr__(self):
        return f"IRA_Networks('{self.code}')"


class IRA_Networks_modes(db.Model):
    __tablename__ = 'IRA_Networks_modes'
    id_network_mode = db.Column(db.Integer, primary_key=True)
    id_network = db.Column(db.Integer,
                           db.ForeignKey(
                               'IRA_Networks.id'),
                           nullable=False)
    # id_node_segment_category = \
    #     db.Column(db.Integer,
    #               db.ForeignKey(
    #                   'IRA_Nodes_segments_categories.id_node_segment_category'),
    #               nullable=True)
    
    id_node_segment = \
        db.Column(db.Integer,
                  db.ForeignKey(
                      'IRA_Nodes_segments.id_node_segment'),
                  nullable=True)

    id_network_mode_theme = \
        db.Column(db.Integer,
                  db.ForeignKey(
                      'IRA_Networks_modes_themes.id_network_mode_theme'),
                  nullable=True)

    adjacency_forms = db.relationship('IRA_Adjacency_input_form',
                                      backref=db.backref('network_mode', lazy=True))

    # responses=db.relationship('IRA_Responses',
    #                             backref=db.backref('network_mode',lazy=True))

    def __repr__(self):
        return f"IRA_Networks_modes('{self.id_network_mode}','{self.id_node_segment_category}','{self.id_network_mode_theme}')"


class IRA_Networks_modes_themes(db.Model):
    __tablename__ = 'IRA_Networks_modes_themes'
    id_network_mode_theme = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    Network_mode_theme_es = db.Column(db.String(100), nullable=False)
    Network_mode_theme_en = db.Column(db.String(100), nullable=False)

    network_modes = db.relationship('IRA_Networks_modes',
                                    backref=db.backref('network_mode_theme', lazy=True))

    def __repr__(self):
        return f"IRA_Networks_modes_themes('{self.id_network_mode_theme}', \
            '{self.code}')"

class IRA_Narrative_topics(db.Model):
    __tablename__ = 'IRA_Narrative_topics'
    id = db.Column(db.Integer, primary_key=True)
    topic_es = db.Column(db.Text, nullable=False)
    topic_en = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return f"IRA_Narrative_topics('{self.id}', ' {self.topic_es}')"


class IRA_Narratives(db.Model):
    __tablename__ = 'IRA_Narratives'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    narrative = db.Column(db.Text, nullable=False)
    
    id_topic = db.Column(db.Integer,
                            db.ForeignKey('IRA_Narrative_topics.id'),
                            nullable=False)
    
    id_employee = db.Column(db.Integer,
                            db.ForeignKey('users.id',ondelete='CASCADE'),
                            nullable=False)
    id_cycle = db.Column(db.Integer,
                         db.ForeignKey('IRA_Cycles.id_cycle'),
                         nullable=False)

    def __repr__(self):
        return f"IRA_Narratives('{self.id}', ' {self.title}','{self.id_employee}','{self.id_cycle}')"


class IRA_Nodes(db.Model):
    __tablename__ = 'IRA_Nodes'
    id_node = db.Column(db.Integer, primary_key=True)
    Node_es = db.Column(db.String(300), nullable=False)
    Node_en = db.Column(db.String(300), nullable=False)
    theme_es = db.Column(db.String(100), nullable=True)
    theme_en = db.Column(db.String(100), nullable=True)
    origin_es = db.Column(db.String(100), nullable=True)
    origin_en = db.Column(db.String(100), nullable=True)
    
    id_node_segment = db.Column(db.Integer,
                                db.ForeignKey(
                                    'IRA_Nodes_segments.id_node_segment'),
                                nullable=False)
    id_employee = db.Column(db.Integer,
                            db.ForeignKey('users.id',ondelete='CASCADE'),
                            nullable=True)

    networks_modes = db.relationship('IRA_Networks_modes',
                                     secondary=nodes_vs_networks_modes,
                                     backref=db.backref('nodes',
                                                        lazy='dynamic'))

    def __repr__(self):
        return f"IRA_Nodes('{self.id_node}', '{self.Node_es}','{self.id_node_segment}','{self.id_employee}')"


class IRA_Nodes_segments(db.Model):
    __tablename__ = 'IRA_Nodes_segments'
    id_node_segment = db.Column(db.Integer, primary_key=True)
    Node_segment = db.Column(db.String(100), nullable=False)
    id_node_segment_category = \
        db.Column(db.Integer,
                  db.ForeignKey(
                      'IRA_Nodes_segments_categories.id_node_segment_category'), nullable=False)

    nodes = db.relationship(
        'IRA_Nodes', backref=db.backref('node_segment', lazy=True))
    
    networks_modes = db.relationship('IRA_Networks_modes',
                                     backref=db.backref('node_segment', lazy=True))

    def __repr__(self):
        return f"IRA_Nodes_segments('{self.id_node_segment}', \
            '{self.Node_segment}','{self.id_node_segment_category}')"


class IRA_Nodes_segments_categories(db.Model):
    __tablename__ = 'IRA_Nodes_segments_categories'
    id_node_segment_category = db.Column(db.Integer, primary_key=True)
    Node_segment_category = db.Column(db.String(100), nullable=False)

    nodes_segments = db.relationship('IRA_Nodes_segments',
                                     backref=db.backref('node_segment_category', lazy=True))

    # networks_modes = db.relationship('IRA_Networks_modes',
    #                                  backref=db.backref('node_segment_category', lazy=True))

    def __repr__(self):
        return f"IRA_Nodes_segments_categories('{self.id_node_segment_category}', \
            '{self.Node_segment_category}')"


class IRA_Organization_areas(db.Model):
    __tablename__ = 'IRA_Organization_areas'
    id_organization_area = db.Column(db.Integer, primary_key=True)
    Organization_area_es = db.Column(db.String(100), nullable=False)
    Organization_area_en = db.Column(db.String(100), nullable=False)

    employees = db.relationship(
        'User', backref=db.backref('organization_area', lazy=True))

    def __repr__(self):
        return f"IRA_Organization_area('{self.id_organization_area}'," \
               f"'{self.Organization_area_es}')"


class IRA_Questions(db.Model):
    __tablename__ = 'IRA_Questions'
    id_question = db.Column(db.Integer, primary_key=True)
    # Question_es = db.Column(db.String(250), nullable=False)
    # Question_en = db.Column(db.String(250), nullable=False)
    Question_es = db.Column(db.Text, nullable=False)
    Question_en = db.Column(db.Text, nullable=False)
    short_question_es = db.Column(db.String(200), nullable=True)
    short_question_en = db.Column(db.String(200), nullable=True)
    help_es = db.Column(db.Text, nullable=True)
    help_en = db.Column(db.Text, nullable=True)
    acronym_es = db.Column(db.String(10), nullable=True)
    acronym_en = db.Column(db.String(10), nullable=True)
    
    
    id_question_possible_answers = \
        db.Column(db.Integer,
                  db.ForeignKey(
                      'IRA_Questions_possible_answers.id_question_possible_answers'),
                  nullable=True)

    networks_modes = db.relationship('IRA_Networks_modes',
                                     secondary=questions_vs_networks_modes,
                                     backref=db.backref('questions',
                                                        lazy='dynamic'))

    responses = db.relationship('IRA_Responses',
                                backref=db.backref('question', lazy=True))

    def __repr__(self):
        return f"IRA_Questions('{self.id_question}'," \
               f"'{self.Question}','{self.id_question_possible_answers}')"


class IRA_Questions_possible_answers(db.Model):
    __tablename__ = 'IRA_Questions_possible_answers'
    id_question_possible_answers = db.Column(db.Integer, primary_key=True)
    Question_possible_answers_es = db.Column(db.Text, nullable=False)
    Question_possible_answers_en = db.Column(db.Text, nullable=False)
    multiple = db.Column(db.Boolean, default=False)
    use_external_source = db.Column(db.Boolean, nullable=True)
    source_name = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(200), nullable=True)
    max_selections = db.Column(db.Integer, nullable=True)
    

    questions = db.relationship('IRA_Questions',
                                backref=db.backref('question_possible_answers',
                                                   lazy=True))

    def __repr__(self):
        return f"IRA_Questions_possible_answers('{self.id_question_possible_answers}'," \
               f"'{self.Question_possible_answers}')"


class IRA_Responses(db.Model):
    __tablename__ = 'IRA_Responses'
    id_response = db.Column(db.Integer, primary_key=True)
    Response = db.Column(db.JSON, nullable=True)
    id_question = db.Column(db.Integer,
                            db.ForeignKey('IRA_Questions.id_question'),
                            nullable=False)
    id_adjacency_input_form = \
        db.Column(db.String(15),
                  db.ForeignKey(
                      'IRA_Adjacency_input_form.id_adjacency_input_form'),
                  nullable=True)

    def __repr__(self):
        return f"IRA_Responses('{self.id_response}','{self.Response}'," \
               f"'{self.id_question}','{self.id_adjacency_input_form}')"

# -----------------------------------------------------------------------------------------------------------
# CVF CULTURE models
# -----------------------------------------------------------------------------------------------------------


class CVF_Culture_input_form(db.Model):
    __tablename__ = 'CVF_Culture_input_form'
    id = db.Column(db.Integer, primary_key=True)
    # id_culture_input_form = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employee = db.Column(db.Integer,
                            db.ForeignKey('users.id',ondelete='CASCADE'),
                            nullable=False)
    id_cycle = db.Column(db.Integer,
                         db.ForeignKey('IRA_Cycles.id_cycle'),
                         nullable=False)

    Is_concluded = db.Column(db.Boolean, nullable=False)

    id_culture_mode = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_modes.id'),
                  nullable=False)

    db.UniqueConstraint('id_employee', 'id_cycle', 'id_culture_mode',
                        name='uix_1')

    themes_responses = db.relationship('CVF_Themes_responses',
                                       backref=db.backref('culture_input_form',
                                                          lazy=True))

    def __repr__(self):
        return f"CVF_Culture_input_form('{self.id}'," \
               f"'{self.id_employee}','{self.id_cycle}','{self.id_culture_mode}'," \
               f"'{self.Is_concluded}')"


class CVF_Culture_modes(db.Model):
    __tablename__ = 'CVF_Culture_modes'
    id = db.Column(db.Integer, primary_key=True)
    Culture_mode_es = db.Column(db.String(100), nullable=False)
    Culture_mode_en = db.Column(db.String(100), nullable=False)

    culture_modes_themes = db.relationship('CVF_Culture_modes_themes',
                                           backref=db.backref('culture_mode',
                                                              lazy=True))

    # culture_input_forms = db.relationship('CVF_Culture_input_form',
    #                                       backref=db.backref('culture_mode', lazy=True))

    def __repr__(self):
        return f"CVF_Culture_modes('{self.id}', \
            '{self.Culture_mode_es}')"


class CVF_Culture_modes_themes(db.Model):
    __tablename__ = 'CVF_Culture_modes_themes'
    id = db.Column(db.Integer, primary_key=True)
    Culture_mode_theme_es = db.Column(db.String(255), nullable=False)
    Culture_mode_theme_en = db.Column(db.String(255), nullable=False)
    Questions_prefix_es = db.Column(db.String(255), nullable=False)
    Questions_prefix_en = db.Column(db.String(255), nullable=False)

    id_culture_mode = db.Column(db.Integer,
                                db.ForeignKey('CVF_Culture_modes.id'),
                                nullable=False)

    culture_mode_theme_questions = \
        db.relationship('CVF_Culture_modes_themes_questions',
                        backref=db.backref('culture_mode_theme', lazy=True))

    themes_responses = db.relationship('CVF_Themes_responses',
                                       backref=db.backref('culture_mode_theme',
                                                          lazy=True))

    def __repr__(self):
        return f"CVF_Culture_modes_themes('{self.id}', \
            '{self.Culture_mode_theme_es}','{self.id_culture_mode}')"


class CVF_Culture_modes_themes_questions(db.Model):
    __tablename__ = 'CVF_Culture_modes_themes_questions'
    id = db.Column(db.Integer, primary_key=True)
    Culture_mode_theme_question_es = db.Column(db.Text, nullable=False)
    Culture_mode_theme_question_en = db.Column(db.Text, nullable=False)

    id_culture_mode_theme = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_modes_themes.id'),
                  nullable=False)

    id_culture_quadrant = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_quadrants.id'),
                  nullable=False)

    questions_responses = \
        db.relationship('CVF_Questions_responses',
                        backref=db.backref('modes_themes_question', lazy=True))

    def __repr__(self):
        return f"CVF_Culture_modes_themes_questions('" \
               f"'{self.id}'," \
               f"'{self.Culture_mode_theme_question_es}'," \
               f"'{self.id_culture_mode_theme}'," \
               f"'{self.id_culture_quadrant}')"


class CVF_Culture_quadrants(db.Model):
    __tablename__ = 'CVF_Culture_quadrants'
    id = db.Column(db.Integer, primary_key=True)
    Culture_quadrant_es = db.Column(db.String(100), nullable=False)
    Culture_quadrant_en = db.Column(db.String(100), nullable=False)

    culture_modes_themes_questions = \
        db.relationship('CVF_Culture_modes_themes_questions',
                        backref=db.backref('culture_quadrant',
                                           lazy=True))

    def __repr__(self):
        return f"CVF_Culture_quadrants('{self.id}', \
            '{self.Culture_quadrant_es}')"


class CVF_Questions_responses(db.Model):
    __tablename__ = 'CVF_Questions_responses'
    id = db.Column(db.Integer, primary_key=True)
    Actual = db.Column(db.Integer, nullable=False)
    Preferred = db.Column(db.Integer, nullable=False)

    id_theme_responses = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Themes_responses.id'),
                  nullable=False)

    id_culture_mode_theme_question = db.Column(db.Integer,
                                               db.ForeignKey(
                                                   'CVF_Culture_modes_themes_questions.id'),
                                               nullable=False)

    def __repr__(self):
        return f"CVF_Questions_responses('{self.id}'," \
               f"'{self.id_theme_responses}','{self.id_culture_mode_theme_question}'," \
               f"'{self.Actual}','{self.Preferred}')"


class CVF_Themes_responses(db.Model):
    __tablename__ = 'CVF_Themes_responses'
    id = db.Column(db.Integer, primary_key=True)

    id_culture_input_form = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_input_form.id'),
                  nullable=False)

    id_culture_mode_theme = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_modes_themes.id'),
                  nullable=False)

    Is_concluded = db.Column(db.Boolean, nullable=False)

    Total_actual = db.Column(db.Integer, nullable=False)

    Total_preferred = db.Column(db.Integer, nullable=False)

    questions_responses = \
        db.relationship('CVF_Questions_responses',
                        backref=db.backref('theme_responses', lazy=True))

    def __repr__(self):
        return f"CVF_Themes_responses('{self.id}'," \
               f"'{self.id_culture_input_form}','{self.id_culture_mode_theme}'," \
               f"'{self.Is_concluded}','{self.Total_actual}'," \
               f"'{self.Total_preferred}')"


####################################################################################################
#                              School DataWise Models
####################################################################################################

# grades_vs_subjects = db.Table('DW_grades_vs_subjects',\
#     db.Column('grade_id', db.Integer,db.ForeignKey('DW_Grades.id')),\
#     db.Column('subject_id', db.Integer,db.ForeignKey('DW_Subjects.id')))

class DW_Roles(db.Model):
    __tablename__ = 'DW_Roles'

    id = db.Column(db.Integer, primary_key=True)
    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)

    users = db.relationship("DW_UsersSchoolRolesPivot",
                            back_populates="school_role")
    tools = db.relationship("DW_ToolsRolesPivot", back_populates="role")

    def __repr__(self):
        return f"DW_Roles('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


class DW_ServiceUnits(db.Model):
    __tablename__ = 'DW_ServiceUnits'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=True)

    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)

    # users_schoolroles_pivot = db.relationship('DW_UsersSchoolRolesPivot',backref=db.backref('service_unit',lazy=True))

    def __repr__(self):
        return f"DW_ServiceUnits('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


class DW_Schools(db.Model):
    __tablename__ = 'DW_Schools'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=True)

    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)

    grades = db.relationship(
        'DW_Grades', backref=db.backref('school', lazy=True))
    # users_schoolroles_pivot = db.relationship('DW_UsersSchoolRolesPivot',backref=db.backref('school',lazy=True))

    def __repr__(self):
        return f"DW_Schools('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


class DW_Areas(db.Model):
    __tablename__ = 'DW_Areas'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=True)

    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)

    subjects = db.relationship(
        'DW_Subjects', backref=db.backref('area', lazy=True))
    tools = db.relationship("DW_ToolsAreasPivot", back_populates="area")
    # users_schoolroles_pivot = db.relationship('DW_UsersSchoolRolesPivot',backref=db.backref('area',lazy=True))

    def __repr__(self):
        return f"DW_Areas('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


class DW_Topics(db.Model):
    __tablename__ = 'DW_Topics'

    id = db.Column(db.Integer, primary_key=True)
    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)

    tools = db.relationship('DW_Tools', backref=db.backref('topic', lazy=True))

    def __repr__(self):
        return f"DW_Topics('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


class DW_Grades(db.Model):
    __tablename__ = 'DW_Grades'

    id = db.Column(db.Integer, primary_key=True)
    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)

    school_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Schools.id'), nullable=False)

    # sections = db.relationship('DW_Sections',backref=db.backref('grade',lazy=True))
    # subjects = db.relationship('DW_Subjects',
    #                                  secondary=grades_vs_subjects,
    #                                  backref=db.backref('grades',
    #                                                     lazy='dynamic'))

    subjects = db.relationship(
        "DW_GradesSubjectsPivot", back_populates="grade")
    sections = db.relationship(
        "DW_GradesSectionsPivot", back_populates="grade")
    tools = db.relationship("DW_ToolsGradesPivot", back_populates="grade")

    users_sections_subjects = db.relationship(
        "DW_UsersGradesSectionsSubjectsPivot", back_populates="grade")
    # users_schoolroles_pivot = db.relationship('DW_UsersSchoolRolesPivot',backref=db.backref('grade',lazy=True))

    def __repr__(self):
        return f"DW_Grades('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


class DW_Sections(db.Model):
    __tablename__ = 'DW_Sections'

    id = db.Column(db.Integer, primary_key=True)
    # code = db.Column(db.String(20), nullable=True)

    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    # grade_id = db.Column(db.Integer,db.ForeignKey('DW_Grades.id'),nullable=False)
    # users_schoolroles_pivot = db.relationship('DW_UsersSchoolRolesPivot',backref=db.backref('section',lazy=True))
    grades = db.relationship("DW_GradesSectionsPivot",
                             back_populates="section")
    users_grades_subjects = db.relationship(
        "DW_UsersGradesSectionsSubjectsPivot", back_populates="section")

    def __repr__(self):
        return f"DW_Sections('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


class DW_Subjects(db.Model):
    __tablename__ = 'DW_Subjects'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=True)

    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Areas.id'), nullable=False)

    # users_schoolroles_pivot = db.relationship('DW_UsersSchoolRolesPivot',backref=db.backref('subject',lazy=True))

    grades = db.relationship("DW_GradesSubjectsPivot",
                             back_populates="subject")
    users_grades_sections = db.relationship(
        "DW_UsersGradesSectionsSubjectsPivot", back_populates="subject")

    def __repr__(self):
        return f"DW_Subjects('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


tools_vs_options = db.Table('DW_tools_vs_options',
                            db.Column('tool_id', db.Integer,
                                      db.ForeignKey('DW_Tools.id')),
                            db.Column('option_id', db.Integer, db.ForeignKey('DW_Options.id')))


class DW_Tools(db.Model):
    __tablename__ = 'DW_Tools'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=True)

    name_es = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_es = db.Column(db.String(400), nullable=True)
    description_en = db.Column(db.String(400), nullable=True)

    topic_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Topics.id'), nullable=False)

    grades = db.relationship("DW_ToolsGradesPivot", back_populates="tool")
    roles = db.relationship("DW_ToolsRolesPivot", back_populates="tool")
    areas = db.relationship("DW_ToolsAreasPivot", back_populates="tool")

    # options = db.relationship("DW_ToolsOptionsPivot", back_populates="tool")
    options = db.relationship(
        'DW_Options', secondary=tools_vs_options, backref=db.backref('tools', lazy='dynamic'))

    def __repr__(self):
        return f"DW_Tools('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


class DW_Options(db.Model):
    __tablename__ = 'DW_Options'

    id = db.Column(db.Integer, primary_key=True)
    name_es = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)

    # tools = db.relationship("DW_ToolsOptionsPivot", back_populates="option")

    def toJson(self):
        return json.dumps({'id': self.id,
                           'name_es': self.name_es,
                           'name_en': self.name_en,
                           }).decode('utf-8')

    def __repr__(self):
        return f"DW_Options('{self.id}'," \
               f"'{self.name_es}','{self.name_en}')"


class DW_UsersSchoolRolesPivot(db.Model):
    __tablename__ = 'DW_users_schoolroles'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id',ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Roles.id'), primary_key=True)

    areas = db.Column(db.String(100), nullable=True)
    schools = db.Column(db.String(100), nullable=True)

    user = db.relationship("User", back_populates="school_roles")
    school_role = db.relationship("DW_Roles", back_populates="users")


class DW_UsersGradesSectionsSubjectsPivot(db.Model):
    __tablename__ = 'DW_users_grades_sections_subjects'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id',ondelete='CASCADE'), primary_key=True)
    grade_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Grades.id'), primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Sections.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Subjects.id'), primary_key=True)

    user = db.relationship("User", back_populates="grades_sections_subjects")
    grade = db.relationship(
        "DW_Grades", back_populates="users_sections_subjects")
    section = db.relationship(
        "DW_Sections", back_populates="users_grades_subjects")
    subject = db.relationship(
        "DW_Subjects", back_populates="users_grades_sections")


class DW_ToolsGradesPivot(db.Model):
    __tablename__ = 'DW_tools_grades'

    tool_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Tools.id'), primary_key=True)
    grade_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Grades.id'), primary_key=True)

    tool = db.relationship("DW_Tools", back_populates="grades")
    grade = db.relationship("DW_Grades", back_populates="tools")


class DW_ToolsAreasPivot(db.Model):
    __tablename__ = 'DW_tools_areas'

    tool_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Tools.id'), primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Areas.id'), primary_key=True)

    tool = db.relationship("DW_Tools", back_populates="areas")
    area = db.relationship("DW_Areas", back_populates="tools")


class DW_ToolsRolesPivot(db.Model):
    __tablename__ = 'DW_tools_roles'

    tool_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Tools.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Roles.id'), primary_key=True)

    tool = db.relationship("DW_Tools", back_populates="roles")
    role = db.relationship("DW_Roles", back_populates="tools")


class DW_GradesSectionsPivot(db.Model):
    __tablename__ = 'DW_grades_sections'

    grade_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Grades.id'), primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Sections.id'), primary_key=True)
    code = db.Column(db.String(20), nullable=True)

    grade = db.relationship("DW_Grades", back_populates="sections")
    section = db.relationship("DW_Sections", back_populates="grades")


class DW_GradesSubjectsPivot(db.Model):
    __tablename__ = 'DW_grades_subjects'

    grade_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Grades.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey(
        'DW_Subjects.id'), primary_key=True)

    grade = db.relationship("DW_Grades", back_populates="subjects")
    subject = db.relationship("DW_Subjects", back_populates="grades")


# class DW_ToolsOptionsPivot(db.Model):
#     __tablename__ = 'DW_tools_options'

#     tool_id = db.Column(db.Integer, db.ForeignKey('DW_Tools.id'), primary_key=True)
#     option_id = db.Column(db.Integer,db.ForeignKey('DW_Options.id'),primary_key=True)

#     tool = db.relationship("DW_Tools", back_populates="options")
#     option = db.relationship("DW_Options", back_populates="tools")


####################################################################################################
#                               Marshmallow Schemas
####################################################################################################

class AreaSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Organization_areas
        # fields = ("id_organization_area", "Organization_area")


areas_schema = AreaSchema(many=True)


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        fields = ("id", "name")


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post


class ResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IRA_Responses


class NarrativeTopicsSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Narrative_topics

narrative_topics_schema = NarrativeTopicsSchema(many=True)


class NarrativeSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Narratives
        fields = ("id", "title", "narrative", "id_topic")


narrative_schema = NarrativeSchema()
narratives_schema = NarrativeSchema(many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id", "username", "email", "id_redmine", "roles",
                  "id_organization_area", "organization_area")

    organization_area = ma.Nested(AreaSchema)
    # posts = ma.List(ma.Nested(PostSchema))
    roles = ma.List(ma.Nested(RoleSchema))
    # narratives = ma.List(ma.Nested(NarrativeSchema))
    # adjacency_forms = ma.List(ma.Nested(AdjacencyFormSchema))
    # culture_input_forms = ma.List(ma.Nested(CultureFormSchema))


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# class CycleSchema(ma.SQLAlchemyAutoSchema):

#     class Meta:
#         model = IRA_Cycles

#         network_modes = ma.Nested(NetworksModesSchema)

# cycles_schema = CycleSchema(many=True)


class NetworkSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Networks
        # fields = ("id", "name_es","name")


networks_schema = NetworkSchema(many=True)

# class NetworkModeSchema(ma.SQLAlchemyAutoSchema):

#     class Meta:
#         model = IRA_Networks_modes
#         fields = ("id_network_mode", "id_network","id_node_segment_category","id_network_mode_theme")

# network_modes_schema = NetworkModeSchema(many=True)


class NetworkModeThemeSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Networks_modes_themes


network_mode_theme_schema = NetworkModeThemeSchema(many=True)


class NodeSegmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IRA_Nodes_segments


node_segment_schema = NodeSegmentSchema(many=True)


class NodeSegmentCategorySchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Nodes_segments_categories
        fields = ("id_node_segment_category", "Node_segment_category")


node_segment_category_schema = NodeSegmentCategorySchema(many=True)


class NodeSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Nodes
        fields = ("id_node", "Node_es", "Node_en","theme_es","theme_en","origin_es","origin_en",
                  "id_node_segment", "node_segment", "id_employee")

    node_segment = ma.Nested(NodeSegmentSchema)


nodes_schema = NodeSchema(many=True)


class QuestionsPossibleAnswersSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Questions_possible_answers
        # fields = ("id_question_possible_answers", "Question_possible_answers_es", "Question_possible_answers_en")


questions_possible_answers_schema = QuestionsPossibleAnswersSchema(many=True)


class QuestionsSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Questions
        fields = ("id_question", 
                  "Question_es", 
                  "Question_en",
                  "short_question_es", 
                  "short_question_en",
                  "help_es", 
                  "help_en",
                  "acronym_es", 
                  "acronym_en",
                  "id_question_possible_answers", "question_possible_answers")

    question_possible_answers = ma.Nested(QuestionsPossibleAnswersSchema)


questions_schema = QuestionsSchema(many=True)


class NetworkModeSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Networks_modes
        fields = ("id_network_mode", "id_network", "network", "id_node_segment",
                  "node_segment", "id_network_mode_theme", "network_mode_theme")

    network = ma.Nested(NetworkSchema)
    node_segment = ma.Nested(NodeSegmentSchema)
    network_mode_theme = ma.Nested(NetworkModeThemeSchema)


network_mode_schema = NetworkModeSchema(many=True)


class AdjacencyInputFormSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IRA_Adjacency_input_form
        fields = ("id_adjacency_input_form", "id_employee",
                  "id_cycle", "id_network_mode", "Is_concluded")

    # network_mode = ma.Nested(NetworkModeSchema)


adjacency_input_forms_schema = AdjacencyInputFormSchema(many=True)


class CycleSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Cycles
        # fields = ("id_cycle","Cycle_es","Cycle_en","Initial_date","End_date","Is_active","networks_modes")

        # network_modes = ma.Nested(NetworksModesSchema)


cycles_schema = CycleSchema(many=True)


class ResponseSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = IRA_Responses
        fields = ("id_response", "id_question",
                  "id_adjacency_input_form", "Response", "adjacency_input_form")

    adjacency_input_form = ma.Nested(AdjacencyInputFormSchema)


responses_schema = ResponseSchema(many=True)


# -----------------------------------------------------------------------------------------------------------
# Culture Schemas
# -----------------------------------------------------------------------------------------------------------

class QuestionResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Questions_responses


class ThemeResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Themes_responses

    questions_responses = ma.List(ma.Nested(QuestionResponseSchema))


class CultureInputFormSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Culture_input_form

    themes_responses = ma.List(ma.Nested(ThemeResponseSchema))


class CultureModeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Culture_modes


culture_mode_schema = CultureModeSchema(many=True)


class CultureQuadrantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Culture_quadrants


culture_quadrant_schema = CultureQuadrantSchema(many=True)


class CultureModeThemeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Culture_modes_themes
        # fields = ("id", "Culture_mode_theme_es", "Culture_mode_theme_en","Questions_prefix_es","Questions_prefix_en", "id_culture_mode")
        # fields = ("id", "Culture_mode_theme_es", "Culture_mode_theme_en","Questions_prefix_es","Questions_prefix_en", "id_culture_mode","culture_mode")

   # culture_mode = ma.Nested(CultureModeSchema)
culture_mode_theme_schema = CultureModeThemeSchema(many=True)


class CultureModeThemeQuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Culture_modes_themes_questions
        fields = ("id", "Culture_mode_theme_question_es",
                  "Culture_mode_theme_question_en", "id_culture_quadrant")
        # fields = ("id", "Culture_mode_theme_question_es", "Culture_mode_theme_question_en","id_culture_mode_theme","culture_mode_theme", "id_culture_quadrant","culture_quadrant")

    # culture_mode_theme = ma.Nested(CultureModeThemeSchema)
    # culture_quadrant = ma.Nested(CultureQuadrantSchema)


culture_mode_theme_question_schema = CultureModeThemeQuestionSchema(many=True)


class CultureThemeResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Themes_responses
        fields = ("id", "id_culture_input_form", "id_culture_mode_theme",
                  "Total_actual", "Total_preferred", "Is_concluded")
        # fields = ("id", "id_culture_input_form","culture_input_form", "id_culture_mode_theme","culture_mode_theme", "Total_actual","Total_preferred", "Is_concluded")

    # culture_input_form = ma.Nested(CultureInputFormSchema)
    # culture_mode_theme = ma.Nested(CultureModeThemeSchema)


culture_theme_response_schema = CultureThemeResponseSchema(many=True)


class CultureQuestionResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Questions_responses
        fields = ("id", "id_theme_responses",
                  "id_culture_mode_theme_question", "Actual", "Preferred")
        # fields = ("id", "id_theme_responses", "theme_responses", "id_culture_mode_theme_question","culture_mode_theme_question","Actual","Preferred")

    # theme_responses = ma.Nested(CultureThemeResponseSchema)
    # culture_mode_theme_question = ma.Nested(CultureModeThemeQuestionSchema)


culture_question_response_schema = CultureQuestionResponseSchema(many=True)


# -----------------------------------------------------------------------------------------------------------
# Datawise Schemas
# -----------------------------------------------------------------------------------------------------------

class DW_OptionsSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = DW_Options
        fields = ("id", "name_es", "name_en")


class DW_ToolsSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = DW_Tools
        fields = ("id", "name_es", "name_en", "topic_id", "code", "options")

    options = ma.List(ma.Nested(DW_OptionsSchema))


dw_tools_schema = DW_ToolsSchema(many=True)
