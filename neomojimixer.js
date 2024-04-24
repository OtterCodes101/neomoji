const NeomojiMixer = (function(NeomojiMixer) {
	//global variables

	const color_names = [
		"blue",
		"lightgrey",
		"orange",
		"red",
		"white",
		"yellow",
		"lightbrown",
	];
	let selected_color = "blue";
	let color_change_callbacks = [];

	//shotnames for HTML elements to interact with

	const canvas = document.getElementById("canvas_export");
	const export_img = document.getElementById("imageExport");
	const neomoji_name = document.getElementById("fullNeomojiName");

	//Stats
	const stats = document.getElementById("stats");

	function onColorChange() {
		for (let i = 0; i < color_change_callbacks.length; i++) {
			if (color_change_callbacks[i]) {
				color_change_callbacks[i]();
			}
		}
	}

	function PartHandler(name) {
		this.name = name;
		this.entries = []; //Arrays to hold the parts
		this.entry_indices = []; //Maps selected_index to entries index
		this.selected_index = 0; //index_color -> arms.selected_index; index_arms -> arms.entry_indices[arms.selected_index]
		this.image_element = document.getElementById(name + "_img");
		this.name_element = document.getElementById(name + "_name");
		this.button_left = document.getElementById(name + "_left");
		this.button_right = document.getElementById(name + "_right");
	}

	PartHandler.prototype = {
		fillArray: function(item) {
			let name = item.name;
			let url = item.url;
			this.entries.push([name, url]); //Two dimensional array, Second dimension holds name on index 0 and url at index 1
		},
		fillIndices: function() {
			for (let i = 0; i < this.entries.length; i++) {
				this.entry_indices.push(i); //By default preserve index
			}
		},
		getSelectedEntry: function() {
			return this.entries[this.entry_indices[this.selected_index]];
		},
		setIndex: function(index) {
			const modulo = this.entry_indices.length; //Check if index is too big for the array
			if (!modulo) {
				this.selected_index = 0; //Error
			} else {
				index %= modulo;
				if (index < 0) {
					index += modulo;
				}
				this.selected_index = index;
			}
			this.redraw();
		},
		redraw: function() {
			const entry = this.getSelectedEntry();
			this.image_element.src = "." + entry[1]; //Change URL of picture
			//Change name in controls
			this.updateOptions();
			this.name_element.selectedIndex = this.selected_index;
		},
		onClickNext: function() {
			this.setIndex(this.selected_index + 1);
		},
		onClickPrev: function() {
			this.setIndex(this.selected_index - 1);
		},
		onChangeDropdown: function() {
			this.setIndex(this.name_element.selectedIndex);
		},
		activateControls: function() {
			this.button_left.disabled = false;
			this.button_right.disabled = false;
			this.name_element.disabled = false;
		},
		randomize: function() {
			this.setIndex(Math.floor(Math.random() * this.entry_indices.length));
		},
		createExportImage: function() {
			const entry = this.getSelectedEntry();
			let img = new Image();
			img.src = "." + entry[1];
			return img;
		},
		updateOptions: function() {
			const options = this.name_element.options;
			for (let i = 0; i < this.entry_indices.length; i++) {
				const index = this.entry_indices[i];
				const entry = this.entries[index];
				if (options.length > i && options[i].value == entry[0]) {
					continue;
				} else {
					const option = new Option(entry[0], entry[0], false, this.selected_index == i);
					if (this.name_element.length <= i) {
						this.name_element.add(option);
					} else {
						this.name_element.remove(i);
						this.name_element.add(option, i);
					}
				}
			}
		},
	};

	function ColoredPartHandler(name) {
		PartHandler.call(this, name);
		//For all the different colours of the arms there will be each a own array
		this.colored_indices = Object.create(null);
		for (let i = 0; i < color_names.length; i++) {
			this.colored_indices[color_names[i]] = [];
		}
		this.entry_indices = this.colored_indices[selected_color];
		const that = this;
		color_change_callbacks.push(function() {
			that.onColorChange();
		});
	}

	ColoredPartHandler.prototype = Object.assign(Object.create(PartHandler.prototype), {
		constructor: PartHandler,
		fillArray: function(item) {
			let name = item.name;
			let url = item.url;
			let color = item.color;
			this.entries.push([name, url, color]); //Two dimensional array, Second dimension holds name on index 0, url at index 1, and color at index 2
		},
		fillIndices: function() {
			for (let i = 0; i < this.entries.length; i++) {
				const color = this.entries[i][2];
				if (color == "") {
					//All colors
					for (let j in this.colored_indices) {
						this.colored_indices[j].push(i);
					}
				} else {
					const indices = this.colored_indices[color];
					if (indices == undefined) {
						console.log("Cannot register " + this.name + " with unknown color: " + color);
					} else {
						indices.push(i);
					}
				}
			}
		},
		onColorChange: function() {
			this.entry_indices = this.colored_indices[selected_color];
			this.redraw();
		},
	});

	function BodyPartHandler(name) {
		PartHandler.call(this, name);
	}

	BodyPartHandler.prototype = Object.assign(Object.create(PartHandler.prototype), {
		constructor: PartHandler,
		fillArray: ColoredPartHandler.prototype.fillArray,
		setIndex: function(index) {
			const modulo = this.entry_indices.length; //Check if index is too big for the array
			if (!modulo) {
				this.selected_index = 0; //Error
			} else {
				index %= modulo;
				if (index < 0) {
					index += modulo;
				}
				this.selected_index = index;
			}
			this.redraw();
			const entry = this.getSelectedEntry();
			selected_color = entry[2]; //Global
			onColorChange(); //Global
		},
	});

	const part_handlers = {
		body: new BodyPartHandler("body"),
		eyes: new PartHandler("eyes"),
		mouth: new PartHandler("mouth"),
		arms: new ColoredPartHandler("arms"),
	};


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
		for (const i in part_handlers) {
			parts.type[i].forEach(function(p) {part_handlers[i].fillArray(p);});
		}

		//find the indexes of each part of the corresponding color and write those into the color arrays
		for (const i in part_handlers) {
			part_handlers[i].fillIndices();
		}

		//Randomize initial view
		randomize();

		// If there was a hash, restore as a direct permalink.
		if (document.location.hash != "") {
			loadFromHash(document.location.hash);
		}
		window.addEventListener("hashchange", () => {
			loadFromHash(document.location.hash);
		});

		//Show little statistic
		var sum = 0;
		var variety = 1;
		for (const i in part_handlers) {
			sum += part_handlers[i].entries.length;
			variety *= part_handlers[i].entry_indices.length;
		}

		stats.innerHTML = "There are " + sum + " Elements available,<br />with " + new Intl.NumberFormat("de-DE").format(variety) + " possible combinations.";

		//Activate the buttons after everything is loaded in
		for (const i in part_handlers) {
			part_handlers[i].activateControls();
		}
		document.getElementById("random").disabled = false;
		document.getElementById("export").disabled = false;

	}

	function loadFromHash(hash) {
		let parts = hash
			.slice(1) // the first character is always the '#' sign
			.split('+');

		// define a constant order for the parts to appear in the hash
		const parts_order = ["body", "eyes", "mouth", "arms"];

		if (parts.length == parts_order.length) {
			// convert the part names to part indices
			parts = parts.map((name, i) =>
				Array.from(part_handlers[parts_order[i]].name_element.options).findIndex(x => x.value === name)
			);
			if (parts.every(x => x != -1)) {
				// all part names were found
				parts.forEach((part_index, i) => part_handlers[parts_order[i]].setIndex(part_index));
			}
		}
	}

	function randomize() { //Randomize which parts are shown
		for (const i in part_handlers) {
			part_handlers[i].randomize();
		}
	}

	function exportImage() { //Export image so it can be saved as one PNG
		let ctx=canvas.getContext("2d");

		ctx.clearRect(0, 0, canvas.width, canvas.height);

		//Set name for the emoji to use as the image name and to show as shortcode
		neomoji_name.innerText = part_handlers.body.getSelectedEntry()[0] + "_" + part_handlers.eyes.getSelectedEntry()[0] + "_" + part_handlers.mouth.getSelectedEntry()[0] + "_" + part_handlers.arms.getSelectedEntry()[0];
		neomoji_name.href = new URL("#" + part_handlers.body.getSelectedEntry()[0] + "+" + part_handlers.eyes.getSelectedEntry()[0] + "+" + part_handlers.mouth.getSelectedEntry()[0] + "+" + part_handlers.arms.getSelectedEntry()[0], document.location.href)

		let export_layers = [
			part_handlers.body.createExportImage(),
			part_handlers.eyes.createExportImage(),
			part_handlers.mouth.createExportImage(),
			part_handlers.arms.createExportImage(),
		];

		function layerCallback() {
			while (export_layers.length) {
				const layer = export_layers[0];
				if (!layer.complete) {
					layer.onload = layerCallback;
					return; //Wait to load
				}
				//Finished waiting
				export_layers.shift()
				ctx.drawImage(layer, 0, 0, 256, 256);
			}
			let img = canvas.toDataURL("image/png");
			export_img.src = img;
		}

		setTimeout(layerCallback, 0); //Run asynchronously

		export_img.hidden = false;
		neomoji_name.hidden = false;
		document.getElementById("exportSaveMessage").hidden = false;
	}

	NeomojiMixer.PartHandler = PartHandler;
	NeomojiMixer.ColoredPartHandler = ColoredPartHandler;
	NeomojiMixer.BodyPartHandler = BodyPartHandler;

	NeomojiMixer.color_names = color_names;
	NeomojiMixer.color_change_callbacks = color_change_callbacks;
	NeomojiMixer.part_handlers = part_handlers;
	NeomojiMixer.onColorChange = onColorChange;
	NeomojiMixer.getData = getData;
	NeomojiMixer.loadParts = loadParts;
	NeomojiMixer.randomize = randomize;
	NeomojiMixer.exportImage = exportImage;
	NeomojiMixer.canvas = canvas;
	NeomojiMixer.export_img = export_img;
	NeomojiMixer.neomoji_name = neomoji_name;
	NeomojiMixer.stats = stats;

	Object.defineProperty(NeomojiMixer, 'selected_color', {
		enumerable: true,
		configurable: true,
		get: function() {
			return selected_color;
		},
		set: function(value) {
			selected_color = value;
			onColorChange();
		},
	});

	return NeomojiMixer;
})(window.NeomojiMixer || {});


//Main Programm
document.getElementById("noJSmessage").hidden = true;
NeomojiMixer.getData();
