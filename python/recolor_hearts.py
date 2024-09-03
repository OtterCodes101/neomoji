import subprocess
import xml.etree.ElementTree as ET
import re
import os
import json
from glob import glob

INKSCAPE_PATH = "C:\\Program Files\\Inkscape\\bin\\inkscape.com"

def as_palette(contents):
  dct = dict(contents)
  if "outline" not in dct:
    dct["outline"] = "#000000"
  if "paw" not in dct:
    dct["paw"] = dct["fur"]
  if "hand" not in dct:
    dct["hand"] = dct["paw"]
  return dct

color_dict = {}
with open("colors.json") as cd:
  color_dict = {k:as_palette(v) for k,v in json.load(cd).items()}

location = "arms"
heart_color_list = [
  ("blue", "#72abeb", "#104989"),
  ("cyan", "#4ac5c9", "#00595c"),
  ("gray", "#a1a1a1", "#3f3f3f"),
  ("green", "#75c750", "#1d5d00"),
  ("orange", "#ea9e6b", "#b05e28"),
  ("pink", "#ff8aa3", "#cc4561"),
  ("purple", "#d875f6", "#761394"),
  ("red", "#ff7a77", "#c70500"),
  ("yellow", "#c7ac00", "#4e4300")
]

tree = ET.parse(f"high-res-parts/svg/arms_heart.svg")
for heart_color, heart_inner, heart_outer in heart_color_list:
  for color, palette in color_dict.items():
    print(f"Needs to be made: .\\parts\\arms_{heart_color}_heart_{color}.png")
    style = tree.find(".//{http://www.w3.org/2000/svg}style")
    style.text = re.sub(r"\.fur{fill:\#[0-9a-f]{3,8}}", f".fur{{fill:{palette["fur"]}}}", style.text)
    style.text = re.sub(r"\.outline{stroke:\#[0-9a-f]{3,8}}", f".outline{{stroke:{palette["outline"]}}}", style.text)
    style.text = re.sub(r"\.paw{fill:\#[0-9a-f]{3,8}}", f".paw{{fill:{palette["paw"]}}}", style.text)
    style.text = re.sub(r"\.hand{fill:\#[0-9a-f]{3,8}}", f".hand{{fill:{palette["hand"]}}}", style.text)
    style.text = re.sub(r"#inner_heart{fill:\#[0-9a-f]{3,8}}", f"#inner_heart{{fill:{heart_inner}}}", style.text)
    style.text = re.sub(r"#outer_heart{fill:\#[0-9a-f]{3,8}}", f"#outer_heart{{fill:{heart_outer}}}", style.text)
    
    tree.write("temp.svg")
    subprocess.run(f"{INKSCAPE_PATH} .\\temp.svg --export-area-page -w 256 -h 256 --export-filename=.\\parts\\arms_{heart_color}_heart_{color}.png")
    subprocess.run(f"{INKSCAPE_PATH} .\\temp.svg --export-area-page -w 2048 -h 2048 --export-filename=.\\high-res-parts\\arms_{heart_color}_heart_{color}_2048.png")
    os.remove("temp.svg")

    with open("new_parts.txt", "a") as new_parts:
        new_parts.write(f"""
      {{
        "name": "{heart_color}_heart",
        "url": "/parts/arms_{heart_color}_heart_{color}.png",
        "color": "{color}"
      }},""")
