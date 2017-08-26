//On page load, auto-fill for today's date
$(document).ready(function() {
	var today = new Date();
	var year = today.getFullYear();
	var month = today.getMonth() + 1;
	var day = today.getDate();

	var dateFormatted = year + '-';
	if (month < 10) {
		dateFormatted += '0';
	}
	dateFormatted += month + '-';
	if (day < 10) {
		dateFormatted += '0';
	}
	dateFormatted += day;

	$('#date').val(dateFormatted);
});

// calculate age from date of birth
$('#dob').focusout(function() {
	var dob = $(this).val();
	var bday = new Date(dob);
	var today = new Date();
	var age =  Math.floor((today-bday) / (365.25 * 24 * 60 * 60 * 1000));
	$('#age').val(age);
	console.log(dob);
});


// Add inputs when buttons are clicked
var impressionForm = $('#impression').find('form');

function addDiagnosis() {
	impressionForm.append(lineBreak).append(htmlInput);
	impressionForm.find('input:last').attr('name', 'diagnosis');
}

var treatmentForm = $('#treatments').find('form');

function addTreatment() {
	treatmentForm.append(lineBreak).append(htmlInput);
	treatmentForm.find('input:last').attr('name', 'treatment');
}

var planForm = $('#plan').find('form');

function addPlan() {
	planForm.append(lineBreak).append(htmlInput);
	planForm.find('input:last').attr('name', 'plan');
	// to add code for adding id
}


// when submit button clicked, gather all infor from page to send off to confirmation page
function submitForm() {

}