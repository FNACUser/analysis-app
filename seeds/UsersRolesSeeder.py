from flask_security.utils import hash_password
from flask_seeder import Seeder

from defaultapp import db, user_datastore
from defaultapp.models import User
from defaultapp.bkhapps.common.Utilities import generate_random_string

# All seeders inherit from Seeder
class UsersRolesSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    # run() will be called by Flask-Seeder
    def run(self):
        # Creates 2 main roles Admin y Encuestado

        admin = user_datastore.create_role(name='admin')
        encuestado = user_datastore.create_role(name='encuestado')

        all_users = User.query.all()

        for registered_user in all_users:
            user_datastore.add_role_to_user(registered_user, encuestado)

        #random_pwd = generate_random_string()
        random_pwd = '12345'
        # Creates my user Humberto y LG  as admin and encuestado
        user1 = user_datastore.create_user(username='Humberto Zuluaga', email='hzuluaga@gmail.com',
                                           documentID='153528',
                                           password=hash_password(random_pwd))
        db.session.add(user1)

        user2 = user_datastore.create_user(username='Luis Gabriel', email='luis.caro@finac.com',
                                           documentID='19270627',
                                           password=hash_password(random_pwd))

        db.session.add(user2)

        user_datastore.add_role_to_user(user1, admin)
        user_datastore.add_role_to_user(user2, admin)
        # user_datastore.add_role_to_user(user1,encuestado)

        db.session.commit()
