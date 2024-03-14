import requests
import logging
import os
import base64
from PIL import Image

from flyer import Flyer

async def get_images(
        url="https://1111.makespacemadrid.org",
        prompt="puppy dog",
        img_size=(512, 512),
        batch_size=5,
        timeout=30) -> list:
    """
    If size is larger than 720, the model will have strong issues generating good images. 

    A possible workaround is to generate them in a smaller resolution keeping the ratio,
    then use a scaling technique using the API to get the thing at the request resolution.
    """

    payload = {
      "prompt": prompt,
      "width": img_size[Flyer.WIDTH],
      "height": img_size[Flyer.HEIGH],
      "batch_size": batch_size,
    }
    response = None

    try:
        response = requests.post(url=f'{url}/sdapi/v1/txt2img', timeout=timeout, json=payload)
    except Exception as e:
        logging.error(e)
        return []

    if response == None or response.status_code != 200:
        if response != None:
            logging.error(f"Could not fetch response: {response.status_code}")
            logging.debug(response)
        return []
    
    r = response.json()

    images = []
    for image_data in r['images']:
        try:
            os.remove("/tmp/output.png")
        except Exception as e:
            # Nothing to remove
            pass

        # An ugly hack to convert bytes to Pil.Image's
        with open("/tmp/output.png", "wb") as f:
            f.write(base64.b64decode(image_data))
        with Image.open("/tmp/output.png").convert("RGBA") as image:
            images.append(image)
        os.remove("/tmp/output.png")
    return images
