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
''''
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
'''

## Routes for saving patients, editing and deleting
@app.route('/')
@app.route('/physiofiles/')
def showPatients():
	patientList = session.query(Patient).all()
	return render_template('patients.html', patients = patientList)

@app.route('/physiofiles/new/', methods=['GET', 'POST'])
def newPatient(): 
	if request.method == 'POST':
		newPatient = Patient(title=request.form['title'], firstname = request.form['firstname'], lastname = request.form['lastname'], birthdate = request.form['dob'], mobile = request.form['mobile'], home_ph = request.form['home-ph'], work_ph = request.form['work-ph'], email = request.form['email'], occupation = request.form['occupation'])
		session.add(newPatient)
		session.commit()
		return redirect(url_for('showPatients'))
	else:
		return render_template('newpatient.html')

@app.route('/physiofiles/<int:patient_id>/edit/', methods=['GET', 'POST'])
def editPatient(patient_id):
	patientToEdit = session.query(Patient).filter_by(id = patient_id).one()
	if request.method == 'POST':
		if request.form['firstname'] and request.form['lastname']:
			patientToEdit.firstname = request.form['firstname']
			patientToEdit.lastname = request.form['lastname']
		session.add(patientToEdit)
		session.commit()
		return redirect(url_for('showPatients'))
	else:
		return render_template('editpatient.html', patient = patientToEdit)

@app.route('/physiofiles/<int:patient_id>/delete/', methods=['GET', 'POST'])
def deletePatient(patient_id):
	patientToDelete = session.query(Patient).filter_by(id = patient_id).one()
	if request.method == 'POST':
		session.delete(patientToDelete)
		session.commit()
		return redirect(url_for('showPatients'))
	else:
		return render_template('deletepatient.html', patient = patientToDelete)


## Diagnoses/episodes
@app.route('/physiofiles/<int:patient_id>/')
@app.route('/physiofiles/<int:patient_id>/diagnoses/')
def showDiagnoses(patient_id):
	diagnosesForPatient = session.query(Diagnosis).filter_by(patient_id = patient_id).all()
	patient = session.query(Patient).filter_by(id = patient_id).one()
	return render_template('diagnoses.html', patient = patient, diagnoses = diagnosesForPatient)

@app.route('/physiofiles/<int:patient_id>/diagnoses/new/', methods=['GET', 'POST'])
def newDiagnosis(patient_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	if request.method == 'POST':
		newDiagnosis = Diagnosis(name = request.form['diagnosis'], patient_id = patient.id)
		session.add(newDiagnosis)
		session.commit()
		return redirect(url_for('showDiagnoses', patient_id = patient.id))
	else:
		return render_template('newdiagnosis.html', patient = patient)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/edit/', methods=['GET', 'POST'])
def editDiagnosis(patient_id, diagnosis_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	diagnosisToEdit = session.query(Diagnosis).filter_by(id = diagnosis_id).one()
	if request.method == 'POST':
		if request.form['diagnosis']:
			diagnosisToEdit.name = request.form['diagnosis']
			session.add(diagnosisToEdit)
			session.commit()
		return redirect(url_for('showDiagnoses', patient_id = patient.id))
	else:
		return render_template('editdiagnosis.html', patient = patient, diagnosis = diagnosisToEdit)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/delete/', methods=['GET', 'POST'])
def deleteDiagnosis(patient_id, diagnosis_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	diagnosisToDelete = session.query(Diagnosis).filter_by(id = diagnosis_id).one()
	if request.method == 'POST':
		session.delete(diagnosisToDelete)
		session.commit()
		return redirect(url_for('showDiagnoses', patient_id = patient.id))
	else:
		return render_template('deletediagnosis.html', patient = patient, diagnosis = diagnosisToDelete)


##Treatments
@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/')
@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/')
def showTreatments(patient_id, diagnosis_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	diagnosis = session.query(Diagnosis).filter_by(id = diagnosis_id).one()
	treatments = session.query(Treatment).filter_by(diagnosis_id = diagnosis_id).all()
	return render_template('treatments.html', patient = patient, diagnosis = diagnosis, treatments = treatments)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/new/', methods=['GET', 'POST'])
def newTreatment(patient_id, diagnosis_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	diagnosis = session.query(Diagnosis).filter_by(id = diagnosis_id).one()
	if request.method == 'POST':
		newTreatment = Treatment(name = request.form['treatment'], patient_id = patient.id, diagnosis_id = diagnosis.id, description = request.form['comment'])
		session.add(newTreatment)
		session.commit()
		return redirect(url_for('showTreatments', patient_id = patient.id, diagnosis_id = diagnosis.id))
	else:
		return render_template('newtreatment.html', patient = patient, diagnosis = diagnosis)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/<int:treatment_id>/edit/', methods=['GET', 'POST'])
def editTreatment(patient_id, diagnosis_id, treatment_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	diagnosis = session.query(Diagnosis).filter_by(id = diagnosis_id).one()
	treatmentToEdit = session.query(Treatment).filter_by(id = treatment_id).one()
	if request.method == 'POST':
		if request.form['treatment']:
			treatmentToEdit.name = request.form['treatment']
			session.add(treatmentToEdit)
			session.commit()
		return redirect(url_for('showTreatments', patient_id = patient.id, diagnosis_id = diagnosis.id))
	else:
		return render_template('edittreatment.html', patient = patient, diagnosis = diagnosis, treatment = treatmentToEdit)

@app.route('/physiofiles/<int:patient_id>/diagnoses/<int:diagnosis_id>/treatments/<int:treatment_id>/delete/', methods=['GET', 'POST'])
def deleteTreatment(patient_id, diagnosis_id, treatment_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	diagnosis = session.query(Diagnosis).filter_by(id = diagnosis_id).one()
	treatmentToDelete = session.query(Treatment).filter_by(id = treatment_id).one()
	if request.method == 'POST':
		session.delete(treatmentToDelete)
		session.commit()
		return redirect(url_for('showTreatments', patient_id = patient.id, diagnosis_id = diagnosis.id))
	else:
		return render_template('deletetreatment.html', patient = patient, diagnosis = diagnosis, treatment = treatmentToDelete)


## For running website on localhost:5000 in debug mode (automatic refresh of webserver on file save)
if __name__ == '__main__':
	app.secret_key = 'secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
