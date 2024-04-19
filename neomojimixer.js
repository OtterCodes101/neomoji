//global variables

//Arrays to hold the parts
let eyes = [];
let body = [];
let mouth = [];
let arms = [];

//Index to easily find when to roll back to the first/last element in the list
let inex_eyes = 0;
let index_body = 0;
let index_mouth = 0;
let index_arms = 0;

//shotnames for HTML elements to interact with

//images
const body_image = document.getElementById("body_img");
const eyes_image = document.getElementById("eyes_img");
const mouth_image = document.getElementById("mouth_img");
const arms_image = document.getElementById("arms_img");

const canvas = document.getElementById("canvas_export");
const neomoji_name = document.getElementById("fullNeomojiName");

//names
const body_name = document.getElementById("body_name");
const eyes_name = document.getElementById("eyes_name");
const mouth_name = document.getElementById("mouth_name");
const arms_name = document.getElementById("arms_name");

//Stats
const stats = document.getElementById("stats");


// Loading the JSON and getting all the available parts
async function getData() {
	
	fetch('./parts.json')
  	.then(function(response) {
   	 return response.json();
  	})
 	 .then(function(data) {
   	 loadParts(data);
 	 })
  	.catch(function(error) {
  	  console.log('An error occurred:', error);
 	 });
}

function loadParts(parts) {
	//Load parts into Arrays
	parts.type.eyes.forEach(fillArrayEyes);
	parts.type.body.forEach(fillArrayBody);
	parts.type.mouth.forEach(fillArrayMouth);
	parts.type.arms.forEach(fillArrayArms);
	
	//Randomize initial view
	randomize();
	
	//Show little statistic
	var sum = body.length + eyes.length + mouth.length + arms.length;
	var variety = body.length * eyes.length * mouth.length * arms.length;
	
	stats.innerHTML = "There are " + sum + " Elements available,<br />with " + new Intl.NumberFormat("de-DE").format(variety) + " possible combinations.";
	
	//Activate the buttons after everything is loaded in
	document.getElementById("body_left").disabled = false;
	document.getElementById("body_right").disabled = false;
	document.getElementById("eyes_left").disabled = false;
	document.getElementById("eyes_right").disabled = false;
	document.getElementById("mouth_left").disabled = false;
	document.getElementById("mouth_right").disabled = false;
	document.getElementById("arms_left").disabled = false;
	document.getElementById("arms_right").disabled = false;
	document.getElementById("random").disabled = false;
	document.getElementById("export").disabled = false;

}

function fillArrayEyes(item){
	var name = item.name;
	var url = item.url;
	eyes.push ([name, url]); //Two dimensional array, Second dimension holds name on index 0 and url at index 1
}

function fillArrayBody(item){
	var name = item.name;
	var url = item.url;
	body.push ([name, url]); //Two dimensional array, Second dimension holds name on index 0 and url at index 1
}

function fillArrayMouth(item){
	var name = item.name;
	var url = item.url;
	mouth.push ([name, url]); //Two dimensional array, Second dimension holds name on index 0 and url at index 1
}

function fillArrayArms(item){
	var name = item.name;
	var url = item.url;
	arms.push ([name, url]); //Two dimensional array, Second dimension holds name on index 0 and url at index 1
}

function onClick_body_next(){
	index_body++;
	
	if (index_body == body.length) {index_body = 0;} //check if index is too big for the array
	
	body_image.src = "." + body[index_body][1]; //Change URL of picture
	body_name.innerHTML = body[index_body][0]; //Change name in controls
}

function onClick_body_prev(){
	index_body--;
	
	if (index_body < 0) {index_body = (body.length-1);} //check if index is too big for the array
	
	body_image.src = "." + body[index_body][1]; //Change URL of picture
	body_name.innerHTML = body[index_body][0]; //Change name in controls
}

