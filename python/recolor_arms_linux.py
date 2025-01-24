import subprocess
import xml.etree.ElementTree as ET
import re
import os
import json
from glob import glob

INKSCAPE_PATH = "inkscape"

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
with open("../colors.json") as cd:
  color_dict = {k:as_palette(v) for k,v in json.load(cd).items()}

location = "arms"
sub_path = "arms/"
part_list = []
for file in glob(r"../high-res-parts/svg/arms_*"):
  part_list.append(re.match(r".*/arms_(.*)\.svg", file).groups()[0])

print("Found arm files:", part_list)  # Debug output

# part_list = [p for p in part_list if p <= "sign_alt_text" and p > "keyboard"]
# part_list = ["guitar", ] 

for part_name in part_list:
  for color, palette in ((k, color_dict[k]) for k in ("pig", )):
  #for color, palette in color_dict.items():

    # if os.path.isfile(f"./parts/{location}_{part_name}_{color}.png"):
    #   print(f"Already exists: ./parts/{location}_{part_name}_{color}.png")
    #   continue
    # else:
    print(f"Needs to be made: ../parts/{location}_{part_name}_{color}.png")
    tree = ET.parse(f"../high-res-parts/svg/{location}_{part_name}.svg")
    style = tree.find(".//{http://www.w3.org/2000/svg}style")
    
    # Skip if no style element or no text content
    if style is None or style.text is None:
        print(f"Skipping {part_name} - no style element or text content found")
        continue
        
    style.text = re.sub(r"\.fur{fill:\#[0-9a-f]{3,8}}", f".fur{{fill:{palette['fur']}}}", style.text)
    style.text = re.sub(r"\.outline{stroke:\#[0-9a-f]{3,8}}", f".outline{{stroke:{palette['outline']}}}", style.text)
    style.text = re.sub(r"\.paw{fill:\#[0-9a-f]{3,8}}", f".paw{{fill:{palette['paw']}}}", style.text)
    style.text = re.sub(r"\.hand{fill:\#[0-9a-f]{3,8}}", f".hand{{fill:{palette['hand']}}}", style.text)
    
    tree.write("temp.svg")
    subprocess.run([
        INKSCAPE_PATH,
        "temp.svg",
        "--export-area-page",
        "-w", "256",
        "-h", "256",
        f"--export-filename=../parts/{location}_{part_name}_{color}.png"
    ])
    subprocess.run([
        INKSCAPE_PATH,
        "temp.svg",
        "--export-area-page",
        "-w", "2048",
        "-h", "2048",
        f"--export-filename=../high-res-parts/{sub_path}{location}_{part_name}_{color}_2048.png"
    ])
    os.remove("temp.svg")

    with open("new_parts.txt", "a") as new_parts:
        new_parts.write(f"""
      {{
        "name": "{part_name}",
        "url": "/parts/{location}_{part_name}_{color}.png",
        "color": "{color}"
      }},""")
