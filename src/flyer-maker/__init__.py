"""
flyer maker library
---
"""

from PIL import Image, ImageDraw, ImageFont
import os
import requests
import base64
import time
import threading

import logging

# Read configuration
## This will first be hardcoded here.
number_of_attempts = 1
prompt = ""
title = "MakeSpace - AI Lab #2"
subtitle = "Python con IAs autoalojadas"
date = "Día 20 de Marzo"
timeframe = "19:00-21:00"
place= "Calle Ruiz Palacios 7"
metro = "Tetuán"

# Connect to the remote API and generate image based on prompt.
# Insert title and datetime in frame. 
# Overlay frame over the generated image.

# ImageDraw.textbbox
# ImageDraw.multiline_textbbox

# Size selectors constants
WIDTH=0
HEIGH=1

Sizes = {
    'Facebook': {
        'Landscape': (1200, 628),
        'Portrait': (628, 1200),
        'Square': (1200, 1200),
        'Stories': (1080, 1920),
        'Cover': (851, 315)
    },
    'Instagram': {
        'Landscape': (1080, 566),
        'Portrait': (1080, 1350),
        'Square': (1080, 1080),
        'Stories': (1080, 1920),
        'Cover': None
    },
    'Twitter': {
        'Landscape': (1600, 900),
        'Portrait': (1080, 1350),
        'Square': (1080, 1080),
        'Stories': None,
        'Cover': (1500, 500)
    },
    'LinkedIn': {
        'Landscape': (1200, 627),
        'Portrait': (627, 1200),
        'Square': (1080, 1080),
        'Stories': None,
        'Cover': (1584, 396)
    },
    'TikTok': {
        'Landscape': (1920, 1080),
        'Portrait': (1080, 1920),
        'Square': (1080, 1080),
        'Stories': (1080, 1920),
        'Cover': None
    }
}

def width(size: tuple, percent: float) -> int: return int(size[WIDTH] * percent/100)

def heigh(size: tuple, percent: float) -> int: return int(size[HEIGH] * percent/100)

def resize_factor(size, factor): return (int(size[WIDTH]*factor), int(size[HEIGH]*factor))

def isPortrait(size): return size[0] <= size[1]

