// On page load, add col and row attributes to all textareas to create size
$(document).ready(function() {
	$('textarea').attr('rows', 5).attr('cols', 30);
});

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
// getContext() below only works on DOM element, not jQuery object. Hence getElementById is used
var canvas = document.getElementById("myCanvas"); 
var context = canvas.getContext('2d');

function loadCanvas() { 
	var img = new Image();
	var x = 0;
	var y = -20;
	var imgWidth = canvas.width;
	var imgHeight = canvas.height;

	//img.src = "{{url_for('static', filename='body_chart.png')}}";
	img.src = "img/body_chart.png"; // THIS NEEDS TO BE FIXED TO WORK WITH PYTHON/FLASK
	img.onload = function() {
		context.drawImage(img, x, y, imgWidth, imgHeight);
	}
	
}
loadCanvas();

// Create drawing capabilities onto canvas
var colour = $('.selected').css('background-color');
var $canvas = $('#myCanvas');
var $context = $canvas[0].getContext("2d");
var lastEvent;
var mouseDown = false;

$canvas.mousedown(function(event) {
	lastEvent = event;
	mouseDown = true;
}).mousemove(function(event) {
	// Draw lines
	if (mouseDown) {
		$context.beginPath();
		$context.moveTo(lastEvent.offsetX, lastEvent.offsetY);
		$context.lineTo(event.offsetX, event.offsetY);
		$context.strokeStyle = colour;
		$context.stroke();
		lastEvent = event;
	}
}).mouseup(function() {
	mouseDown = false;
});

// Selection of colour
$('#colours').on('click', 'div', function() {
	$(this).siblings().removeClass('selected');
	$(this).addClass('selected');
	colour = $(this).css('background-color');
});

// Clear canvas function for button
function clearCanvas() {
	context.clearRect(0, 0, canvas.width, canvas.height);
	loadCanvas();
}

// Add inputs when buttons are clicked
/*var impressionForm = $('#impression').find('form');

function addDiagnosis() {
	impressionForm.append(lineBreak).append(htmlInput);
	impressionForm.find('input:last').attr('name', 'diagnosis');
}*/

/*
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
*/
