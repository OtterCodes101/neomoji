import os
import json
import random
from telnetlib import DO
from PIL import Image

import sys


with open('../parts.json', 'r') as f:
  data = json.load(f)

#no Arms because that made the favicon very noisy
eyes = []
mouth = []
bodies = []
arms = []
hat = []
front = []
badge = []
back = []
images = []

print('Loading file path of eyes, mouth, bodies, etc...')

#Extracting only the URLs in list for all three body parts
for eye in data['type']['eyes']:
    eyes.append(eye['url'])

for mund in data['type']['mouth']:
    mouth.append(mund['url'])

for hut in data['type']['hat']:
    hat.append(hut['url'])

for deko in data['type']['front']:
    front.append(deko['url'])

for badges in data['type']['badge']:
    badge.append(badges['url'])

for background in data['type']['back']:
    back.append(background['url'])

for body in data['type']['body']:
    bodies.append([body['url'], body['color']])

for arm in data['type']['arms']:
    arms.append([arm['url'], arm['color']])


print ("Generating 300 pictures...")
for i in range(300):
    color_arms = []
    skip_element = 100

    print(f"Generating image #{i}", end='\r')

    if i > 1:
        skip_element = random.randint(0,7)

    if skip_element != 2:
        chosen_body = random.choice(bodies)

    for item in arms:
        if item[1] == chosen_body[1]:
            if os.path.exists(".." + item[0]): #Check if arms really exist if not, don't add it to the array
                color_arms.append(item[0])

    if skip_element != 3:
        arms_url = random.choice(color_arms)
        index_arms = color_arms.index(arms_url)
    else:
        if index_arms > len(color_arms)-1: #If the arms in that colour doesn't exist yet, just chose one available by random
            index_arms = random.randint(0,len(color_arms)-1)
            
        arms_url=color_arms[index_arms]

    if skip_element != 0:
        image_eye = Image.open("../"+random.choice(eyes)).convert("RGBA")

    if skip_element != 1:
        image_mouth = Image.open("../"+random.choice(mouth)).convert("RGBA")

    if skip_element != 4:
        image_hat = Image.open("../"+random.choice(hat)).convert("RGBA")

    if skip_element != 5:
        image_front = Image.open("../"+random.choice(front)).convert("RGBA")

    if skip_element != 6:
        image_badge = Image.open("../"+random.choice(badge)).convert("RGBA")

    if skip_element != 7:
        image_back = Image.open("../"+random.choice(back)).convert("RGBA")

    image_bodies = Image.open("../"+chosen_body[0]).convert("RGBA")

    image_arms = Image.open("../"+arms_url).convert("RGBA")

    #image_eye = image_eye.resize((128, 128))
    #image_mouth = image_mouth.resize((128, 128))
    #image_bodies = image_bodies.resize((128, 128))
    #image_arms = image_arms.resize((128, 128))

    result_image = Image.new("RGBA", (256, 256))

    result_image.paste(image_back, (0, 0), image_back)
    result_image.paste(image_bodies, (0, 0), image_bodies)
    result_image.paste(image_eye, (0, 0), image_eye)
    result_image.paste(image_hat, (0, 0), image_hat)
    result_image.paste(image_mouth, (0, 0), image_mouth)
    result_image.paste(image_badge, (0, 0), image_badge)
    result_image.paste(image_arms, (0, 0), image_arms)
    result_image.paste(image_front, (0, 0), image_front)

    #result_image.save("./favicon_pics/"+str(i)+".png", format="png")
    images.append(result_image)

print("Saving pfp")
images[0].save("../pfp.gif", save_all=True, append_images=images[1:], optimize=False, duration=2000, loop=0, disposal=2)
