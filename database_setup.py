import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger, VARCHAR
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
	diagnoses = relationship('Diagnosis', backref='patient', lazy='select')


class Diagnosis(Base):
	__tablename__ = 'diagnosis'

	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	patient_id = Column(Integer, ForeignKey('patient.id'), nullable=False)
	treatments = relationship('Treatment', backref='diagnosis', lazy='select')


class Treatment(Base):
	__tablename__ = 'treatment'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(250))
	diagnosis_id = Column(Integer, ForeignKey('diagnosis.id'))

engine = create_engine('sqlite:///patientfiles.db')

Base.metadata.create_all(engine)
