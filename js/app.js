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

// Add body chart image to canvas
function loadCanvas() { //getContext below only works on DOM element, not jQuery object. Hence getElementById is used
	var canvas = document.getElementById("myCanvas"); 
	var context = canvas.getContext('2d');
	
	var img = new Image();
	var x = 0;
	var y = -10;
	var imgWidth = canvas.width;
	var imgHeight = canvas.height;

	img.onload = function() {
		context.drawImage(img, x, y, imgWidth, imgHeight);
	}
	img.src = "img/body_chart_0.5x.png";
}
loadCanvas();

// Create drawing capabilities onto canvas
var colour = 'red';
var $canvas = $('#myCanvas');
var context = $canvas[0].getContext("2d");
var lastEvent;
var mouseDown = false;

$canvas.mousedown(function(event) {
	lastEvent = event;
	mouseDown = true;
}).mousemove(function(event) {
	// Draw lines
	if (mouseDown) {
		context.beginPath();
		context.moveTo(lastEvent.offsetX, lastEvent.offsetY);
		context.lineTo(event.offsetX, event.offsetY);
		context.strokeStyle = colour;
		context.stroke();
		lastEvent = event;
	}
}).mouseup(function() {
	mouseDown = false;
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