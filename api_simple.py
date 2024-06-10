import json
import random
from flask import Flask, request, send_file, g, jsonify
from PIL import Image, ExifTags
from io import BytesIO
from jsonpath import JSONPath
from dataclasses import dataclass
from enum import StrEnum
from datetime import datetime

app = Flask(__name__)

def get_src_parts():
    if "src_parts" not in g:
        g.src_parts = {}
        with open("parts.json") as parts_file:
            g.src_parts = json.load(parts_file)
            
    return g.src_parts

Level = StrEnum("LEVELS", ["BODY", "EYES", "HAT", "MOUTH", "ARMS", "FRONT"])

@dataclass
class Layer:
    name: str
    level: Level
    url: str
    variant: str|None

    def __init__(self, level: Level, name: str, variant:str=None):
        self.name = name
        self.level = level
        self.variant = variant
        if not variant:
            part_data = JSONPath(f'$.type.{self.level}[?(@.name=="{self.name}")]').parse(get_src_parts())[0]
            self.url = part_data["url"]
        else:
            part_data = JSONPath(f'$.type.{self.level }[?(@.name=="{self.name}" and @.color=="{variant}")]').parse(get_src_parts())[0]
            self.url = part_data["url"]
        self._image = Image.open(f"./{self.url}").convert("RGBA")

    def render(self) -> Image:
        return self._image

class BlankLayer(Layer):
    def __init__(self, level: Level):
        self.name = "blank"
        self.level = level
        self.url = None

    def render(self) -> Image:
        return Image.new("RGBA", (256, 256), "#00000000")


@dataclass
class Neomoji:
    layers: list[Layer]
    color: str = None
    author: str|None = None
    render: Image = None
    exif: Image.Exif = None

    def add_layer(self, level:str, part_name:str) -> None:
        source_part = JSONPath(f'$.type.{level}[?(@.name=="{part_name}")]').parse(get_src_parts())
        variant_count = len(source_part)
        new_layer = None
        if variant_count == 0:
            print(f"Error: {level} doesn't have {part_name}")
            self.layers.append(BlankLayer(Level[level.upper()]))
            return
        elif variant_count == 1:
            new_layer = Layer(Level[level.upper()], part_name)
        else:
            new_layer = Layer(Level[level.upper()], part_name, self.color)
        
        self.layers.append(new_layer)

        if Level[level.upper()] == Level.BODY:
            self.color = source_part[0]["color"]

    def compile_image(self) -> None:
        out_image = Image.new("RGBA", (256, 256), "#0000")
        for l in self.layers:
            out_image =  Image.alpha_composite(out_image, l.render())
        self.render = out_image

    def add_exif(self) -> None:
        self.exif = self.render.getexif()
        self.exif[ExifTags.Base.Software] = "Neomoji Mixer"
        self.exif[ExifTags.Base.Copyright] = "CC BY-NC-SA 4.0"
        self.exif[ExifTags.Base.ImageDescription] = " ".join([l.name.capitalize() for l in self.layers])
        self.exif[ExifTags.Base.DateTime] = f"{datetime.now():%Y-%m-%d %H:%I:%S}"
        if self.author:
            self.exif[ExifTags.Base.Artist] = f"Image creator, {self.author}"

    def export(self) -> BytesIO:
        img_io = BytesIO()
        self.render.save(img_io, 'PNG', exif=self.exif)
        img_io.seek(0)
        return img_io

    def get_filename(self) -> str:
        return "_".join([l.name for l in self.layers])+".png"

    def __init__(self):
        self.layers = []
        self.color = None
        self.render = None

@app.route("/create", methods=["GET", "POST", ])
def handle_create(specification:dict=None):
    if not specification:
        specification = {l: None for l in Level}
        if request.is_json:
            for l in Level:
                try:
                    specification[l] = str(request.json[l])
                except (TypeError, KeyError):
                    pass
        else:
            for l in Level:
                try:
                    specification[l] = str(request.args[l])
                except (TypeError, KeyError):
                    pass
    
    n = Neomoji()
    for l in Level:
        n.add_layer(l, specification[l])

    try:
        n.author = specification["author"]
    except KeyError:
        n.author = None
    n.compile_image()
    n.add_exif()
    stream = n.export()
    return send_file(
        stream, 
        mimetype='image/png',
        as_attachment=True, 
        download_name=n.get_filename()
    )

@app.route("/create/random", methods=["GET", "POST"])
def handle_create_random():
    random_spec = {}
    try:
        random_spec["author"] = request.args["author"]
    except KeyError:
        pass
    blank_chance = {
        Level.BODY: 0,
        Level.EYES: 0.01,
        Level.MOUTH: 0.01,
        Level.ARMS: 0.5,
        Level.HAT: 0.75,
        Level.FRONT: 0.95
    }
    for l in Level:
        if blank_chance[l] < random.random():
            parts = JSONPath(f'$.type.{l}[*][name]').parse(get_src_parts())
            random_spec[l] = random.choice(parts)
    return handle_create(random_spec)

@app.route("/list", methods=["GET","POST"])
def handle_parts_list():
    out_dict = {}
    for part_level in Level:
        level_list = set()
        for part in get_src_parts()["type"][part_level]:
            level_list.add(part["name"])
        out_dict[part_level] = sorted([l for l in level_list])
    return jsonify(out_dict)

@app.route("/list/<level>", methods=["GET", "POST"])
def handle_parts_category(level:str):
    out_dict = {}
    match(level):
        case Level.BODY:
            print("body")
            for part in get_src_parts()["type"][level]:
                out_dict[part["name"]] = {"color": part["color"]}
        case Level.ARMS:
            print("arms")
            for part in get_src_parts()["type"][level]:
                try:
                    out_dict[part["name"]]["variants"].append(part["color"])
                except KeyError:
                    if len(part["color"]) == 0:
                        out_dict[part["name"]] = {}
                    else:
                        out_dict[part["name"]] = {"variants": [part["color"], ]}
        case _:
            print("default")
            for part in get_src_parts()["type"][level]:
                out_dict[part["name"]] = {}
    return jsonify(out_dict)

@app.route("/part/<level>/<name>", methods=["GET", "POST"])
def handle_part_image(level:str, name:str):
    part = JSONPath(f'$.type.{level}[?(@.name=="{name}")]').parse(get_src_parts())[0]
    stream = open(f"./{part["url"]}", "rb")
    return send_file(
        stream, 
        mimetype='image/png',
        as_attachment=False, 
        download_name=f"{level}_{name}.png"
    )

@app.route("/part/<level>/<name>/<variant>", methods=["GET", "POST"])
def handle_part_image_variant(level:str, name:str, variant:str):
    part = JSONPath(f'$.type.{level}[?(@.name=="{name}" and @.color=="{variant}")]').parse(get_src_parts())[0]
    stream = open(f"./{part["url"]}", "rb")
    return send_file(
        stream, 
        mimetype='image/png',
        as_attachment=False, 
        download_name=f"{level}_{name}_{variant}.png"
    )