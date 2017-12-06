import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Date, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Patient(Base):
	__tablename__ = 'patient'

	id = Column(Integer, primary_key=True)
	date_started = Column(String(10))
	title = Column(String(4), nullable=False)
	firstname = Column(String(80), nullable=False)
	lastname = Column(String(80), nullable=False)
	birthdate = Column(String(10), nullable=False)
	mobile = Column(BigInteger, unique=True, nullable=False)
	home_ph = Column(BigInteger)
	work_ph = Column(BigInteger)
	email = Column(String(120))
	occupation = Column(String(80))

	episodes = relationship('Episode', backref='patient', lazy=True)

class Episode(Base):
	__tablename__ = 'episode'

	id = Column(Integer, primary_key=True)
	patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
	diagnosis1 = Column(String(80), nullable=False)
	diagnosis2 = Column(String(80))
	diagnosis3 = Column(String(80))
	pain = Column(Integer)
	pain_description = Column(String(500))
	pins_needles = Column(Boolean)
	numbness = Column(Boolean)
	current_history = Column(String(1000), nullable=False)
	aggs = Column(String(250))
	ease = Column(String(250))
	daily_history = Column(String(250))
	past_history = Column(String(250))
	social_history = Column(String(250))
	special_q = Column(String(250))
	comments = Column(String(1000))

	body_chart = relationship('BodyChart', backref='episode', lazy=True)
	consultations = relationship('Consultation', backref='episode', lazy=True)

class BodyChart(Base):
	__tablename__ = 'body_chart'

	id = Column(Integer, primary_key=True)
	episode_id = Column(Integer, ForeignKey('episode.id'), nullable=False)
	body_chart = Column(LargeBinary)

class Consultation(Base):
	__tablename__ = 'consultation'

	id = Column(Integer, primary_key=True)
	episode_id = Column(Integer, ForeignKey('episode.id'), nullable=False)
	initial = Column(Boolean)
	subjective = Column(String(1000))
	observation = Column(String(500))
	consent = Column(Boolean)
	active = Column(String(500))
	passive = Column(String(500))
	strength = Column(String(500))
	functional = Column(String(500))
	neurological = Column(String(500))
	special_tests = Column(String(500))
	passive_accessory = Column(String(500))
	palpation = Column(String(500))
	other_tests = Column(String(500))
	treatments = Column(String(1000), nullable=False)
	comments = Column(String(1000))
	plan = Column(String(500))
	

engine = create_engine('sqlite:///patientfiles.db')

Base.metadata.create_all(engine)
