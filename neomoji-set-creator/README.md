## Set creator for neomojimixer

Hello! This is a little tool to help you bulk export your neomoji. It's made up of three parts.

### presets.json
This file defines emojis to then be exported. Each emoji is given a name and then parts for that emoji to be made of. The complete list of parts can be found at [neomojimixer.com/list](https://neomojimixer.com/list) or you can view just parts of a certain kind eg [neomojimixer.com/list/eyes](https://neomojimixer.com/list/eyes). More info on this can be found on the [API docs](https://neomojimixer.com/api-doc)

Here's an example emoji preset:
```json
"pensive_cowboy": {
  "mouth": "meh",
  "eyes": "pensive",
  "hat": "cowboy"
}
```

### sets.json
Here is where the sets of emoji you wish to export are defined. Each set is given a name, body to use and then a list of emoji to export. This example will make a pack called neofox, using the body neofox and export all the emoji in presets.json

```json
"neofox": {
    "body": "neofox",
    "emoji": true
}
```

If I wanted to export only a few specific emoji I could do something like this:

```json
"neootter_signs": {
  "body": "neootter",
  "emoji": [
    "sign_yes", "sign_no"
  ]
}
```

### set-creator.py
This is the script that takes the json files and spits out the emoji we want. To run it you need to have a version of [python 3](https://www.python.org/downloads/) installed. 

Open a commandline in this folder (neomoji-set-creator) and run `python3 set-creator.py`. 

You will see messages in the console as each emoji is made and if something goes wrong instead an error will be printed saying what went wrong.

That's it! There should now be folders full of beautiful emoji for you to do with what you wish 😊