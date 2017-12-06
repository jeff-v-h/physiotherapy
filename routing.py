from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Patient, Episode, BodyChart, Consultation
from datetime import date

engine = create_engine('sqlite:///patientfiles.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

## Routes for saving patients, viewing, editing and deleting
@app.route('/')
@app.route('/ptfiles/')
def patientList():
	patientList = session.query(Patient).all()
	return render_template('patientlist.html', patients = patientList)

@app.route('/ptfiles/new/', methods=['GET', 'POST'])
def newPatient(): 
	if request.method == 'POST':
		newPatient = Patient(date_started = request.form['date'], title=request.form['title'], firstname = request.form['firstname'], lastname = request.form['lastname'], birthdate = request.form['dob'], mobile = request.form['mobile'], home_ph = request.form['home-ph'], work_ph = request.form['work-ph'], email = request.form['email'], occupation = request.form['occupation'])
		session.add(newPatient)
		session.commit()
		return redirect(url_for('patientList'))
	else:
		return render_template('newpatient.html')

@app.route('/ptfiles/<int:patient_id>/episodes')
@app.route('/ptfiles/<int:patient_id>/info/')
def patientInfo(patient_id):
	episodesForPatient = session.query(Episode).filter_by(patient_id = patient_id).all()
	patient = session.query(Patient).filter_by(id = patient_id).one()
	return render_template('patientinfo.html', patient = patient, episodes = episodesForPatient)

@app.route('/physiofiles/<int:patient_id>/edit/', methods=['GET', 'POST'])
def editPatient(patient_id):
	patientToEdit = session.query(Patient).filter_by(id = patient_id).one()
	if request.method == 'POST':
		if request.form['firstname'] and request.form['lastname'] and request.form['dob'] and request.form['mobile']:
			patientToEdit.date_started = request.form['date']
			patientToEdit.title = request.form['title']
			patientToEdit.firstname = request.form['firstname']
			patientToEdit.lastname = request.form['lastname']
			patientToEdit.birthdate = request.form['dob']
			patientToEdit.mobile = request.form['mobile']
			patientToEdit.home_ph = request.form['home-ph']
			patientToEdit.work_ph = request.form['work-ph']
			patientToEdit.email = request.form['email']
			patientToEdit.occupation = request.form['occupation']
			session.add(patientToEdit)
			session.commit()
		else:
			print "fields required: firstname, lastname, date of birth and mobile"
		return redirect(url_for('patientInfo', patient_id = patientToEdit.id))
	else:
		return render_template('editpatient.html', patient = patientToEdit)

@app.route('/ptfiles/<int:patient_id>/delete/', methods=['GET', 'POST'])
def deletePatient(patient_id):
	patientToDelete = session.query(Patient).filter_by(id = patient_id).one()
	if request.method == 'POST':
		session.delete(patientToDelete)
		session.commit()
		return redirect(url_for('patientList'))
	else:
		return render_template('deletepatient.html', patient = patientToDelete)


## Diagnoses/episodes
@app.route('/ptfiles/<int:patient_id>/episodes/new/', methods=['GET', 'POST'])
def newEpisode(patient_id):
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
		newEpisode = Episode(patient_id = patient.id, pain = request.form['pain'], pain_description = request.form['pain-description'], pins_needles = pnInput, numbness = nbInput, current_history = request.form['current-history'], aggs = request.form['agg'], ease = request.form['ease'], daily_history = request.form['24hr'], past_history = request.form['past-hx'], social_history = request.form['social-hx'], special_q = request.form['special-q'], comments = request.form['comments'], diagnosis1 = request.form['diagnosis1'], diagnosis2 = request.form['diagnosis2'], diagnosis3 = request.form['diagnosis3'])
		session.add(newEpisode)
		# flush() to have primary_key (id) field updated into database for the Diagnosis
		session.flush()
		if request.form.get('consent'):
			consentInput = True
		else:
			consentInput = False
		newConsultation = Consultation(initial = True, observation = request.form['observation'], consent = consentInput, active = request.form['active'], passive = request.form['passive'], strength = request.form['strength'], functional = request.form['functional'], neurological = request.form['neurological'], special_tests = request.form['special-tests'], passive_accessory = request.form['passive-accessory'], palpation = request.form['palpation'], other_tests = request.form['other-tests'], treatments = request.form['treatments'], comments = request.form['treatment-comments'], plan = request.form['plan'], episode_id = newEpisode.id)
		session.add(newConsultation)

		session.commit()
		return redirect(url_for('episodeInfo', patient_id = patient.id, episode_id = newEpisode.id))
	else:
		return render_template('newepisode.html', patient = patient)

@app.route('/ptfiles/<int:patient_id>/episodes/<int:episode_id>/info')
@app.route('/ptfiles/<int:patient_id>/episodes/<int:episode_id>/consults/')
def episodeInfo(patient_id, episode_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	episode = session.query(Episode).filter_by(id = episode_id).one()
	consults = session.query(Consultation).filter_by(episode_id = episode_id).all()
	return render_template('episodeinfo.html', patient = patient, episode = episode, consults = consults)

@app.route('/ptfiles/<int:patient_id>/episodes/<int:episode_id>/edit/', methods=['GET', 'POST'])
def editEpisode(patient_id, episode_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	episodeToEdit = session.query(Episode).filter_by(id = episode_id).one()
	if request.method == 'POST':
		if request.form['diagnosis1'] and request.form['current-history']:
			if request.form.get('pins-needles'):
				pnInput = True
			else:
				pnInput = False
			if request.form.get('numbness'):
				nbInput = True
			else:
				nbInput = False
			episodeToEdit.diagnosis1 = request.form['diagnosis1']
			episodeToEdit.pain = request.form['pain']
			episodeToEdit.pain_description = request.form['pain-description']
			episodeToEdit.pins_needles = pnInput
			episodeToEdit.numbness = nbInput
			episodeToEdit.current_history = request.form['current-history']
			episodeToEdit.aggs = request.form['agg']
			episodeToEdit.ease = request.form['ease']
			episodeToEdit.daily_history = request.form['24hr']
			episodeToEdit.past_history = request.form['past-hx']
			episodeToEdit.social_history = request.form['social-hx']
			episodeToEdit.special_q = request.form['special-q']
			episodeToEdit.comments = request.form['comments']
			episodeToEdit.diagnosis1 = request.form['diagnosis1']
			episodeToEdit.diagnosis2 = request.form['diagnosis2']
			episodeToEdit.diagnosis3 = request.form['diagnosis3']
			session.add(episodeToEdit)
			session.commit()
		else:
			print "fields required: diagnosis1 and current history"
		return redirect(url_for('episodeInfo', patient_id = patient.id, episode_id = episodeToEdit.id))
	else:
		return render_template('editepisode.html', patient = patient, episode = episodeToEdit)

@app.route('/ptfiles/<int:patient_id>/episodes/<int:episode_id>/delete/', methods=['GET', 'POST'])
def deleteEpisode(patient_id, episode_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	episodeToDelete = session.query(Episode).filter_by(id = episode_id).one()
	associatedConsults = session.query(Consultation).filter_by(episode_id = episode_id).all()
	if request.method == 'POST':
		session.delete(episodeToDelete)
		for consult in associatedConsults:
			session.delete(consult)
		session.commit()
		return redirect(url_for('patientInfo', patient_id = patient.id))
	else:
		return render_template('deleteepisode.html', patient = patient, episode = episodeToDelete)


##New, view, edit and delete consult/treatment pages
@app.route('/ptfiles/<int:patient_id>/episodes/<int:episode_id>/consults/new/', methods=['GET', 'POST'])
def newConsult(patient_id, episode_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	episode = session.query(Episode).filter_by(id = episode_id).one()
	if request.method == 'POST':
		if request.form.get('consent'):
			consentInput = True
		else:
			consentInput = False
		newConsult = Consultation(episode_id = episode.id, initial = False, subjective = request.form['subjective'], observation = request.form['observation'], consent = consentInput, active = request.form['active'], passive = request.form['passive'], strength = request.form['strength'], functional = request.form['functional'], neurological = request.form['neurological'], special_tests = request.form['special-tests'], passive_accessory = request.form['passive-accessory'], palpation = request.form['palpation'], other_tests = request.form['other-tests'], treatments = request.form['treatments'], comments = request.form['treatment-comments'], plan = request.form['plan'])
		session.add(newConsult)
		session.commit()
		return redirect(url_for('episodeInfo', patient_id = patient.id, episode_id = episode.id))
	else:
		return render_template('newconsult.html', patient = patient, episode = episode)

@app.route('/ptfiles/<int:patient_id>/episodes/<int:episode_id>/consults/<int:consult_id>/')
def consultInfo(patient_id, episode_id, consult_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	episode = session.query(Episode).filter_by(id = episode_id).one()
	consult = session.query(Consultation).filter_by(id = consult_id).one()
	return render_template('consultinfo.html', patient = patient, episode = episode, consult = consult)

@app.route('/ptfiles/<int:patient_id>/episodes/<int:episode_id>/consults/<int:consult_id>/edit/', methods=['GET', 'POST'])
def editConsult(patient_id, episode_id, consult_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	episode = session.query(Episode).filter_by(id = episode_id).one()
	consultToEdit = session.query(Consultation).filter_by(id = consult_id).one()
	if request.method == 'POST':
		if request.form['treatments']:
			if request.form.get('consent'):
				consentInput = True
			else:
				consentInput = False
			consultToEdit.subjective = request.form['subjective']
			consultToEdit.observation = request.form['observation']
			consultToEdit.consent = consentInput
			consultToEdit.active = request.form['active']
			consultToEdit.passive = request.form['passive']
			consultToEdit.strength = request.form['strength']
			consultToEdit.functional = request.form['functional']
			consultToEdit.neurological = request.form['neurological']
			consultToEdit.special_tests = request.form['special-tests']
			consultToEdit.passive_accessory = request.form['passive-accessory']
			consultToEdit.palpation = request.form['palpation']
			consultToEdit.other_tests = request.form['other-tests']
			consultToEdit.treatments = request.form['treatments']
			consultToEdit.comments = request.form['treatment-comments']
			consultToEdit.plan = request.form['plan']
			session.add(consultToEdit)
			session.commit()
		return redirect(url_for('consultInfo', patient_id = patient.id, episode_id = episode.id, consult_id = consultToEdit.id))
	else:
		return render_template('editconsult.html', patient = patient, episode = episode, consult = consultToEdit)

@app.route('/ptfiles/<int:patient_id>/episodes/<int:episode_id>/consults/<int:consult_id>/delete/', methods=['GET', 'POST'])
def deleteConsult(patient_id, episode_id, consult_id):
	patient = session.query(Patient).filter_by(id = patient_id).one()
	episode = session.query(Episode).filter_by(id = episode_id).one()
	consultToDelete = session.query(Consultation).filter_by(id = consult_id).one()
	if request.method == 'POST':
		session.delete(consultToDelete)
		session.commit()
		return redirect(url_for('episodeInfo', patient_id = patient.id, episode_id = episode.id))
	else:
		return render_template('deleteconsult.html', patient = patient, episode = episode, consult = consultToDelete)


## For running website on localhost:5000 in debug mode (automatic refresh of webserver on file save)
if __name__ == '__main__':
	app.secret_key = 'secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
