from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Patient, Diagnosis, Treatment

engine = create_engine('sqlite:///patientfiles.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

## Routes for saving patients, editing and deleting
@app.route('/')
@app.route('/physiofiles/')
def showPatients():
	return "page to show list of physio/patient files" #render_template('')

@app.route('/physiofiles/new/')
def newPatient():
	return "page to create a new patient"

@app.route('/physiofiles/<int:patient_id>/edit/')
def editPatient():
	return "page to edit a patient's personal details"

@app.route('/physiofiles/<int:patient_id>/delete/')
def deletePatient():
	return "page to edit a patient's personal details"


## Diagnoses/episodes
@app.route('/physiofiles/<int:patient_id>/')
@app.route('/physiofiles/<int:patient_id>/diagnoses/')
def showDiagnoses():
	return "page for showing all episodes for a specific patient"

@app.route('/physiofiles/<int:patient_id>/diagnoses/new/')
def newDiagnosis():
	return "page for creating a new diagnosis or episode for a specific patient"

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/edit/')
def editDiagnosis():
	return "page to edit an existing episode"

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/edit/')
def deleteDiagnosis():
	return "page to confirm deletion of an episode"


##Treatments
@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/')
@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/')
def showTreatments():
	return "Shows all treatments provided for a particular diagnosis for a patient"

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/new/')
def newTreatment():
	return "Create a new treatment provided"

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/<int:treatment_id>/edit/')
def editTreatment():
	return "Edit treatment"

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/<int:treatment_id>/delete/')
def deletetreatment():
	return "Cnofirm deletion of a treatment"


## For running website on localhost:5000 in debug mode (automatic refresh of webserver on file save)
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
