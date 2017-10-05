import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Patient(Base):
	__tablename__ = 'patient'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)


class Diagnosis(Base):
	__tablename__ = 'diagnosis'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	patient_id = Column(Integer, ForeignKey('patient.id'))
	patient = relationship(Patient)


class Treatment(Base):
	__tablename__ = 'treatment'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(250))
	patient_id = Column(Integer, ForeignKey('patient.id'))
	patient = relationship(Patient)
	diagnosis_id = Column(Integer, ForeignKey('diagnosis.id'))
	diagnosis = relationship(Diagnosis)

engine = create_engine('sqlite:///patientfiles.db')

Base.metadata.create_all(engine)
