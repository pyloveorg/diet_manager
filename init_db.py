#
# from sqlalchemy import create_engine
# from main import db, bcrypt
# import models
#
#
# def db_start():
#     create_engine('sqlite:///test.db', convert_unicode=True)
#     db.create_all()
#     db.session.commit()
#     user = models.User()
#     user.name = "krystyna"
#     user.email = 'mariquita1@wp.pl'
#     user.set_password('superhaslo')
#     user.weight = 50
#     user.height = 150
#     user.admin = True
#     db.session.add(user)
#     db.session.commit()
#
#
# if __name__ == '__main__':
#     db_start()
