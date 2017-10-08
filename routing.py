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
	return render_template('patients.html')

@app.route('/physiofiles/new/')
def newPatient():
	return render_template('newpatient.html')

@app.route('/physiofiles/<int:patient_id>/edit/')
def editPatient(patient_id):
	return render_template('editpatient.html')

@app.route('/physiofiles/<int:patient_id>/delete/')
def deletePatient(patient_id):
	return render_template('deletepatient.html')


## Diagnoses/episodes
@app.route('/physiofiles/<int:patient_id>/')
@app.route('/physiofiles/<int:patient_id>/diagnoses/')
def showDiagnoses(patient_id):
	return render_template('diagnoses.html')

@app.route('/physiofiles/<int:patient_id>/diagnoses/new/')
def newDiagnosis(patient_id):
	return render_template('newdiagnosis.html')

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/edit/')
def editDiagnosis(patient_id, diagnosis_id):
	return render_template('editdiagnosis.html')

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/delete/')
def deleteDiagnosis(patient_id, diagnosis_id):
	return render_template('deletediagnosis.html')


##Treatments
@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/')
@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/')
def showTreatments(patient_id, diagnosis_id):
	return render_template('treatments.html')

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/new/')
def newTreatment(patient_id, diagnosis_id):
	return render_template('newtreatment.html')

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/<int:treatment_id>/edit/')
def editTreatment(patient_id, diagnosis_id, treatment_id):
	return render_template('edittreatment.html')

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/<int:treatment_id>/delete/')
def deletetreatment(patient_id, diagnosis_id, treatment_id):
	return render_template('deletetreatment.html')


## For running website on localhost:5000 in debug mode (automatic refresh of webserver on file save)
if __name__ == '__main__':
	app.secret_key = 'secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
