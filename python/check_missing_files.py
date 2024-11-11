import os
import json

filepath = "../parts.json"

try:
    with open(filepath, 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Fehler: Datei '{filepath}' nicht gefunden.")
except json.JSONDecodeError:
    print(f"Fehler: Ungueltiges JSON-Format in '{filepath}'.")

for second_level in data['type']:
    #for item in data['type'][second_level]:
        #if not os.path.exists(".." + item['url']):
            #print(f"{item['url']} doesn't exist!")

    for i, item in enumerate(data['type'][second_level]):  # Add index i
        if not os.path.exists(".." + item['url']):
            line_number = 0  # Initialize line number
            try:
                with open(filepath, 'r') as f:
                    for j, line in enumerate(f, 1):  # Iterate through the file line by line
                        if item['url'] in line:  # Search for the URL in the line
                            line_number = j
                            break  # Exit the inner loop once the URL is found
            except FileNotFoundError:
                pass  # Error already handled above

            print(f"{item['url']} doesn't exist! (Line {line_number} in JSON)")  # Print line number