import urllib.request
import json
from os import path
from os import makedirs


# Set to true to write over already created emoji
rewrite = True

server = "https://neomojimixer.com/create"

sets_file = open("sets.json")
sets = json.load(sets_file)

presets_file = open("presets.json")
presets = json.load(presets_file)

# Makes sure a folder exists and creates it if it doesn't
def ensure_folder(folder_path):
    if not path.isdir(folder_path) and not path.exists(folder_path):
        makedirs(folder_path)

# Turn emoji json to query strings for the API
def json_to_qs(json_object):
    qs="?"

    for part in json_object:
        qs += f"{part}={json_object[part]}&"
        
    # return qs minus last &
    return qs[:-1]
    
for emoji_set in sets:
    body = sets[emoji_set]["body"]
    # Make sure the output folder exists
    ensure_folder(emoji_set)
    
    # If this pack has all emoji enabled
    if sets[emoji_set]["emoji"] == True:
        # Replace true with all the emoji in presets
        sets[emoji_set]["emoji"] = presets.keys()
    
    for emoji_to_make in sets[emoji_set]["emoji"]:
        
        # If we're not rewriting emoji
        if not rewrite:
            # And the emoji exists already
            if path.exists(f"{emoji_set}/{emoji_set}_{emoji_to_make}.png"):
                # Skip this emoji
                continue
        
        # Set the body of this preset
        presets[emoji_to_make]["body"] = body
        # Turn the json into a query string and slap it on the end of the server address
        request_url = server + json_to_qs(presets[emoji_to_make])
        try:
            emoji_out = urllib.request.urlretrieve(url=request_url, filename=f"{emoji_set}/{emoji_set}_{emoji_to_make}.png")
            print(f"Made {emoji_set}/{emoji_set}_{emoji_to_make}.png")
        except urllib.error.HTTPError as e:
            print(f"Error while making {emoji_set}/{emoji_set}_{emoji_to_make}.png")
            print(presets[emoji_to_make])
            print(e)