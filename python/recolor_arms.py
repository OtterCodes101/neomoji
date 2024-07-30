import subprocess
import xml.etree.ElementTree as ET
import re
import os
import json

INKSCAPE_PATH = "C:\\Program Files\\Inkscape\\bin\\inkscape.com"

def as_palette(contents):
  dct = dict(contents)
  # print(dct)
  if "paw" not in dct:
    dct["paw"] = dct["fur"]
  if "outline" not in dct:
    dct["outline"] = "#000000"
  return dct

color_dict = {}
with open("colors.json") as cd:
  color_dict = {k:as_palette(v) for k,v in json.load(cd).items()}

location = "arms"
part_name = "feed_baby"

with open("new_parts.txt", "w") as new_parts:
  for color, palette in color_dict.items():
    new_parts.write(f"""
      {{
        "name": "{part_name}",
        "url": "/parts/{location}_{part_name}_{color}.png",
        "color": "{color}"
      }},""")

for color, palette in color_dict.items():
    print(f"{color}")
    tree = ET.parse(f"high-res-parts/svg/{location}_{part_name}.svg")
    style = tree.find(".//{http://www.w3.org/2000/svg}style")
    style.text = re.sub(r"\.fur{fill:\#[0-9a-f]{3,8}}", f".fur{{fill:{palette["fur"]}}}", style.text)
    style.text = re.sub(r"\.outline{stroke:\#[0-9a-f]{3,8}}", f".outline{{stroke:{palette["outline"]}}}", style.text)
    style.text = re.sub(r"\.paw{fill:\#[0-9a-f]{3,8}}", f".paw{{fill:{palette["paw"]}}}", style.text)
    
    tree.write("temp.svg")
    subprocess.run(f"{INKSCAPE_PATH} .\\temp.svg --export-area-page -w 256 -h 256 --export-filename=.\\parts\\{location}_{part_name}_{color}.png")
    subprocess.run(f"{INKSCAPE_PATH} .\\temp.svg --export-area-page -w 2048 -h 2048 --export-filename=.\\high-res-parts\\{location}_{part_name}_{color}_2048.png")
    os.remove("temp.svg")
