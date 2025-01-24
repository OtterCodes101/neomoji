import json
import random
from PIL import Image

# Load the parts configuration from JSON file
with open('../parts.json', 'r') as f:
  data = json.load(f)

# No Arms because that made the favicon very noisy
eyes = []
mouth = []
bodies = []

print('Loading URLs of eyes, mouth and bodies...')

# Extract only the URLs for normal eyes
for eye in data['type']['eyes']:
    if eye['name'] == 'normal':
        eyes.append(eye['url'])

# Extract only the URLs for normal mouths
for mund in data['type']['mouth']:
    if mund['name'] == 'normal':
        mouth.append(mund['url'])

# Extract URLs and colors for all body types
for body in data['type']['body']:
    bodies.append([body['url'], body['color']])

# Load random eye and mouth images and convert to RGBA
image_eye = Image.open("../"+random.choice(eyes)).convert("RGBA")
image_mouth = Image.open("../"+random.choice(mouth)).convert("RGBA")

# List to store all generated images for the GIF
images = []

# Number of images to generate
NUM_IMAGES = 300

print(f"Generating {NUM_IMAGES} pictures...")

# Generate the specified number of combinations
for i in range(NUM_IMAGES):
    # Select and load a random body
    chosen_body = random.choice(bodies)
    image_bodies = Image.open("../"+chosen_body[0]).convert("RGBA")

    # Resize all components to 128x128 pixels
    image_eye = image_eye.resize((128, 128))
    image_mouth = image_mouth.resize((128, 128))
    image_bodies = image_bodies.resize((128, 128))

    # Create a new white background image instead of transparent
    result_image = Image.new("RGB", (128, 128), "white")

    # Layer the components: body first, then eyes, then mouth
    result_image.paste(image_bodies, (0, 0), image_bodies)
    result_image.paste(image_eye, (0, 0), image_eye)
    result_image.paste(image_mouth, (0, 0), image_mouth)

    # Add the completed image to our list
    images.append(result_image)

print("Saving favicon")
# Save all images as an animated GIF
# duration=1000 means each frame shows for 1 second
# loop=0 means infinite loop
# disposal=2 means each frame is cleared before showing the next
images[0].save('../favicon.gif', save_all=True, append_images=images[1:], optimize=False, duration=1000, loop=0, disposal=2)
