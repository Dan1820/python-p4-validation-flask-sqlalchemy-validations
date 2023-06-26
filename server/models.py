from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, sessionmaker
db = SQLAlchemy()

connection_string = "sqlite:///database.db"   # for SQLite, local file
db = create_engine(connection_string)
base = declarative_base()


class EmailAddress(db.Model):
    __tablename__ = 'emailaddress'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    backup_email = db.Column(db.String)

    @validates('email', 'backup_email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Failed simple email validation")
        return address


Session = sessionmaker(db)
session = Session()
base.metadata.create_all(db)


email = EmailAddress(email='banana')
session.add(email)

try:
    session.commit()
except SQLAlchemy.exc.IntegrityErr as e:
    print("Integrity Violation blocked")
    session.rollback()
