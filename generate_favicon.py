import json
import random
from PIL import Image


with open('parts.json', 'r') as f:
  data = json.load(f)

#no Arms because that made the favicon very noisy
eyes = []
mouth = []
bodies = []
arms = []
images = []

print('Loading URLs of eyes, mouth and bodies...')

#Extracting only the URLs in list for all three body parts
for eye in data['type']['eyes']:
    eyes.append(eye['url'])

for mund in data['type']['mouth']:
    mouth.append(mund['url'])

for body in data['type']['body']:
    bodies.append([body['url'], body['color']])

for arm in data['type']['arms']:
    arms.append([arm['url'], arm['color']])


print ("Generating 100 pictures...")
for i in range(100):

    color_arms = []
    skip_element = 100

     if i > 1:
        skip_element = random.randint(0,3)

    if skip_element != 2:
        chosen_body = random.choice(bodies)

    for item in arms:
        if item[1] == chosen_body[1]:
            color_arms.append(item[0])



    if skip_element != 0:
        image_eye = Image.open("."+random.choice(eyes)).convert("RGBA")

    if skip_element != 1:
        image_mouth = Image.open("."+random.choice(mouth)).convert("RGBA")

    image_bodies = Image.open("."+chosen_body[0]).convert("RGBA")

    if skip_element != 3:
        image_arms = Image.open("."+random.choice(color_arms)).convert("RGBA")

    image_eye = image_eye.resize((128, 128))
    image_mouth = image_mouth.resize((128, 128))
    image_bodies = image_bodies.resize((128, 128))
    image_arms = image_arms.resize((128, 128))

    result_image = Image.new("RGBA", (128, 128))

    result_image.paste(image_bodies, (0, 0), image_bodies)
    result_image.paste(image_eye, (0, 0), image_eye)
    result_image.paste(image_mouth, (0, 0), image_mouth)
    result_image.paste(image_arms, (0, 0), image_arms)

    #result_image.save("./favicon_pics/"+str(i)+".png", format="png")
    images.append(result_image)

print("Saving favicon")
images[0].save('favicon.gif', save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0, disposal=2)
