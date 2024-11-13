import os
import re

path = "../parts/"
json = "../parts.json"

missing_file = []

file_list = os.scandir(path) #get content of that folder

try:
    with open(json, 'r') as fp:
        # read all lines in a list
        content = fp.read() #read content of that file once
except FileNotFoundError:
    print(f"Fehler: Datei '{json}' nicht gefunden.")
except json.JSONDecodeError as err:
    print(f"Fehler: Ungueltiges JSON-Format in '{json}'." + "\n" + err)

for file in file_list: #check for every file
    #print(file.name)
    if file.name not in content:
        #print(f"{file.name} not in JSON!") #if file name not found in parts.json print it
        missing_file.append(file.name)
            
        if re.search(r"\s",file.name): #Check for any white spaces in the name
            file_wo_space = re.sub(r"\s","",file.name) #Remove whitepsaces and check if the same file w/o spaces exist
            if file_wo_space in content:
                print(f"{file.name} isn't in {json}, but {file_wo_space} is. Maybe a duplicate?'")

#print(missing_file)
input("Press Enter to continue...") #Wait for [Enter] before generating JSON

for file in missing_file:
    file_parts = file.split("_")

    if file_parts[0] == "eyes":
        name = file.split(".")[0]
        name = name.replace("eyes_","")

        print("{\"name\": \"" + name + "\",\n\"url\": \"/parts/" + file + "\"},")

    elif file_parts[0] == "mouth":
        name = file.split(".")[0]
        name = name.replace("mouth_","")

        print("{\"name\": \"" + name + "\",\n\"url\": \"/parts/" + file + "\"},")

    elif file_parts[0] == "front":
        name = file.split(".")[0]
        name = name.replace("front_","")

        print("{\"name\": \"" + name + "\",\n\"url\": \"/parts/" + file + "\"},")

    elif file_parts[0] == "badge":
        name = file.split(".")[0]
        name = name.replace("badge_","")

        print("{\"name\": \"" + name + "\",\n\"url\": \"/parts/" + file + "\"},")

    elif file_parts[0] == "back":
        name = file.split(".")[0]
        name = name.replace("back_","")

        print("{\"name\": \"" + name + "\",\n\"url\": \"/parts/" + file + "\"},")

    elif file_parts[0] == "hat":
        name = file.split(".")[0]
        name = name.replace("hat_","")

        print("{\"name\": \"" + name + "\",\n\"url\": \"/parts/" + file + "\"},")

    elif file_parts[0] == "arms":
        name = file.split(".")[0]
        name = name.replace("arms_","")

        name = re.sub(r"_(?!.*_)\w*$", "", name)

        if len(file_parts) > 2:
            color = file_parts[len(file_parts)-1].split(".")[0]
        else:
            color = ""

        print("{\"name\": \"" + name + "\",\n\"url\": \"/parts/" + file + "\",\n\"color\": \"" + color + "\"},")

    else: #if its not found in anything its probably a body
        name = file.split(".")[0]
        
        print("{\"name\": \"" + name + "\",\n\"url\": \"/parts/" + file + "\",\n\"color\": \"\"},")
