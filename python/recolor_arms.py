import subprocess
import xml.etree.ElementTree as ET
import re
import os

INKSCAPE_PATH = "C:\\Program Files\\Inkscape\\bin\\inkscape.com"

color_dict = {
    "blue": ("#4f8c9e","#000000"),
    "catraxx": ("#070362","#000000"),
    "darkbrown": ("#672c10","#000000"),
    "dog": ("#f3c07b", "#000000"),
    "frozen": ("#7beeff", "#2d67cc"),
    "green": ("#add359", "#000000"),
    "grey": ("#979797", "#000000"),
    "lightbrown": ("#ba856d", "#000000"),
    "lightgrey": ("#d2d0ca", "#000000"),
    "orange": ("#f7965b", "#000000"),
    "pink": ("#dea3aa", "#000000"),
    "red": ("#f2725a", "#000000"),
    "white": ("#ffffff", "#000000"),
    "wyvern": ("#91746e", "#000000"),
    "yellow": ("#ffc95c", "#000000")
}

part_name = "arms_megaphone"

for color, (fill, stroke) in color_dict.items():
    # print(f"{color}, {fill}, {stroke}")
    print(f"""      {{
        "name": "{part_name}",
        "url": "/parts/{part_name}_{color}.png",
        "color": "{color}"
      }},""")
    tree = ET.parse(f"high-res-parts/svg/{part_name}.svg")
    style = tree.find(".//{http://www.w3.org/2000/svg}style")
    style_text = re.sub("fill:#4f8c9e;stroke:#000", f"fill:{fill};stroke:{stroke}", style.text)
    style.text = style_text

    tree.write("temp.svg")
    subprocess.run(f"{INKSCAPE_PATH} .\\temp.svg --export-area-page -w 256 -h 256 --export-filename=.\\parts\\{part_name}_{color}.png", capture_output=True)
    subprocess.run(f"{INKSCAPE_PATH} .\\temp.svg --export-area-page -w 2048 -h 2048 --export-filename=.\\high-res-parts\\{part_name}_{color}.png", capture_output=True)
    os.remove("temp.svg")
