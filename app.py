from flask import Flask, request, send_file, g, jsonify
from PIL import Image, ExifTags
from io import BytesIO
import json
from jsonpath import JSONPath
from dataclasses import dataclass
from enum import StrEnum
from datetime import datetime
import random

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

    def rotate(self, degrees:float):
        x0, y0, x1, y1 = self._image.getbbox()
        center_x = (x0 + x1)//2
        center_y = (y0 + y1)//2
        self._image = self._image.rotate(degrees, expand=0, center=(center_x, center_y))

    def move(self, x:float, y:float):
        self._image = self._image.transform(
            size = self._image.size,
            method = Image.AFFINE,
            data = (1, 0, x, 0, 1, y),
            fill = 1,
            fillcolor = "#00000000"
        )

    def flip(self, in_place:bool=False):
        if in_place:
            x0, y0, x1, y1 = self._image.getbbox()
            old_center_x = (x0 + x1)//2
            old_center_y = (y0 + y1)//2
        self._image = self._image.transform(
            size = self._image.size,
            method = Image.AFFINE,
            data = (1, 0, 0, 0, -1, 256),
            fill = 1,
            fillcolor = "#00000000"
        )
        if in_place:
            x0, y0, x1, y1 = self._image.getbbox()
            new_center_x = (x0 + x1)//2
            new_center_y = (y0 + y1)//2
            self.move(new_center_x-old_center_x, new_center_y-old_center_y)

    def mirror(self, in_place:bool=False):
        if in_place:
            x0, y0, x1, y1 = self._image.getbbox()
            old_center_x = (x0 + x1)//2
            old_center_y = (y0 + y1)//2
        self._image = self._image.transform(
            size = self._image.size,
            method = Image.AFFINE,
            data = (-1, 0, 256, 0, 1, 0),
            fill = 1,
            fillcolor = "#00000000"
        )
        if in_place:
            x0, y0, x1, y1 = self._image.getbbox()
            new_center_x = (x0 + x1)//2
            new_center_y = (y0 + y1)//2
            self.move(new_center_x-old_center_x, new_center_y-old_center_y)

    def render(self) -> Image:
        return self._image

class BlankLayer(Layer):
    def __init__(self, level: Level):
        self.name = "blank"
        self.level = level
        self.url = None

    def rotate(self, degrees:float):
        pass

    def move(self, x:float, y:float):
        pass

    def flip(self, in_place:bool=False):
        pass

    def mirror(self, in_place:bool=False):
        pass

    def render(self) -> Image:
        return Image.new("RGBA", (256, 256), "#00000000")


@dataclass
class Neomoji:
    layers: list[Layer]
    color: str = None
    author: str|None = None
    render: Image = None
    exif: Image.Exif = None

    def add_layer(self, level:str, specification:dict|str|None):
        if level not in specification.keys():
            self.layers.append(BlankLayer(Level[level.upper()]))
            if Level[level.upper()] == Level.BODY:
                self.color = "yellow"
            return

        if not specification[level]:
            self.layers.append(BlankLayer(Level[level.upper()]))
            if Level[level.upper()] == Level.BODY:
                self.color = "yellow"
            return

        if isinstance(specification[level], str):
            part_name = specification[level]
        elif "part" in specification[level].keys():
            part_name = specification[level]["part"]
        else:
            print(f"Error: {level} is a dict but doesn't have a part")
            self.layers.append(BlankLayer(Level[level.upper()]))
            if Level[level.upper()] == Level.BODY:
                self.color = "yellow"
            return
        
        source_part = JSONPath(f'$.type.{level}[?(@.name=="{part_name}")]').parse(get_src_parts())
        variant_count = len(source_part)
        if variant_count == 0:
            print(f"Error: {level} doesn't have {part_name}")
            self.layers.append(BlankLayer(Level[level.upper()]))
        elif variant_count == 1:
            new_layer = Layer(Level[level.upper()], part_name)
        else:
            if "variant" in specification[level]:
                new_layer = Layer(Level[level.upper()], part_name, specification[level]["variant"])
            else:
                new_layer = Layer(Level[level.upper()], part_name, self.color)

        if "mirror" in specification[level]:
            try:
                new_layer.mirror(specification[level]["mirror"]["in_place"])
            except TypeError:
                new_layer.mirror()

        if "flip" in specification[level]:
            try:
                new_layer.flip(specification[level]["flip"]["in_place"])
            except TypeError:
                new_layer.flip()

        if "rotate" in specification[level]:
            new_layer.rotate(specification[level]["rotate"])

        if "move" in specification[level]:
            new_layer.move(*specification[level]["move"])
        
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
        if request.is_json:
            specification = request.json
        else:
            specification = request.args
    
    n = Neomoji()
    for l in Level:
        n.add_layer(l, specification)

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
        Level.EYES: 0,
        Level.MOUTH: 0,
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