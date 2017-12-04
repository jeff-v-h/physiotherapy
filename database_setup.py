import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, VARCHAR, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Patient(Base):
	__tablename__ = 'patient'

	id = Column(Integer, primary_key=True)
	title = Column(String(4), nullable=False)
	firstname = Column(String(80), nullable=False)
	lastname = Column(String(80), nullable=False)
	birthdate = Column(VARCHAR(10), nullable=False)
	mobile = Column(BigInteger, unique=True, nullable=False)
	home_ph = Column(BigInteger)
	work_ph = Column(BigInteger)
	email = Column(String(120), unique=True)
	occupation = Column(String(80))
	diagnoses = relationship('Diagnosis', backref='patient', lazy=True)

class Diagnosis(Base):
	__tablename__ = 'diagnosis'

	id = Column(Integer, primary_key=True)
	patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
	name = Column(String(80), nullable=False)
	name_two = Column(String(80))
	name_three = Column(String(80))
	
	subjective = relationship('Subjective', backref='diagnosis', lazy=True)
	body_chart = relationship('BodyChart', backref='diagnosis', lazy=True)
	objective = relationship('Objective', backref='diagnosis', lazy=True)
	treatments = relationship('Treatment', backref='diagnosis', lazy=True)

class Subjective(Base):
	__tablename__ = 'subjective'

	id = Column(Integer, primary_key=True)
	diagnosis_id = Column(Integer, ForeignKey('diagnosis.id'), nullable=False)
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
	comments = Column(String(250))

class BodyChart(Base):
	__tablename__ = 'body_chart'

	id = Column(Integer, primary_key=True)
	body_chart = Column(LargeBinary)
	diagnosis_id = Column(Integer, ForeignKey('diagnosis.id'), nullable=False)

class Objective(Base):
	__tablename__ = 'objective'

	id = Column(Integer, primary_key=True)
	diagnosis_id = Column(Integer, ForeignKey('diagnosis.id'), nullable=False)
	observation = Column(String(1000))
	active = Column(String(1000))
	passive = Column(String(1000))
	strength = Column(String(1000))
	functional = Column(String(1000))
	neurological = Column(String(1000))
	special_tests = Column(String(1000))
	passive_accessory = Column(String(1000))
	palpation = Column(String(1000))
	other_tests = Column(String(1000))

class Treatment(Base):
	__tablename__ = 'treatment'

	id = Column(Integer, primary_key=True)
	diagnosis_id = Column(Integer, ForeignKey('diagnosis.id'), nullable=False)
	treatment1 = Column(String(250), nullable=False)
	treatment2 = Column(String(250))
	treatment3 = Column(String(250))
	treatment4 = Column(String(250))
	treatment5 = Column(String(250))
	treatment6 = Column(String(250))
	treatment7 = Column(String(250))
	treatment8 = Column(String(250))
	comments = Column(String(250))
	plan = Column(String(250))
	

engine = create_engine('sqlite:///patientfiles.db')

Base.metadata.create_all(engine)
