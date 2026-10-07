from datetime import datetime
from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey,Text,Index
from sqlalchemy.orm import relationship
from .database import Base
class Creator(Base):
 __tablename__='creators';id=Column(Integer,primary_key=True);name=Column(String(120),nullable=False);email=Column(String(255),nullable=False);created_at=Column(DateTime,default=datetime.utcnow);forms=relationship('Form',back_populates='creator',cascade='all, delete-orphan')
class Form(Base):
 __tablename__='forms';id=Column(Integer,primary_key=True);creator_id=Column(Integer,ForeignKey('creators.id'),nullable=False);title=Column(String(255),nullable=False);slug=Column(String(255),unique=True,nullable=False);description=Column(Text,default='');status=Column(String(20),default='draft');theme_json=Column(Text,default='{}');thank_you_json=Column(Text,default='{}');created_at=Column(DateTime,default=datetime.utcnow);updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow);published_at=Column(DateTime,nullable=True);creator=relationship('Creator',back_populates='forms');questions=relationship('Question',back_populates='form',cascade='all, delete-orphan',order_by='Question.position');responses=relationship('Response',back_populates='form',cascade='all, delete-orphan')
class Question(Base):
 __tablename__='questions';id=Column(Integer,primary_key=True);form_id=Column(Integer,ForeignKey('forms.id'),nullable=False);position=Column(Integer,nullable=False);type=Column(String(40),nullable=False);title=Column(String(500),nullable=False);description=Column(Text,default='');required=Column(Boolean,default=True);settings_json=Column(Text,default='{}');created_at=Column(DateTime,default=datetime.utcnow);updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow);form=relationship('Form',back_populates='questions');answers=relationship('Answer',back_populates='question')
class Response(Base):
 __tablename__='responses';id=Column(Integer,primary_key=True);form_id=Column(Integer,ForeignKey('forms.id'),nullable=False);submitted_at=Column(DateTime,default=datetime.utcnow);form=relationship('Form',back_populates='responses');answers=relationship('Answer',back_populates='response',cascade='all, delete-orphan')
class Answer(Base):
 __tablename__='answers';id=Column(Integer,primary_key=True);response_id=Column(Integer,ForeignKey('responses.id'),nullable=False);question_id=Column(Integer,ForeignKey('questions.id'),nullable=False);value_text=Column(Text,nullable=True);value_number=Column(String(100),nullable=True);value_boolean=Column(Boolean,nullable=True);value_json=Column(Text,nullable=True);response=relationship('Response',back_populates='answers');question=relationship('Question',back_populates='answers')
Index('ix_questions_form_position',Question.form_id,Question.position)
Index('ix_answers_response',Answer.response_id)
