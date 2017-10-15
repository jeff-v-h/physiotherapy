from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Patient, Diagnosis, Treatment

engine = create_engine('sqlite:///patientfiles.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Temporary data
temppatient = {'name': 'Jeffrey Huang', 'id': '1'}
temppatients = [{'name': 'Jeffrey Huang', 'id': '1'}, {'name': 'Katherine Kuorence', 'id': '2'}, 
{'name': 'Timothy Lee', 'id': '3'}]
tempdiagnoses = [{'name': 'lumbar disc bulge', 'id': '1', 'patient_id': '1', 'patient': 'Jeffrey Huang'}, 
{'name': 'Hamstring Tendinopathy', 'id': '2', 'patient_id': '2', 'patient': 'Katherine Kuorence'}, 
{'name': 'PCL tear', 'id': '3', 'patient_id': '3', 'patient': 'Timothy Lee'}]
tempdiagnosis = {'name': 'lumbar disc bulge', 'id': '1', 'patient_id': '1', 'patient': 'Jeffrey Huang'}
temptreatment = {'name': 'mobilisations', 'id': '1', 'description': 'grade 2 PA L1-5', 'patient_id': '1', 'patient': 'Jeffrey Huang', 'diagnosis_id': '1', 'diagnosis': 'lumbar disc bulge'}
temptreatments = [{'name': 'mobilisations', 'id': '1', 'description': 'grade 2 PA L1-5', 'patient_id': '1', 'patient': 'Jeffrey Huang', 'diagnosis_id': '1', 'diagnosis': 'lumbar disc bulge'}, 
{'name': 'Eccentric hamstring curls', 'id': '2', 'description': '3sets 15reps 2.5kg', 'patient_id': '2', 'patient': 'Katherine Kuorence', 'diagnosis_id': '2', 'diagnosis': 'Hamstring Tendinopathy'}, 
{'name': 'Short arc quad extensions', 'id': '3', 'description': '3sets 6reps', 'patient_id': '3', 'patient': 'Timothy Lee', 'diagnosis_id': '3', 'diagnosis': 'PCL tear'}]

## Routes for saving patients, editing and deleting
@app.route('/')
@app.route('/physiofiles/')
def showPatients():
	return render_template('patients.html', patients = temppatients)

@app.route('/physiofiles/new/')
def newPatient():
	return render_template('newpatient.html')

@app.route('/physiofiles/<int:patient_id>/edit/')
def editPatient(patient_id):
	return render_template('editpatient.html', patient = temppatient)

@app.route('/physiofiles/<int:patient_id>/delete/')
def deletePatient(patient_id):
	return render_template('deletepatient.html', patient = temppatient)


## Diagnoses/episodes
@app.route('/physiofiles/<int:patient_id>/')
@app.route('/physiofiles/<int:patient_id>/diagnoses/')
def showDiagnoses(patient_id):
	return render_template('diagnoses.html', patient = temppatient, diagnoses = tempdiagnoses)

@app.route('/physiofiles/<int:patient_id>/diagnoses/new/')
def newDiagnosis(patient_id):
	return render_template('newdiagnosis.html', patient = temppatient)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/edit/')
def editDiagnosis(patient_id, diagnosis_id):
	return render_template('editdiagnosis.html', patient = temppatient, diagnosis = tempdiagnosis)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/delete/')
def deleteDiagnosis(patient_id, diagnosis_id):
	return render_template('deletediagnosis.html', patient = temppatient, diagnosis = tempdiagnosis)


##Treatments
@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/')
@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/')
def showTreatments(patient_id, diagnosis_id):
	return render_template('treatments.html', patient = temppatient, diagnosis = tempdiagnosis, treatments = temptreatments)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/new/')
def newTreatment(patient_id, diagnosis_id):
	return render_template('newtreatment.html', patient = temppatient, diagnosis = tempdiagnosis)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/<int:treatment_id>/edit/')
def editTreatment(patient_id, diagnosis_id, treatment_id):
	return render_template('edittreatment.html', patient = temppatient, diagnosis = tempdiagnosis, treatment = temptreatment)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/<int:treatment_id>/delete/')
def deletetreatment(patient_id, diagnosis_id, treatment_id):
	return render_template('deletetreatment.html', patient = temppatient, diagnosis = tempdiagnosis, treatment = temptreatment)


## For running website on localhost:5000 in debug mode (automatic refresh of webserver on file save)
if __name__ == '__main__':
	app.secret_key = 'secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
