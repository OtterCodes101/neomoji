import os

path = "../parts/"
json = "../parts.json"

file_list = os.scandir(path) #get content of that folder

i = 1

with open(json, 'r') as fp:
    # read all lines in a list
    content = fp.read() #read content of that file once

    for file in file_list: #check for every file
        i += 1
        #print(file.name)

        if file.name not in content:
            print(f"{file.name} not in JSON!") #if file name not found in parts.json print it

#TODO generate valid JSON to copy and paste it into parts.json
        