function onClick_eyes_next(){
	index_eyes++;
	
	if (index_eyes == eyes.length) {index_eyes = 0;} //check if index is too big for the array
	
	eyes_image.src = "." + eyes[index_eyes][1]; //Change URL of picture
	eyes_name.innerHTML = eyes[index_eyes][0]; //Change name in controls
}

function onClick_eyes_prev(){
	index_eyes--;
	
	if (index_eyes < 0) {index_eyes = (eyes.length-1);} //check if index is too big for the array
	
	eyes_image.src = "." + eyes[index_eyes][1]; //Change URL of picture
	eyes_name.innerHTML = eyes[index_eyes][0]; //Change name in controls
}

function onClick_mouth_next(){
	index_mouth++;
	
	if (index_mouth == mouth.length) {index_mouth = 0;} //check if index is too big for the array
	
	mouth_image.src = "." + mouth[index_mouth][1]; //Change URL of picture
	mouth_name.innerHTML = mouth[index_mouth][0]; //Change name in controls
}

function onClick_mouth_prev(){
	index_mouth--;
	
	if (index_mouth < 0) {index_mouth = (mouth.length-1);} //check if index is too big for the array
	
	mouth_image.src = "." + mouth[index_mouth][1]; //Change URL of picture
	mouth_name.innerHTML = mouth[index_mouth][0]; //Change name in controls
}

function onClick_arms_next(){
	index_arms++;
	
	if (index_arms == arms.length) {index_arms = 0;} //check if index is too big for the array
	
	arms_image.src = "." + arms[index_arms][1]; //Change URL of picture
	arms_name.innerHTML = arms[index_arms][0]; //Change name in controls
}

function onClick_arms_prev(){
	index_arms--;
	
	if (index_arms < 0) {index_arms = (arms.length-1);} //check if index is too big for the array
	
	arms_image.src = "." + arms[index_arms][1]; //Change URL of picture
	arms_name.innerHTML = arms[index_arms][0]; //Change name in controls
}

function randomize(){ //Randomize which parts are shown
	index_body = Math.floor(Math.random() * body.length);
	index_eyes = Math.floor(Math.random() * eyes.length);
	index_mouth = Math.floor(Math.random() * mouth.length);
	index_arms = Math.floor(Math.random() * arms.length);
	
	body_image.src = "." + body[index_body][1];
	eyes_image.src = "." + eyes[index_eyes][1];
	mouth_image.src = "." + mouth[index_mouth][1];
	arms_image.src = "." + arms[index_arms][1];
	
	body_name.innerHTML = body[index_body][0];
	eyes_name.innerHTML = eyes[index_eyes][0];
	mouth_name.innerHTML = mouth[index_mouth][0];
	arms_name.innerHTML = arms[index_arms][0];
}

function exportImage(){ //Export image so it can be saved as one PNG
	var ctx=canvas.getContext("2d");
	
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	
	var body_export = new Image();
	var eyes_export = new Image();
	var mouth_export = new Image();
	var arms_export = new Image();
	
	body_export.src = "." + body[index_body][1];
	body_export.onload = function() {
		ctx.drawImage(body_export, 0, 0, 256, 256);
		eyes_export.src = "." + eyes[index_eyes][1];
		eyes_export.onload = function() {
			ctx.drawImage(eyes_export, 0, 0, 256, 256);
			mouth_export.src = "." + mouth[index_mouth][1];
			mouth_export.onload = function() {
				ctx.drawImage(mouth_export, 0, 0, 256, 256);
				arms_export.src = "." + arms[index_arms][1];
					arms_export.onload = function() {
					ctx.drawImage(arms_export, 0, 0, 256, 256);
					}
			}
		}
	};
	
	neomoji_name.value = body[index_body][0] + "_" + eyes[index_eyes][0] + "_" + mouth[index_mouth][0] + "_" + arms[index_arms][0];
	
	canvas.hidden = false;
	neomoji_name.hidden = false;
	document.getElementById("exportSaveMessage").hidden = false;
}

//Main Programm
document.getElementById("noJSmessage").hidden = true;
getData();