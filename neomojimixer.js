const NeomojiMixer = (function(NeomojiMixer) {
	//global variables

	//Arrays to hold the parts
	let eyes = [];
	let body = [];
	let mouth = [];
	let arms = [];

	//FOr all the different colours of the arms there will be each a own arraz
	let arms_orange = [];
	let arms_blue = [];
	let arms_lightgrey = [];
	let arms_red = [];
	let arms_white = [];
	let arms_yellow = [];

	//Index to easily find when to roll back to the first/last element in the list
	let inex_eyes = 0;
	let index_body = 0;
	let index_mouth = 0;
	let index_arms = 0;
	let index_color = 0;

	//shotnames for HTML elements to interact with

	//images
	const body_image = document.getElementById("body_img");
	const eyes_image = document.getElementById("eyes_img");
	const mouth_image = document.getElementById("mouth_img");
	const arms_image = document.getElementById("arms_img");

	const canvas = document.getElementById("canvas_export");
	const export_img = document.getElementById("imageExport");
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

		//find the indexes of each part of the corresponding color and write those into the color arrays
		fillArraysArms();

		//Randomize initial view
		randomize();

		//Show little statistic
		var sum = body.length + eyes.length + mouth.length + arms.length;
		var variety = body.length * eyes.length * mouth.length * arms_orange.length;

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

	function fillArrayEyes(item) {
		let name = item.name;
		let url = item.url;
		eyes.push ([name, url]); //Two dimensional array, Second dimension holds name on index 0 and url at index 1
	}

	function fillArrayBody(item) {
		let name = item.name;
		let url = item.url;
		let color = item.color;
		body.push ([name, url, color]); //Two dimensional array, Second dimension holds name on index 0 and url at index 1
	}

	function fillArrayMouth(item) {
		let name = item.name;
		let url = item.url;
		mouth.push ([name, url]); //Two dimensional array, Second dimension holds name on index 0 and url at index 1
	}

	function fillArrayArms(item) {
		let name = item.name;
		let url = item.url;
		let color = item.color;
		arms.push ([name, url, color]); //Two dimensional array, Second dimension holds name on index 0 and url at index 1
	}

	function fillArraysArms() {
		for (let i=0; i<arms.length; i++){
			if (arms[i][2] == "blue" || arms[i][2] == ""){
				arms_blue.push(i);
			}

			if (arms[i][2] == "lightgrey" || arms[i][2] == ""){
				arms_lightgrey.push(i);
			}

			if (arms[i][2] == "orange" || arms[i][2] == ""){
				arms_orange.push(i);
			}

			if (arms[i][2] == "red" || arms[i][2] == ""){
				arms_red.push(i);
			}

			if (arms[i][2] == "white" || arms[i][2] == ""){
				arms_white.push(i);
			}

			if (arms[i][2] == "yellow" || arms[i][2] == ""){
				arms_yellow.push(i);
			}
		}
	}



	function onClick_body_next() {
		index_body++;

		if (index_body == body.length) {index_body = 0;} //check if index is too big for the array

		if (body[index_body][2] == "blue"){index_arms = arms_blue[index_color];}
		else if (body[index_body][2] == "lightgrey"){index_arms = arms_lightgrey[index_color];}
		else if (body[index_body][2] == "orange"){index_arms = arms_orange[index_color];}
		else if (body[index_body][2] == "red"){index_arms = arms_red[index_color];}
		else if (body[index_body][2] == "white"){index_arms = arms_white[index_color];}
		else if (body[index_body][2] == "yellow"){index_arms = arms_yellow[index_color];}

		body_image.src = "." + body[index_body][1]; //Change URL of body picture
		body_name.innerHTML = body[index_body][0]; //Change body name in controls

		arms_image.src = "." + arms[index_arms][1]; //Change URL of arms picture
		arms_name.innerHTML = arms[index_arms][0]; //Change arms name in controls
	}

	function onClick_body_prev() {
		index_body--;

		if (index_body < 0) {index_body = (body.length-1);} //check if index is too big for the array

		if (body[index_body][2] == "blue"){index_arms = arms_blue[index_color];}
		else if (body[index_body][2] == "lightgrey"){index_arms = arms_lightgrey[index_color];}
		else if (body[index_body][2] == "orange"){index_arms = arms_orange[index_color];}
		else if (body[index_body][2] == "red"){index_arms = arms_red[index_color];}
		else if (body[index_body][2] == "white"){index_arms = arms_white[index_color];}
		else if (body[index_body][2] == "yellow"){index_arms = arms_yellow[index_color];}

		body_image.src = "." + body[index_body][1]; //Change URL of body picture
		body_name.innerHTML = body[index_body][0]; //Change body name in controls

		arms_image.src = "." + arms[index_arms][1]; //Change URL of arms picture
		arms_name.innerHTML = arms[index_arms][0]; //Change arms name in controls
	}

	function onClick_eyes_next() {
		index_eyes++;

		if (index_eyes == eyes.length) {index_eyes = 0;} //check if index is too big for the array

		eyes_image.src = "." + eyes[index_eyes][1]; //Change URL of picture
		eyes_name.innerHTML = eyes[index_eyes][0]; //Change name in controls
	}

	function onClick_eyes_prev() {
		index_eyes--;

		if (index_eyes < 0) {index_eyes = (eyes.length-1);} //check if index is too big for the array

		eyes_image.src = "." + eyes[index_eyes][1]; //Change URL of picture
		eyes_name.innerHTML = eyes[index_eyes][0]; //Change name in controls
	}

	function onClick_mouth_next() {
		index_mouth++;

		if (index_mouth == mouth.length) {index_mouth = 0;} //check if index is too big for the array

		mouth_image.src = "." + mouth[index_mouth][1]; //Change URL of picture
		mouth_name.innerHTML = mouth[index_mouth][0]; //Change name in controls
	}

	function onClick_mouth_prev() {
		index_mouth--;

		if (index_mouth < 0) {index_mouth = (mouth.length-1);} //check if index is too big for the array

		mouth_image.src = "." + mouth[index_mouth][1]; //Change URL of picture
		mouth_name.innerHTML = mouth[index_mouth][0]; //Change name in controls
	}

	function onClick_arms_next() {
		index_color++;

		if (body[index_body][2] == "blue"){
			if (index_color == arms_blue.length) {index_color = 0;}
			index_arms = arms_blue[index_color];
		}
		else if (body[index_body][2] == "lightgrey"){
			if (index_color == arms_lightgrey.length) {index_color = 0;}
			index_arms = arms_lightgrey[index_color];
		}
		else if (body[index_body][2] == "orange"){
			if (index_color == arms_orange.length) {index_color = 0;}
			index_arms = arms_orange[index_color];
		}
		else if (body[index_body][2] == "red"){
			if (index_color == arms_red.length) {index_color = 0;}
			index_arms = arms_red[index_color];
		}
		else if (body[index_body][2] == "white"){
			if (index_color == arms_white.length) {index_color = 0;}
			index_arms = arms_white[index_color];
		}
		else if (body[index_body][2] == "yellow"){
			if (index_color == arms_yellow.length) {index_color = 0;}
			index_arms = arms_yellow[index_color];
		}

		arms_image.src = "." + arms[index_arms][1]; //Change URL of picture
		arms_name.innerHTML = arms[index_arms][0]; //Change name in controls
	}

	function onClick_arms_prev() {
		index_color--;

		if (body[index_body][2] == "blue"){
			if (index_color < 0) {index_color = arms_blue.length-1;}
			index_arms = arms_blue[index_color];
		}
		else if (body[index_body][2] == "lightgrey"){
			if (index_color < 0) {index_color = arms_lightgrey.length-1;}
			index_arms = arms_lightgrey[index_color];
		}
		else if (body[index_body][2] == "orange"){
			if (index_color < 0) {index_color = arms_orange.length-1;}
			index_arms = arms_orange[index_color];
		}
		else if (body[index_body][2] == "red"){
			if (index_color < 0) {index_color = arms_red.length-1;}
			index_arms = arms_red[index_color];
		}
		else if (body[index_body][2] == "white"){
			if (index_color < 0) {index_color = arms_white.length-1;}
			index_arms = arms_white[index_color];
		}
		else if (body[index_body][2] == "yellow"){
			if (index_color < 0) {index_color = arms_yellow.length-1;}
			index_arms = arms_yellow[index_color];
		}

		arms_image.src = "." + arms[index_arms][1]; //Change URL of picture
		arms_name.innerHTML = arms[index_arms][0]; //Change name in controls
	}

	function randomize() { //Randomize which parts are shown
		index_body = Math.floor(Math.random() * body.length);
		index_eyes = Math.floor(Math.random() * eyes.length);
		index_mouth = Math.floor(Math.random() * mouth.length);
		index_arms = 0;

		//Determine what color the body has and chose the arms color in the same way
		//Basically it does a random on the arms array and returns an index number with the right color for that body
		if (body[index_body][2] == "blue"){
			index_color = Math.floor(Math.random() * arms_blue.length)
			index_arms = arms_blue[index_color];
		}
		else if (body[index_body][2] == "lightgrey"){
			index_color = Math.floor(Math.random() * arms_lightgrey.length)
			index_arms = arms_lightgrey[index_color];
		}
		else if (body[index_body][2] == "orange"){
			index_color = Math.floor(Math.random() * arms_orange.length)
			index_arms = arms_orange[index_color];
		}
		else if (body[index_body][2] == "red"){
			index_color = Math.floor(Math.random() * arms_red.length)
			index_arms = arms_red[index_color];
		}
		else if (body[index_body][2] == "white"){
			index_color = Math.floor(Math.random() * arms_white.length)
			index_arms = arms_white[index_color];
		}
		else if (body[index_body][2] == "yellow"){
			index_color = Math.floor(Math.random() * arms_yellow.length)
			index_arms = arms_yellow[index_color];
		}

		body_image.src = "." + body[index_body][1];
		eyes_image.src = "." + eyes[index_eyes][1];
		mouth_image.src = "." + mouth[index_mouth][1];
		arms_image.src = "." + arms[index_arms][1];

		body_name.innerHTML = body[index_body][0];
		eyes_name.innerHTML = eyes[index_eyes][0];
		mouth_name.innerHTML = mouth[index_mouth][0];
		arms_name.innerHTML = arms[index_arms][0];
	}

	function exportImage() { //Export image so it can be saved as one PNG
		let ctx=canvas.getContext("2d");

		ctx.clearRect(0, 0, canvas.width, canvas.height);

		neomoji_name.value = body[index_body][0] + "_" + eyes[index_eyes][0] + "_" + mouth[index_mouth][0] + "_" + arms[index_arms][0]; //Set name for the emoji to use as the image name and to show as shortcode

		let body_export = new Image();
		let eyes_export = new Image();
		let mouth_export = new Image();
		let arms_export = new Image();

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
						let img = canvas.toDataURL("image/png");
						export_img.src = img;
						}
				}
			}
		};

		export_img.hidden = false;
		neomoji_name.hidden = false;
		document.getElementById("exportSaveMessage").hidden = false;
	}

	NeomojiMixer.eyes = eyes;
	NeomojiMixer.body = body;
	NeomojiMixer.mouth = mouth;
	NeomojiMixer.arms = arms;

	NeomojiMixer.arms_orange = arms_orange;
	NeomojiMixer.arms_blue = arms_blue;
	NeomojiMixer.arms_lightgrey = arms_lightgrey;
	NeomojiMixer.arms_red = arms_red;
	NeomojiMixer.arms_white = arms_white;
	NeomojiMixer.arms_yellow = arms_yellow;

	NeomojiMixer.getData = getData;
	NeomojiMixer.randomize = randomize;
	NeomojiMixer.exportImage = exportImage;

	NeomojiMixer.onClick_body_next = onClick_body_next;
	NeomojiMixer.onClick_body_prev = onClick_body_prev;
	NeomojiMixer.onClick_eyes_next = onClick_eyes_next;
	NeomojiMixer.onClick_eyes_prev = onClick_eyes_prev;
	NeomojiMixer.onClick_mouth_next = onClick_mouth_next;
	NeomojiMixer.onClick_mouth_prev = onClick_mouth_prev;
	NeomojiMixer.onClick_arms_next = onClick_arms_next;
	NeomojiMixer.onClick_arms_prev = onClick_arms_prev;

	return NeomojiMixer;
})(window.NeomojiMixer || {});


//Main Programm
document.getElementById("noJSmessage").hidden = true;
NeomojiMixer.getData();
