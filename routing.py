from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Patient, Diagnosis, BodyChart, Consultation

engine = create_engine('sqlite:///patientfiles.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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
		# add true or false for pins and needles and numbness depending on if it is checked
		if request.form.get('pins-needles'):
			pnInput = True
		else:
			pnInput = False
		if request.form.get('numbness'):
			nbInput = True
		else:
			nbInput = False
		newDiagnosis = Diagnosis(pain = request.form['pain'], pain_description = request.form['pain-description'], pins_needles = pnInput, numbness = nbInput, current_history = request.form['current-history'], aggs = request.form['agg'], ease = request.form['ease'], daily_history = request.form['24hr'], past_history = request.form['past-hx'], social_history = request.form['social-hx'], special_q = request.form['special-q'], comments = request.form['comments'], diagnosis1 = request.form['diagnosis1'], diagnosis2 = request.form['diagnosis2'], diagnosis3 = request.form['diagnosis3'], patient_id = patient.id)
		session.add(newDiagnosis)
		# flush() to have primary_key (id) field updated into database for the Diagnosis
		session.flush()
		if request.form.get('consent'):
			consentInput = True
		else:
			consentInput = False
		newConsultation = Consultation(initial = True, observation = request.form['observation'], consent = consentInput, active = request.form['active'], passive = request.form['passive'], strength = request.form['strength'], functional = request.form['functional'], neurological = request.form['neurological'], special_tests = request.form['special-tests'], passive_accessory = request.form['passive-accessory'], palpation = request.form['palpation'], other_tests = request.form['other-tests'], treatments = request.form['treatments'], comments = request.form['treatment-comments'], plan = request.form['plan'], diagnosis_id = newDiagnosis.id)
		session.add(newConsultation)

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
		newTreatment = Treatment(diagnosis_id = diagnosis.id, treatment1 = request.form['treatment1'], treatment2 = request.form['treatment2'], treatment3 = request.form['treatment3'], treatment4 = request.form['treatment4'], treatment5 = request.form['treatment5'], treatment6 = request.form['treatment1'], treatment7 = request.form['treatment7'], treatment8 = request.form['treatment8'], comments = request.form['comment'])
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
