import subprocess
import xml.etree.ElementTree as ET
import re
import os
from dataclasses import dataclass, field

INKSCAPE_PATH = "C:\\Program Files\\Inkscape\\bin\\inkscape.com"

@dataclass
class Palette:
  fur: str
  outline: str
  paw: str
  nose: str = None
  whiskers: str = None

  def __init__(self, fur, outline, paw=None):
    self.fur = fur
    self.outline = outline
    if paw:
      self.paw = paw
    else:
      self.paw = fur


color_dict = {
    "blue": Palette("#4f8c9e","#000000"),
    "catraxx": Palette("#070362","#000000"),
    "darkbrown": Palette("#672c10","#000000"),
    "dog": Palette("#f3c07b", "#000000"),
    "frozen": Palette("#7beeff", "#2d67cc"),
    "green": Palette("#add359", "#000000"),
    "grey": Palette("#979797", "#000000"),
    "lightbrown": Palette("#ba856d", "#000000"),
    "lightgrey": Palette("#d2d0ca", "#000000"),
    "orange": Palette("#f7965b", "#000000"),
    "pink": Palette("#dea3aa", "#000000"),
    "red": Palette("#f2725a", "#000000"),
    "white": Palette("#ffffff", "#000000"),
    "wyvern": Palette("#91746e", "#000000"),
    "yellow": Palette("#ffc95c", "#000000"),
    "mouse": Palette("#e3dedb", "#000000", "#e9afaf"),
    "hairless": Palette("#e7baba", "#000000", "#e9afaf"),
    "fawn": Palette("#deb28b", "#000000", "#e9afaf"),
    "cinnamon": Palette("#b57746", "#000000", "#e9afaf"),
    "albino": Palette("#ffffff", "#000000", "#e9afaf"),
    "mouseblack": Palette("#4d5b66", "#000000", "#e9afaf"),
    "mousebrown": Palette("#6c5d53", "#000000", "#e9afaf"),
}

location = "arms"
part_name = "shocked"

with open("new_parts.txt", "w") as new_parts:
  for color, palette in color_dict.items():
      # print(f"{color}, {fill}, {stroke}")
      new_parts.write(f"""
        {{
          "name": "{part_name}",
          "url": "/parts/{location}_{part_name}_{color}.png",
          "color": "{color}"
        }},""")
      tree = ET.parse(f"high-res-parts/svg/{location}_{part_name}.svg")
      style = tree.find(".//{http://www.w3.org/2000/svg}style")
      style.text = re.sub(r"\.fur{fill:\#[0-9a-f]{3,8}}", f".fur{{fill:{palette.fur}}}", style.text)
      style.text = re.sub(r"\.outline{stroke:\#[0-9a-f]{3,8}}", f".outline{{stroke:{palette.outline}}}", style.text)
      style.text = re.sub(r"\.paw{fill:\#[0-9a-f]{3,8}}", f".paw{{fill:{palette.paw}}}", style.text)
      
      tree.write("temp.svg")
      subprocess.run(f"{INKSCAPE_PATH} .\\temp.svg --export-area-page -w 256 -h 256 --export-filename=.\\parts\\{location}_{part_name}_{color}.png")
      subprocess.run(f"{INKSCAPE_PATH} .\\temp.svg --export-area-page -w 2048 -h 2048 --export-filename=.\\high-res-parts\\{location}_{part_name}_{color}_2048.png")
      os.remove("temp.svg")