def get_files(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            yield filepath

def progress_feedback(response_received_event, timeout):
    print("Requesting images to stable diffussion", end="")
    steps = timeout
    for _ in range(steps):
        if (response_received_event.is_set()):
            return
        time.sleep(timeout/steps)
        print(".", end="", flush=True),
    print("timeout")

def make_stable_diffusion_req(
        url="https://1111.makespacemadrid.org",
        prompt="puppy dog",
        img_size=(512, 512),
        batch_size=5,
        timeout=30):
    # This should probably be its own utility.

    """
    If size is larger than 720, the model will have strong issues generating good images. 

    A possible workaround is to generate them in a smaller resolution keeping the ratio,
    then use a scaling technique using the API to get the thing at the request resolution.
    """

    payload = {
      "prompt": prompt,
      "width": img_size[WIDTH],
      "height": img_size[HEIGH],
      "batch_size": batch_size,
    }
    response_received_event = threading.Event() 
    response_received_event.clear()
    feedback_thread = threading.Thread(target=progress_feedback, args=(response_received_event, timeout))
    feedback_thread.start()
    response = None
    try:
        response = requests.post(url=f'{url}/sdapi/v1/txt2img', timeout=timeout, json=payload)
    except Exception as e:
        print(e)
    response_received_event.set()
    feedback_thread.join()
    if response == None or response.status_code != 200:
        if response != None:
            print(response)

        return []
    r = response.json()
    images = []
    for image_data in r['images']:
        try:
            os.remove("/tmp/output.png")
        except Exception as e:
            # Nothing to remove
            pass
        with open("/tmp/output.png", "wb") as f:
            f.write(base64.b64decode(image_data))
        with Image.open("/tmp/output.png").convert("RGBA") as image:
            images.append(image)
        os.remove("/tmp/output.png")
    return images

def generate_images_for_each_size():
    #sizes = [ for social in Sizes for typeKeys in social for key in social ]
    sizes = []
    wait = 10
    for i, size in enumerate(sizes):
        filename = f"./sizes/{sizes[i][WIDTH]}x{sizes[i][HEIGH]}.png"
        if os.path.isfile(filename):
            print(f"{filename} already exists.")
        else:
            print(f"Generating {filename}")
            generated_images = make_stable_diffusion_req(img_size=size, timeout=3000)
            if generated_images != None and len(generated_images) > 0:
                generated_images[0].save(filename, "PNG")
                print("Done")
            else:
                print(f"{filename} not generated.")
    
            print(f"Waiting {wait} seconds...")
            time.sleep(wait)

# Fonts
def ubuntu_regular(size): return ImageFont.truetype("./fonts/ubuntu/Ubuntu-Regular.ttf", size)
def ubuntu_bold(size): return ImageFont.truetype("./fonts/ubuntu/Ubuntu-Bold.ttf", size)

def main(metro_path: str):
    images = make_stable_diffusion_req(
            prompt="hackerspace cyberpunk city steampunk",
            img_size=Sizes["Facebook"]['Portrait'],
            timeout=160)
    
    for i, base in enumerate(images):
        dark_overlay = Image.new("RGBA", base.size, (0,0,0,128))
        bg = Image.alpha_composite(base, dark_overlay)
        img = ImageDraw.Draw(bg) 
    
        metro_logo = Image.open(metro_path)
        
        # Landscape percentages
        y_percent = 10
        x_percent = 10
        x_increment_percent = 15
        fontsize_small_percent = 4
        fontsize_large_percent = 8
    
        if isPortrait(base.size):
            # Portrait percentages
            y_percent = 5
            x_percent = 15
            x_increment_percent = 10
            fontsize_small_percent = 7
            fontsize_large_percent = 10
        
        ytxt = width(base.size, y_percent)
        xtxt = heigh(base.size, x_percent)
        xincrements = heigh(base.size, x_increment_percent)
        fontsize_small = width(base.size, fontsize_small_percent)
        fontsize_large = width(base.size, fontsize_large_percent)
        scale_ratio = fontsize_small/metro_logo.size[HEIGH]
       
        #mkspace_logo = mkspace_logo.resize(resize_factor(mkspace_logo.size, scale_ratio))
        #bg.alpha_composite(mkspace_logo, (width(base.size, 50)+mkspace_logo.size[WIDTH], heigh(base.size, 5)))
    
        # Add title
        img.multiline_text((ytxt, xtxt), title, align="center", font=ubuntu_regular(fontsize_large), fill=(255,255,255,255))
        xtxt += xincrements
        # Add Subtitle
        img.multiline_text((ytxt, xtxt), subtitle, align="center", font=ubuntu_regular(fontsize_small), fill=(255,255,255,255))
        xtxt += xincrements
        # Add Date
        img.multiline_text((ytxt, xtxt), date, align="center", font=ubuntu_regular(fontsize_large), fill=(255,255,255,255))
        xtxt += xincrements
        # Add Time frame
        img.multiline_text((ytxt, xtxt), timeframe, align="center", font=ubuntu_regular(fontsize_small), fill=(255,255,255,255))
        xtxt += xincrements
        # Add place
        img.multiline_text((ytxt, xtxt), place, align="center", font=ubuntu_regular(fontsize_large), fill=(255,255,255,255))
        xtxt += xincrements
        # Add metro
        # Obtain scale ratio according to scaled font height
        metro_logo = metro_logo.resize(resize_factor(metro_logo.size, scale_ratio))
        bg.alpha_composite(metro_logo, (ytxt, xtxt))
        img.multiline_text((metro_logo.size[WIDTH]+ytxt, xtxt), metro, align="center", font=ubuntu_regular(fontsize_small), fill=(255,255,255,255))
        
        print(f"./out/out_{i}.png")
        bg.save(f"./out/out_{i}.png", "PNG")
        print(f"./out/out_{i}.pdf")
        bg.save(f"./out/out_{i}.pdf", "PDF")
        bg.show()

if __name__ == "__main__":
    import sys
    # Obtain arguments
    if len(sys.argv) == 1:
        logging.error("Manadatory arguments required.")
        logging.info("./flyer_maker.py <output path>")
    main()

    pass
